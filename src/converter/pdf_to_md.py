import pdfminer
from pdfminer.high_level import extract_text
import markdownify
#import re

def convert_pdf_to_md(pdf_file_path):
    extracted_text = KAno_extract_text_from_pdf(pdf_file_path)

    # NULL文字を除去
    cleaned_text = extracted_text.replace('\x00', '')

    # バイナリデータと思われる非ASCII文字を除去（必要に応じて）
    #cleaned_text = re.sub(r'[^\x00-\x7F]+', ' ', cleaned_text)

    output = markdownify.markdownify(cleaned_text, heading_style="ATX")

    # UTF-8エンコーディングでファイルを保存
    with open(pdf_file_path.replace('.pdf', '.md'), 'w', encoding='utf-8') as md_file:
        md_file.write(output)

    return output

def KAno_extract_text_from_pdf(pdf_file_path):
    #
    return extract_text(pdf_file_path)