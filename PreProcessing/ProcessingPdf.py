import ast
from io import BytesIO

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

from LLM import prompt
from LLM.GPT import GPT

load_dotenv()
import pdfplumber
import os


class PDF:
    def __init__(self, s3, pdf_path, bucket_name, key):
        self.pdf_path = pdf_path  # Đường dẫn tới 1 file PDF
        self.s3 = s3

        self.gpt_chunk = GPT()
        self.gpt_title = GPT()
        self.gpt_content = GPT()

    def read_chunks_stsv(self, footer_height=40):
        all_pages_text = []

        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                num_pages = len(pdf.pages)
                start_page = 9
                end_page = num_pages - 2

                for i in range(start_page, end_page + 1, 3):
                    group_text = []

                    for j in range(i, min(i + 3, end_page + 1)):
                        page = pdf.pages[j]
                        page_height = page.height

                        cropped_page = page.within_bbox(
                            (0, 0, page.width, page_height - footer_height)
                        )
                        text = cropped_page.extract_text()
                        if text:
                            group_text.append(text)

                    if group_text:
                        all_pages_text.append('\n'.join(group_text))
        except Exception as e:
            print(f"Lỗi khi xử lý file {self.pdf_path}: {e}")

        return all_pages_text

    def read_content(self):
        all_pages_text = []

        response = self.s3.get_object(Bucket=self.bucket_name, Key=self.key)
        file_stream = BytesIO(response['Body'].read())

        try:
            with pdfplumber.open(file_stream) as pdf:
                num_pages = len(pdf.pages)

                for i in range(0, num_pages, 2):
                    group_text = []

                    for j in range(i, min(i + 2, num_pages)):
                        page = pdf.pages[j]
                        text = page.extract_text()
                        if text:
                            group_text.append(text)

                    if group_text:
                        all_pages_text.append('\n'.join(group_text))
        except Exception as e:
            print(f"Lỗi khi xử lý file {self.pdf_path}: {e}")

        return all_pages_text

    def create_chunk(self, sentences):
        chunks = []
        for idx, s in enumerate(sentences):
            prompt_template = PromptTemplate(
                input_variables=["sentence"],
                template=prompt.chunking()
            )
            formatted_prompt = prompt_template.format(sentence=s)
            chunk = self.gpt_chunk.ask(formatted_prompt).replace("```", "").replace("```json", "")
            chunk = ast.literal_eval(chunk)
            chunks.append(chunk)

        all_paragraphs = []

        # Tạo mảng các paragraph
        for chunk in chunks:
            for key, content in chunk.items():
                all_paragraphs.append(content)

        return all_paragraphs

    def create_title(self, sentences):
        titles = []
        for i, s in enumerate(sentences):
            prompt_template = PromptTemplate(
                input_variables=["sentence"],
                template=prompt.create_title()
            )
            formatted_prompt = prompt_template.format(sentence=s)

            title_json = self.gpt_title.ask(formatted_prompt).replace("```", "").replace("json", "")
            titles.append(title_json)

        return titles

    def create_nodes(self, sentences):
        entities_relationship = []

        for i, s in enumerate(sentences):
            prompt_template = PromptTemplate(
                input_variables=["sentence"],
                template=prompt.extract_entities_relationship_from_text()
            )
            formatted_prompt = prompt_template.format(sentence=s)

            entities_relationship_json = self.gpt_title.ask(formatted_prompt).replace("```", "").replace("json", "")
            entities_relationship.append(entities_relationship_json)

        return entities_relationship

    def set_path(self, path):
        self.pdf_path = path

    def set_bucket_name(self, bucket_name):
        self.bucket_name = bucket_name

    def set_key(self, key):
        self.key = key
