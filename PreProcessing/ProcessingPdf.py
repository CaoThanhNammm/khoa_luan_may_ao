from io import BytesIO

from dotenv import load_dotenv
load_dotenv()
import pdfplumber
import os


class PDF:
    def __init__(self, s3, pdf_path, bucket_name, key):
        self.pdf_path = pdf_path  # Đường dẫn tới 1 file PDF
        self.s3 = s3

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

    def read_chunks(self):
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

    def set_path(self, path):
        self.pdf_path = path

    def set_bucket_name(self, bucket_name):
        self.bucket_name = bucket_name

    def set_key(self, key):
        self.key = key


