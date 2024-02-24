def convert_docx_to_md(file_path):
    from docx import Document
    import re

    # ドキュメントを読み込む
    doc = Document(file_path)
    md_content = ""

    # ドキュメント内の各段落をループ処理
    for para in doc.paragraphs:
        text = para.text
        # Markdown形式に変換するロジックをここに追加
        # 例: 太字、斜体、見出し等の変換
        # ここではシンプルにテキストのみを扱う
        md_content += text + "\n\n"

    # 追加の変換ロジックが必要な場合はここに記述

    return md_content