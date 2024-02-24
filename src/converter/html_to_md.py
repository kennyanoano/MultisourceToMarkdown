import html2text
import os

def convert_html_to_md(html_file_path):
    # ファイルの存在を確認
    if not os.path.exists(html_file_path):
        print(f"指定されたファイルが見つかりません: {html_file_path}")
        return None

    try:
        # AIによるとあまりいい処理ではない・HTMLファイルを読み込む際に、'utf-8'以外のエンコーディングも考慮する必要がある場合、
        # まずは'utf-8'で試し、UnicodeDecodeErrorが発生したら'cp932' (Windowsの場合) など、
        # 他のエンコーディングで試すようにします。
        try:
            with open(html_file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
        except UnicodeDecodeError:
            with open(html_file_path, 'r', encoding='cp932') as file:  # 日本でよく使われるエンコーディング
                html_content = file.read()

        # html2textを使用してHTMLをMarkdownに変換
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = False
        markdown_content = text_maker.handle(html_content)
        return markdown_content
    except Exception as e:
        print(f"ファイルの読み込みまたは変換中にエラーが発生しました: {e}")
        return None