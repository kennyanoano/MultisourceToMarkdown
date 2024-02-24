def convert_txt_to_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # ここにMarkdownへの変換ロジックを追加
    return content
