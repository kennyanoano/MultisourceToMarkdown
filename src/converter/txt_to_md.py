def convert_txt_to_md(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        # UTF-8以外のエンコーディングで再試行するか、エラーメッセージを表示
        try:
            with open(file_path, 'r', encoding='shift_jis') as file:
                content = file.read()
        except UnicodeDecodeError as e:
            return f"エンコーディングの問題が発生しました: {e}"
    # ここにMarkdownへの変換ロジックを追加
    return content
