def convert_docx_to_md(file_path):
    from docx import Document
    #import re

    doc = Document(file_path)
    md_content = ""

    for para in doc.paragraphs:
        text = para.text
        # Markdown形式に変換するロジックをここに追加
        # 例: 太字、斜体、見出し等の変換
        # ここではシンプルにテキストのみを扱う
        md_content += text + "\n\n"

    return md_content