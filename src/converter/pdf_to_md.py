import pdfminer
from pdfminer.high_level import extract_text
import markdownify

def convert_pdf_to_md(pdf_file_path):
    # PDFからテキストを抽出
    extracted_text = KAno_extract_text_from_pdf(pdf_file_path)
    
    # 抽出したテキストをMarkdownに変換
    output = markdownify.markdownify(extracted_text, heading_style="ATX")
    
    return output

def KAno_extract_text_from_pdf(pdf_file_path):
    # PDFファイルからテキストを取得するためのコード
    return extract_text(pdf_file_path)