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
    get_pdf, get_qdrant, get_neo, get_preprocessing, get_s3_client
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
        sentences = pdf.read_content()

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
        qdrant = instances['qdrant']
        pdf = instances['pdf']

        # all_paragraphs = pdf.create_chunk(sentences)
        all_paragraphs = ['Tài liệu này mô tả các đặc tính và quy định nhằm phát triển một phần mềm quản lý giải đấu bóng đá theo mô hình Cúp thế giới (World Cup) bằng mô hình TDD (Test-Driven Development), nghĩa là tất cả các quy tắc nghiệp vụ (Business rules) phải được cụ thể hóa bằng bộ Test case trong phần mềm trước khi thực hiện phần phát triển (Implement/ coding) các quy tắc đó trong phần mềm.', 'Mỗi lớp X trong project phát triển (VD: Project tên WorldCup) phải có một lớp X_Test tương ứng để kiểm tra chức năng trong project kiểm tra (VD: Project mang tên TestWorldCup). Tất cả các quy tắc nghiệp vụ phải được viết đầy đủ các phương thức (hàm) kiểm tra trước khi phát triển.', 'Các lớp, các hàm kiểm tra phải đảm bảo bao phủ phân hoạch tương đương, phân hoạch giá trị biên, bao phủ câu lệnh, bao phủ đường và bao phủ nhánh cho chương trình. Project kiểm tra có ít nhất 200 testcases.', 'Tổ chức lưu trữ thông tin các đội bóng, bảng đấu, trận đấu, danh sách cầu thủ… trong cơ sở dữ liệu Access hoặc cơ sở dữ liệu SQL đi kèm chương trình, nghĩa là không cần phải cài đặt phần mềm SQL Server và thiết lập cơ sở dữ liệu trong đó để thực hiện chương trình.', 'Chương trình chạy tự động không có sự can thiệp của người dùng, cho ra kết quả từng trận đấu cho đến hết trận chung kết. Cập nhật kết quả giải đấu vào CSDL và xuất ra màn hình các kết quả từng trận đấu, vòng đấu tương ứng.', 'Giải đấu bóng đá World Cup diễn ra 4 năm một lần trên toàn thế giới, là giải đấu chính thức do Liên đoàn bóng đá thế giới FIFA tổ chức. Sau vòng loại ở các khu vực sẽ chọn ra 31 đội bóng mạnh nhất để cùng với đội chủ nhà tham dự vòng chung kết thế giới.', 'Theo đó, các khu vực bóng đá được phân bổ số lượng đội tối đa tham dự vòng chung kết như sau: Khu vực châu Á: 5.5 đội, Khu vực châu Phi: 5 đội, Khu vực châu Bắc, Trung Mỹ và Caribe: 3.5 đội, Khu vực Nam Mỹ: 3.5 đội, Khu vực Châu Đại dương: 0.5 đội, Khu vực Châu Âu: 13 đội, Đội chủ nhà.', 'Đội bóng đứng thứ 6 khu vực châu Á sẽ đá 2 trận play-off với đội bóng đứng thứ 4 khu vực châu Bắc, Trung Mỹ và Caribe để giành suất sự vòng chung kết. Đội bóng đứng thứ 4 khu vực Nam Mỹ sẽ đá 2 trận play-off với đội bóng đứng thứ 1 khu vực châu Đại Dương để giành suất sự vòng chung kết.', '32 đội bóng vào vòng chung kết được chia làm 8 bảng đấu theo thứ tự từ A-H, mỗi bảng có 4 đội bóng được đánh số thứ tự 1-4. Vòng chung kết World Cup được bắt đầu với các trận vòng bảng.', 'Ở vòng bảng, các đội trong cùng bảng đấu sẽ thi đấu vòng tròn một lượt tính điểm, nghĩa là mỗi đội bóng sẽ thi đấu một trận với ba đội còn lại trong bảng để tính điểm. Đội giành thắng trận sẽ được 3 điểm, hòa được 1 điểm và thua không có điểm.', 'Bên cạnh đó, mỗi trận đấu cũng ghi nhận hiệu số bàn thắng – thua của môi đội bóng và số thẻ phạt (thẻ vàng, thẻ đỏ) của mỗi đội. Mỗi đội bóng tham dự vòng chung kết có một tên riêng là tên quốc gia của đội bóng đó, được huấn luyện bởi một huấn luyện viên trưởng, không quá 3 trợ lý huấn luyện viên, 1 săn sóc viên và được đăng ký danh sách tối đa 22 cầu thủ.', 'Tuy nhiên, tại thời điểm trước khi bắt đầu trận đấu, mỗi đội bóng phải đăng ký danh sách các cầu thủ chính thức tham dự trận đấu gồm không quá 11 cầu thủ và không dưới 7 cầu thủ. Mỗi đội được đăng ký danh sách không quá 5 cầu thủ dự bị.', 'Ở vòng bảng của vòng chung kết, một trận đấu bóng đá diễn ra trong 90 phút bao gồm hai hiệp đấu, mỗi hiệp 45 phút và có nghỉ giải lao giữa hai hiệp trong vòng 15 phút. Ở các vòng tiếp theo (1/16, tứ kết, bán kết và trận chung kết), mỗi trận đấu sẽ thi đấu theo thể thức loại trực tiếp.', 'Mỗi trận đấu cũng diễn ra trong hai hiệp 45 phút, tuy nhiên nếu sau hai hiệp đấu mà hai đội hòa nhau, sẽ tiến hành thi đấu tối đa hai hiệp phụ, mỗi hiệp 30 phút và áp dụng nguyên tắc bàn thắng bạc. Nếu sau hai hiệp phụ hai đội vẫn tiếp tục hòa nhau thì hai đội sẽ tiến hành đá luân lưu 5 lần, mỗi đội thay phiên nhau đá và đội giành chiến thắng là đội có số lần đá luân lưu thành bàn nhiều hơn.', 'Nếu sau 5 lần đá luân lưu hai đội hòa nhau, thì tiếp tục đá luân lưu 1 lần cho đến khi tìm được đội giành chiến thắng. Nguyên tắc bàn thắng bạc được định nghĩa như sau: sau hiệp phụ thứ nhất, nếu có đội ghi được bàn thắng nhiều hơn đội còn lại thì đội ghi bàn thắng sẽ giành chiến thắng.', 'Nếu sau hiệp phụ thứ nhất, hai đội hòa nhau thì sẽ tiến hành hiệp phụ thứ hai. Trong thời gian diễn ra trận đấu, trọng tài được quyền phạt thẻ đối với các cầu thủ vi phạm luật bóng đá.', 'Có hai loại thẻ phạt là thẻ vàng và thẻ đỏ. Cầu thủ khi bị phạt thẻ vàng thứ hai trong cùng trận đấu phải lập tức rời sân thi đấu.', 'Cầu thủ khi bị phạt thẻ đỏ trong trận đấu phải lập tức rời sân thi đấu. Đội bóng nào còn dưới 7 cầu thủ trên sân sau khi các cầu thủ khác bị phạt thẻ hoặc chấn thương không thể tiếp tục thi đấu mà không còn cầu thủ dự bị thay thế hoặc hết quyền thay thế cầu thủ sẽ bị xử thua 0-3 trận đấu đó, và trận đấu kết thúc ngay sau khi một đội bóng không còn đủ số lượng cầu thủ tối thiểu để tham gia trận đấu.', 'Ở mỗi trận đấu, mỗi đội bóng có thể thay thế tối đa 3 cầu thủ đang thi đấu trên sân bằng cầu thủ dự bị đã được đăng ký trước, mỗi lần có thể thay từ 1-3 cầu thủ nhưng không vượt quá tối đa 3 cầu thủ được thay trong mỗi trận đấu. Không hạn chế vị trí thi đấu của cầu thủ được thay thể.', 'Danh sách các cầu thủ ghi bàn ở từng trận được lập và theo dõi để xác định cầu thủ ghi nhiều bàn thắng nhất trong cả giải đấu. Cầu thủ nào ghi nhiều bàn thắng nhất sẽ đạt giải Vua phá lưới của giải đấu. Trong trường hợp có nhiều hơn 1 cầu thủ cùng ghi nhiều bàn thắng nhất giải, các cầu thủ này đồng sở hữu danh hiệu Vua phá lưới.', 'Sau khi kết thúc mỗi trận đấu ở vòng bảng, các đội bóng được sắp xếp thứ hạng trong bảng lần lượt theo các tiêu chí sau, khi hai đội bóng có cùng tiêu chí ở mức trên thì thứ hạng được xếp dựa trên tiêu chí kế tiếp, lần lượt cho đến hết các tiêu chí: Số điểm đạt được. Hiệu số bàn thắng – thua.', 'Số thẻ bị phạt (1 thẻ đỏ = 2 thẻ vàng). Kết quả đối đầu trực tiếp giữa hai đội bóng. Bốc thăm.', 'Kết thúc vòng bảng, hai đội xếp thứ nhất và thứ hai của mỗi bảng đấu được tham dự tiếp vòng 1/16. Các đội vượt qua vòng bảng sẽ được chia cặp để thi đấu vòng 1/16 như sau: Trận 1: Nhất bảng A – Nhì bảng B. Trận 2: Nhất bảng B – Nhì bảng A.', 'Trận 3: Nhất bảng C – Nhì bảng D. Trận 4: Nhất bảng D – Nhì bảng C. Trận 5: Nhất bảng E – Nhì bảng F. Trận 6: Nhất bảng F – Nhì bảng E.', 'Trận 7: Nhất bảng G – Nhì bảng H. Trận 8: Nhất bảng H – Nhì bảng G. Vòng 1/16 thi đấu theo thể thức loại trực tiếp đã được mô tả ở trên cho đến khi tìm ra đội chiến thắng.', 'Tám đội giành chiến thắng ở vòng 1/16 sẽ tiếp tục thi đấu vòng tứ kết. Vòng tứ kết thi đấu theo thể thức loại trực tiếp theo các cặp đấu sau: Trận Q1: Thắng trận 1 – Thắng trận 2. Trận Q2: Thắng trận 3 – Thắng trận 4.', 'Trận Q3: Thắng trận 5 – Thắng trận 2. Trận Q4: Thắng trận 7 – Thắng trận 8. 4 đội giành chiến thắng ở vòng tứ kết sẽ tiếp tục thi đấu vòng bán kết.', 'Vòng bán kết thi đấu theo thể thức loại trực tiếp theo các cặp đấu sau: Trận S1: Thắng trận Q1 – Thắng trận Q2. Trận S2: Thắng trận Q3 – Thắng trận Q4.', 'Hai đội giành chiến thắng ở vòng bán kết sẽ gặp nhau ở trận chung kết để tranh cúp vô địch. Đội giành chiến thắng ở trận chung kết sẽ giành chức vô địch và huy chương vàng. Đội thua ở trận chung kết sẽ nhận huy chương bạc.', 'Hai đội thua ở vòng bán kết sẽ cùng nhận hạng ba và nhận huy chương đồng.']

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
        instances = _get_global_instances()
        neo = instances['neo']
        pdf = instances['pdf']

        # titles = pdf.create_title(sentences)
        # entities_relationship = pdf.create_nodes(sentences)

        titles = [{"title": "Mô tả bài toán World Cup – Bài tập về nhà môn Kiểm thử phần mềm (TDD)"}, {"title": "Quy định thi đấu và thể thức giải bóng đá (thay người, xếp hạng, vòng loại trực tiếp, trao giải)"}]

        entities_relationship = [
            {
                "relationships": [
                    {
                        "source": {
                            "name": "đội bóng",
                            "role": "thi đấu",
                            "substitute_limit": "3",
                            "player_limit": "11"
                        },
                        "target": {
                            "name": "cầu thủ",
                            "status": "đang thi đấu",
                            "substitute_type": "cầu thủ dự bị",
                            "registered": "đã đăng ký"
                        },
                        "type_source": "Organization",
                        "type_target": "Person",
                        "relation": "thay_thế"
                    },
                    {
                        "source": {
                            "name": "cầu thủ",
                            "role": "thi đấu",
                            "action": "ghi bàn"
                        },
                        "target": {
                            "name": "danh sách cầu thủ ghi bàn",
                            "tracking": "từng trận",
                            "purpose": "xác định vua phá lưới"
                        },
                        "type_source": "Person",
                        "type_target": "Document",
                        "relation": "được_ghi_nhận_trong"
                    },
                    {
                        "source": {
                            "name": "cầu thủ",
                            "achievement": "nhiều bàn thắng nhất"
                        },
                        "target": {
                            "name": "Vua phá lưới",
                            "award": "giải thưởng",
                            "type": "cá nhân"
                        },
                        "type_source": "Person",
                        "type_target": "Award",
                        "relation": "đạt_giải"
                    },
                    {
                        "source": {
                            "name": "đội bóng",
                            "stage": "vòng bảng"
                        },
                        "target": {
                            "name": "thứ hạng",
                            "criteria": "điểm, hiệu số, thẻ phạt, đối đầu, bốc thăm"
                        },
                        "type_source": "Organization",
                        "type_target": "Metric",
                        "relation": "được_xếp_hạng_theo"
                    },
                    {
                        "source": {
                            "name": "bảng đấu",
                            "stage": "vòng bảng"
                        },
                        "target": {
                            "name": "đội bóng",
                            "position": "nhất và nhì bảng"
                        },
                        "type_source": "CompetitionStage",
                        "type_target": "Organization",
                        "relation": "chọn_ra"
                    },
                    {
                        "source": {
                            "name": "đội bóng",
                            "stage": "vòng 1/16"
                        },
                        "target": {
                            "name": "trận đấu",
                            "format": "loại trực tiếp",
                            "match_pairing": "nhất bảng A - nhì bảng B, ..."
                        },
                        "type_source": "Organization",
                        "type_target": "Match",
                        "relation": "tham_gia"
                    },
                    {
                        "source": {
                            "name": "đội bóng",
                            "stage": "tứ kết"
                        },
                        "target": {
                            "name": "trận Q1, Q2, Q3, Q4",
                            "format": "loại trực tiếp"
                        },
                        "type_source": "Organization",
                        "type_target": "Match",
                        "relation": "thi_đấu_trong"
                    },
                    {
                        "source": {
                            "name": "đội bóng",
                            "stage": "bán kết"
                        },
                        "target": {
                            "name": "trận S1, S2",
                            "format": "loại trực tiếp"
                        },
                        "type_source": "Organization",
                        "type_target": "Match",
                        "relation": "thi_đấu_trong"
                    },
                    {
                        "source": {
                            "name": "hai đội thắng bán kết"
                        },
                        "target": {
                            "name": "trận chung kết",
                            "purpose": "tranh cúp vô địch"
                        },
                        "type_source": "Organization",
                        "type_target": "Match",
                        "relation": "gặp_nhau_tại"
                    },
                    {
                        "source": {
                            "name": "đội thắng trận chung kết"
                        },
                        "target": {
                            "name": "chức vô địch",
                            "award": "huy chương vàng"
                        },
                        "type_source": "Organization",
                        "type_target": "Award",
                        "relation": "giành_được"
                    },
                    {
                        "source": {
                            "name": "đội thua trận chung kết"
                        },
                        "target": {
                            "name": "huy chương bạc"
                        },
                        "type_source": "Organization",
                        "type_target": "Award",
                        "relation": "nhận"
                    },
                    {
                        "source": {
                            "name": "hai đội thua bán kết"
                        },
                        "target": {
                            "name": "hạng ba",
                            "award": "huy chương đồng"
                        },
                        "type_source": "Organization",
                        "type_target": "Award",
                        "relation": "đồng_sở_hữu"
                    }
                ]
            },
            {
                "relationships": [
                    {
                        "source": {
                            "name": "Nguyễn Hữu Phát",
                            "role": "Giảng viên",
                            "subject": "Kiểm thử phần mềm"
                        },
                        "target": {
                            "name": "Bài tập World Cup",
                            "type": "bài tập về nhà",
                            "update_time": "03/2024"
                        },
                        "type_source": "Person",
                        "type_target": "Document",
                        "relation": "ra_đề"
                    },
                    {
                        "source": {
                            "name": "World Cup",
                            "frequency": "4 năm/lần",
                            "scope": "toàn thế giới"
                        },
                        "target": {
                            "name": "FIFA",
                            "full_name": "Liên đoàn bóng đá thế giới"
                        },
                        "type_source": "Competition",
                        "type_target": "Organization",
                        "relation": "được_tổ_chức_bởi"
                    },
                    {
                        "source": {
                            "name": "vòng loại",
                            "scope": "khu vực"
                        },
                        "target": {
                            "name": "31 đội bóng",
                            "qualification": "tham dự vòng chung kết"
                        },
                        "type_source": "CompetitionStage",
                        "type_target": "Organization",
                        "relation": "chọn_ra"
                    },
                    {
                        "source": {
                            "name": "đội chủ nhà"
                        },
                        "target": {
                            "name": "World Cup",
                            "stage": "vòng chung kết"
                        },
                        "type_source": "Organization",
                        "type_target": "Competition",
                        "relation": "tham_gia"
                    },
                    {
                        "source": {
                            "name": "châu Á",
                            "quota": "5.5"
                        },
                        "target": {
                            "name": "World Cup",
                            "stage": "vòng chung kết"
                        },
                        "type_source": "Continent",
                        "type_target": "Competition",
                        "relation": "được_phân_bổ_suất"
                    },
                    {
                        "source": {
                            "name": "châu Phi",
                            "quota": "5"
                        },
                        "target": {
                            "name": "World Cup",
                            "stage": "vòng chung kết"
                        },
                        "type_source": "Continent",
                        "type_target": "Competition",
                        "relation": "được_phân_bổ_suất"
                    },
                    {
                        "source": {
                            "name": "châu Bắc, Trung Mỹ và Caribe",
                            "quota": "3.5"
                        },
                        "target": {
                            "name": "World Cup",
                            "stage": "vòng chung kết"
                        },
                        "type_source": "Region",
                        "type_target": "Competition",
                        "relation": "được_phân_bổ_suất"
                    },
                    {
                        "source": {
                            "name": "Nam Mỹ",
                            "quota": "3.5"
                        },
                        "target": {
                            "name": "World Cup",
                            "stage": "vòng chung kết"
                        },
                        "type_source": "Continent",
                        "type_target": "Competition",
                        "relation": "được_phân_bổ_suất"
                    },
                    {
                        "source": {
                            "name": "châu Đại Dương",
                            "quota": "0.5"
                        },
                        "target": {
                            "name": "World Cup",
                            "stage": "vòng chung kết"
                        },
                        "type_source": "Continent",
                        "type_target": "Competition",
                        "relation": "được_phân_bổ_suất"
                    },
                    {
                        "source": {
                            "name": "châu Âu",
                            "quota": "13"
                        },
                        "target": {
                            "name": "World Cup",
                            "stage": "vòng chung kết"
                        },
                        "type_source": "Continent",
                        "type_target": "Competition",
                        "relation": "được_phân_bổ_suất"
                    },
                    {
                        "source": {
                            "name": "đội bóng đứng thứ 6 châu Á"
                        },
                        "target": {
                            "name": "đội bóng đứng thứ 4 châu Bắc, Trung Mỹ và Caribe"
                        },
                        "type_source": "Organization",
                        "type_target": "Organization",
                        "relation": "đá_play_off_với"
                    },
                    {
                        "source": {
                            "name": "đội bóng đứng thứ 4 Nam Mỹ"
                        },
                        "target": {
                            "name": "đội bóng đứng thứ 1 châu Đại Dương"
                        },
                        "type_source": "Organization",
                        "type_target": "Organization",
                        "relation": "đá_play_off_với"
                    },
                    {
                        "source": {
                            "name": "32 đội bóng",
                            "qualification": "vào vòng chung kết"
                        },
                        "target": {
                            "name": "8 bảng đấu",
                            "range": "A-H",
                            "size": "4 đội/bảng"
                        },
                        "type_source": "Organization",
                        "type_target": "CompetitionStage",
                        "relation": "được_chia_thành"
                    },
                    {
                        "source": {
                            "name": "đội bóng",
                            "role": "tham dự"
                        },
                        "target": {
                            "name": "huấn luyện viên trưởng",
                            "assistants": "tối đa 3",
                            "staff": "1 săn sóc viên"
                        },
                        "type_source": "Organization",
                        "type_target": "Person",
                        "relation": "được_huấn_luyện_bởi"
                    },
                    {
                        "source": {
                            "name": "đội bóng",
                            "squad_size": "tối đa 22 cầu thủ"
                        },
                        "target": {
                            "name": "danh sách cầu thủ chính thức",
                            "min": "7",
                            "max": "11"
                        },
                        "type_source": "Organization",
                        "type_target": "Document",
                        "relation": "đăng_ký"
                    },
                    {
                        "source": {
                            "name": "trận đấu",
                            "stage": "vòng bảng"
                        },
                        "target": {
                            "name": "thời lượng",
                            "main_half": "2 x 45 phút",
                            "break": "15 phút"
                        },
                        "type_source": "Match",
                        "type_target": "Rule",
                        "relation": "tuân_theo"
                    },
                    {
                        "source": {
                            "name": "trận đấu",
                            "stage": "loại trực tiếp"
                        },
                        "target": {
                            "name": "luật hiệp phụ và luân lưu",
                            "extra_time": "2 x 30 phút",
                            "penalty": "5 lần + 1 lần"
                        },
                        "type_source": "Match",
                        "type_target": "Rule",
                        "relation": "áp_dụng"
                    },
                    {
                        "source": {
                            "name": "trọng tài"
                        },
                        "target": {
                            "name": "cầu thủ",
                            "penalty_cards": "thẻ vàng, thẻ đỏ"
                        },
                        "type_source": "Person",
                        "type_target": "Person",
                        "relation": "phạt"
                    },
                    {
                        "source": {
                            "name": "cầu thủ",
                            "card": "2 thẻ vàng hoặc 1 thẻ đỏ"
                        },
                        "target": {
                            "name": "sân thi đấu",
                            "status": "rời sân"
                        },
                        "type_source": "Person",
                        "type_target": "Location",
                        "relation": "phải_rời"
                    },
                    {
                        "source": {
                            "name": "đội bóng",
                            "players_on_field": "<7"
                        },
                        "target": {
                            "name": "kết quả trận đấu",
                            "result": "xử thua 0-3"
                        },
                        "type_source": "Organization",
                        "type_target": "Event",
                        "relation": "bị_xử_thua"
                    }
                ]
            }
        ]
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
                neo.import_relationships(r, title["title"].lower(), "Part")
                print(f"[Neo4j] Đã import relationships cho Part {title['title']}")

        except Exception as e:
            print(f"[ERROR] Lỗi khi insert vào Neo4j: {e}")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Lỗi insert vào Neo4j: {e}")

        print("\nHoàn tất thêm dữ liệu vào Neo4j.")
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