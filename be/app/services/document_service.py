import ast
import asyncio
import json
import re
import time

from botocore.exceptions import NoCredentialsError, ClientError
from sqlalchemy.orm import Session
from app.models.document import UserDocument, ContactMessage
from app.schemas.document import DocumentCreate, ContactMessageCreate
from app.services.user_service import get_user_by_id
from fastapi import HTTPException, status, UploadFile
import os
import uuid
from dotenv import load_dotenv
from typing import Optional
from app.core.global_instances import (
    get_pdf, get_llama_chunks, get_llama_title, get_llama_content,
    get_qdrant, get_neo, get_preprocessing, get_s3_client
)
from LLM.prompt import extract_entities_relationship_from_text, chunking, create_title
import ast
import traceback
from fastapi import HTTPException
load_dotenv()

# AWS S3 Configuration
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "khoaluan111")
S3_REGION = os.getenv("S3_REGION", "ap-southeast-1")

# Global instances will be initialized lazily when needed
def _get_global_instances():
    """Get all global instances lazily"""
    return {
        'pdf': get_pdf(),
        'llama_chunks': get_llama_chunks(),
        'llama_title': get_llama_title(),
        'llama_content': get_llama_content(),
        'qdrant': get_qdrant(),
        'neo': get_neo(),
        'pre_processing': get_preprocessing(),
        's3_client': get_s3_client()
    }

def get_user_documents(db: Session, user_id: int):
    """Get all documents for a user"""
    return db.query(UserDocument).filter(UserDocument.user_id == user_id).all()

def get_document(db: Session, document_id: int):
    """Get a document by ID"""
    return db.query(UserDocument).filter(UserDocument.id == document_id).first()

def get_document_by_external_id(db: Session, document_id: str, user_id: int):
    """Get a document by external ID (document_id field)"""
    return db.query(UserDocument).filter(
        UserDocument.document_id == document_id,
        UserDocument.user_id == user_id
    ).first()

def create_document(db: Session, document: DocumentCreate, user_id: int):
    """Create a new document record"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db_document = UserDocument(
        user_id=user_id,
        conversation_id=document.conversation_id,
        document_id=document.document_id,
        filename=document.filename,
        file_size=document.file_size,
        status=document.status,
        s3_key=document.s3_key,
        s3_url=document.s3_url
    )
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return db_document

def update_document_status(db: Session, document_id: str, status: str, user_id: int):
    """Update a document's status"""
    document = get_document_by_external_id(db, document_id, user_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    document.status = status
    db.commit()
    db.refresh(document)
    
    return document

def upload_to_s3(file_content: bytes, file_name: str, document_id: str) -> dict:
    """Upload a file to S3"""
    instances = _get_global_instances()
    s3_client = instances['s3_client']
    
    if not s3_client:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="S3 client not initialized"
        )
    
    try:
        # Create S3 key with document_id to avoid duplicates
        s3_key = f"documents/{document_id}/{file_name}"
        
        # Upload file to S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=file_content,
            ContentType='application/pdf'
        )
        
        s3_url = f"s3://{S3_BUCKET_NAME}/{s3_key}"
        
        return {
            "s3_key": s3_key,
            "s3_url": s3_url
        }
    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload to S3: {str(e)}"
        )

async def process_file_upload(file: UploadFile, user_id: int, db: Session):
    """Process a file upload"""
    # Validate file
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file uploaded"
        )
    
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are accepted"
        )
    
    # Generate document ID
    document_id = str(uuid.uuid4())
    
    # Read file content
    contents = await file.read()
    if not contents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty or could not be read"
        )
    
    # Upload to S3
    s3_info = upload_to_s3(contents, file.filename, document_id)
    print('in main: ' + document_id)
    # Create document record
    document = DocumentCreate(
        document_id=document_id,
        filename=file.filename,
        file_size=len(contents),
        status="processing",
        s3_key=s3_info["s3_key"],
        s3_url=s3_info["s3_url"]
    )
    
    db_document = create_document(db, document, user_id)

    # Process PDF after uploading to S3
    try:
        # Add timeout for PDF processing (20 minutes)
        await asyncio.wait_for(
            process_pdf(s3_info["s3_url"], s3_info["s3_key"], document_id),
            timeout=1200  # 20 minutes = 1200 seconds
        )
        # Update document status to completed
        update_document_status(db, document_id, "completed", user_id)
        final_status = "completed"
        print(f"🎉 PDF processing completed for document: {document_id}")
    except asyncio.TimeoutError:
        print(f"⏰ PDF processing timeout for document: {document_id}")
        update_document_status(db, document_id, "failed", user_id)
        final_status = "failed"
    except Exception as e:
        print(f"❌ Error processing PDF for document {document_id}: {str(e)}")
        # Update document status to failed
        update_document_status(db, document_id, "failed", user_id)
        final_status = "failed"

    return {
        "document_id": document_id,
        "filename": file.filename,
        "file_size": len(contents),
        "s3_key": s3_info["s3_key"],
        "s3_url": s3_info["s3_url"],
        "status": final_status
    }



def upload_to_s3_key(file_content: bytes, file_name: str, document_id: str) -> str:
    """
    Upload file to S3 and return the S3 key
    """
    try:
        instances = _get_global_instances()
        s3_client = instances['s3_client']
        
        if not s3_client:
            raise Exception("S3 client not initialized")

        # Tạo S3 key với document_id để tránh trùng lặp
        s3_key = f"documents/{document_id}/{file_name}"

        # Upload file to S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=file_content,
            ContentType='application/pdf'
        )

        print(f"File uploaded to S3: s3://{S3_BUCKET_NAME}/{s3_key}")
        return s3_key

    except NoCredentialsError:
        print("AWS credentials not found")
        raise Exception("AWS credentials not configured")
    except ClientError as e:
        print(f"AWS S3 error: {str(e)}")
        raise Exception(f"Failed to upload to S3: {str(e)}")
    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")
        raise


def get_s3_file_url(s3_key: str) -> str:
    """
    Generate S3 file URL
    """
    return f"s3://{S3_BUCKET_NAME}/{s3_key}"


async def process_pdf(s3_file_url: str, s3_key: str, document_id: str):
    try:
        instances = _get_global_instances()
        pdf = instances['pdf']
        
        pdf.set_path(s3_file_url)
        pdf.set_bucket_name(S3_BUCKET_NAME)
        pdf.set_key(s3_key)
        sentences = pdf.read_chunks()

        await _add_data_to_qdrant(sentences, document_id)
        await _add_data_to_neo4j(sentences, document_id)

        print("🎉 PDF processing hoàn tất.")
    except Exception as e:
        print(f"❌ Error during processing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error {str(e)}")


# Thêm file mới vào qdrant
async def _add_data_to_qdrant(sentences, document_id):
    print('in qdrant: ' + document_id)
    try:
        instances = _get_global_instances()
        llama_chunks = instances['llama_chunks']
        qdrant = instances['qdrant']

        chunks = []
        all_paragraphs = []

        llama_chunks.set_prompt(chunking())

        for idx, s in enumerate(sentences):
            print("văn bản ban đầu: " + s)
            llama_chunks.set_text(s)
            print(f"\n--- Sentence {idx + 1}/{len(sentences)} ---")
            try:
                raw_output = llama_chunks.generator()
                print("[Lần 1] Raw output:", repr(raw_output))

                # Nếu muốn parse Python literal
                chunk_json = ast.literal_eval(raw_output)
                print("[Lần 1] Parsed data:", chunk_json)

            except Exception as e1:
                print("[Lần 1] Lỗi parse:", e1)
                traceback.print_exc()

                try:
                    raw_output_2 = llama_chunks.generator()
                    print("[Lần 2] Raw output:", repr(raw_output_2))

                    chunk_json = ast.literal_eval(raw_output_2)
                    print("[Lần 2] Parsed data:", chunk_json)

                except Exception as e2:
                    print("[Lần 2] Lỗi parse:", e2)
                    traceback.print_exc()
                    raise HTTPException(
                        status_code=500,
                        detail=f"Không parse được chunk_json cho câu {idx + 1}"
                    )

            chunks.append(chunk_json)

        # Tạo mảng các paragraph
        for chunk in chunks:
            for key, content in chunk.items():
                all_paragraphs.append(content)

        print("\nTổng số paragraph:", len(all_paragraphs))
        print("Danh sách paragraph:", all_paragraphs)

        # 1. tạo collection trong qdrant
        qdrant.set_collection_name(document_id)
        qdrant.create_collection()

        # 2. Tạo embedding
        embeddings_dict = qdrant.create_embed(all_paragraphs)
        print("Embeddings đã tạo, số lượng:", len(embeddings_dict))

        # 3. lưu vào qdrant
        qdrant.add_data(all_paragraphs, embeddings_dict)
        print("Đã lưu vào Qdrant thành công.")

        return {
            "message": "File uploaded and processed successfully for qdrant",
            "data": document_id
        }

    except Exception as e:
        print(f"[ERROR] Error processing file in qdrant: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file in qdrant: {str(e)}"
        )


async def _add_data_to_neo4j(sentences, document_id):
    try:
        print("\n[DEBUG] Bắt đầu xử lý file cho Neo4j")
        instances = _get_global_instances()
        llama_title = instances['llama_title']
        llama_content = instances['llama_content']
        neo = instances['neo']
        pre_processing = instances['pre_processing']

        # =========================
        # BƯỚC 1: TẠO TIÊU ĐỀ
        # =========================
        titles = []
        llama_title.set_prompt(create_title())
        print("\n[DEBUG] Tạo tiêu đề cho từng câu...")
        for i, s in enumerate(sentences):
            try:
                llama_title.set_text(s)
                raw_title = llama_title.generator().lower()
                print(f"\n[Title {i + 1}] Raw output:", repr(raw_title))

                title_json = pre_processing.string_to_json(raw_title)
                print(f"[Title {i + 1}] Parsed JSON:", title_json)

                titles.append(title_json)

                # Sleep để tránh rate-limit nếu cần
                if i % 2 == 0 and i != 0:
                    print(f"[DEBUG] Sleep 45s sau câu thứ {i + 1}...")
                    time.sleep(45)

            except Exception as e:
                print(f"[ERROR] Lỗi khi xử lý tiêu đề câu {i + 1}: {e}")
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=f"Lỗi parse tiêu đề tại câu {i + 1}: {e}")

        print("\n[DEBUG] Danh sách tiêu đề cuối cùng:", titles)

        # =========================
        # BƯỚC 2: TẠO ENTITIES & RELATIONSHIPS
        # =========================
        entities_relationship = []
        llama_content.set_prompt(extract_entities_relationship_from_text())
        print("\n[DEBUG] Tạo entities & relationships cho từng câu...")

        for i, s in enumerate(sentences):
            try:
                llama_content.set_text(s)
                raw_er = llama_content.generator().lower()
                print(f"\n[Entities {i + 1}] Raw output:", repr(raw_er))

                match = re.search(r'(\{\s*"relationships".*\})', raw_er, re.DOTALL)
                if match:
                    json_str = match.group(1)
                    try:
                        er_json = json.loads(json_str)
                        print(f"[Entities {i + 1}] Parsed JSON:", er_json)
                        entities_relationship.append(er_json)
                    except json.JSONDecodeError as e:
                        try:
                            raw_er = llama_content.generator().lower()
                            match = re.search(r'(\{\s*"relationships".*\})', raw_er, re.DOTALL)
                            if match:
                                json_str = match.group(1)
                                er_json = json.loads(json_str)
                                print(f"[Entities {i + 1}] Parsed JSON:", er_json)
                                entities_relationship.append(er_json)
                        except:
                            print("Lỗi parse JSON:", e)
            except Exception as e:
                print(f"[ERROR] Lỗi khi xử lý entities câu {i + 1}: {e}")
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=f"Lỗi parse entities tại câu {i + 1}: {e}")

        print("\n[DEBUG] Danh sách entities_relationship cuối cùng:", entities_relationship)

        # =========================
        # BƯỚC 3: LƯU VÀO NEO4J
        # =========================
        print("\n[DEBUG] Thêm node & relationship vào Neo4j...")

        try:
            # B1: Nối "General" với Document
            neo.add_single_relationship("tài liệu", "General", document_id, "Document", "BAO_GỒM")
            print(f"[Neo4j] Đã nối 'General' -> Document {document_id}")

            # B2: Nối Document với tiêu đề
            for title in titles:
                neo.add_single_relationship(document_id, "Document", title["title"], "Part", "BAO_GỒM")
                print(f"[Neo4j] Đã nối Document {document_id} -> Part {title['title']}")

            # B3: Nối tiêu đề với entities_relationship
            for r, title in zip(entities_relationship, titles):
                neo.import_relationships(r, title["title"], "Part")
                print(f"[Neo4j] Đã import relationships cho Part {title['title']}")

        except Exception as e:
            print(f"[ERROR] Lỗi khi insert vào Neo4j: {e}")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Lỗi insert vào Neo4j: {e}")

        print("\n[DEBUG] Hoàn tất thêm dữ liệu vào Neo4j.")
        return {
            "message": "File uploaded and processed successfully for neo4j",
            "data": document_id
        }

    except Exception as e:
        print(f"[ERROR] Error processing file in neo4j: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing file in neo4j: {str(e)}")


def create_contact_message(db: Session, contact: ContactMessageCreate):
    """Create a new contact message"""
    db_contact = ContactMessage(
        name=contact.name,
        email=contact.email,
        subject=contact.subject,
        message=contact.message
    )
    
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    
    return db_contact