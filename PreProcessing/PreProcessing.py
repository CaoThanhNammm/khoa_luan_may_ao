import ast
import json
import py_vncorenlp
from dotenv import load_dotenv
load_dotenv()
import re
import os
import unicodedata

# Global VnCoreNLP instance
save_dir = '/root/vncorenlp'
# save_dir = r"C:\Users\Nam\Desktop\vncorenlp"
VnCoreNLP_INSTANCE = None

def get_vncorenlp_instance():
    global VnCoreNLP_INSTANCE
    if VnCoreNLP_INSTANCE is None:
        VnCoreNLP_INSTANCE = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir=save_dir)
    return VnCoreNLP_INSTANCE

class PreProcessing:
    def __init__(self):
        self.vncorenlp = get_vncorenlp_instance()


    def string_to_json(self, text):
        removed_special = text.replace("```", "").replace("json", "")
        removed_special = removed_special.strip()
        return ast.literal_eval(removed_special)

    def text_preprocessing_vietnamese(self, text):
        root_dir = os.path.dirname(os.path.abspath(__file__))  # Thư mục chứa file Python hiện tại
        root_dir = os.path.dirname(root_dir)  # Lên thư mục cha
        stopwords_path = os.path.join(root_dir, 'vietnamese_stopwords.txt')

        with open(stopwords_path, 'r', encoding='utf-8') as f:
            stop_words = set(f.read().splitlines())

        # 1. Chuẩn hóa unicode
        text = self.normalize_unicode(text, 'NFC')

        # 2. Chuyển thành chữ thường
        text = text.lower()

        # 3. Loại bỏ ký tự đánh số/thứ tự ở đầu dòng (ví dụ: "1. ", "a) ")
        #    (?m) bật chế độ multiline, ^ khớp đầu dòng, \s* để bỏ khoảng trắng đầu dòng nếu có
        text = re.sub(r'(?m)^\s*(?:\d+\.|[a-z]\))\s*', '', text)

        # 4. Xóa tất cả các ký tự đặc biệt
        text = re.sub(r'[^\w\s\n]', '', text)

        # 5. Xóa khoảng trắng thừa
        text = text.strip()

        # 6. word segment
        try:
            output = self.vncorenlp.word_segment(text)  # output là một list
            output = output[0].split(' ')
            # 7. Loại bỏ stop words trực tiếp từ list
            filtered_words = [word for word in output if word not in stop_words]
            result_string = ' '.join(filtered_words)
            return result_string
        except:
            output = ''

        return text

    def normalize_unicode(self, text, form='NFC'):
        return unicodedata.normalize(form, text)