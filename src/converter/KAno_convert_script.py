import os

def KAno_convert_script(file_path, file_type, tab_index):
    output_dir = os.path.join(os.getcwd(), f"converted_md/{tab_index}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    sourcetextfolder = os.path.join(os.getcwd(), "sources")
    memo_file_path = os.path.join(sourcetextfolder, f"Tab {tab_index + 1}.txt")

    memo_name = ""  # メモ名の初期化
    with open(memo_file_path, "r", encoding="utf-8") as memo_file:
        for line in memo_file:
            parts = line.strip().split(',')  # 行をカンマで分割
            if len(parts) == 2 and file_path.strip() in parts[1].strip():
                memo_name = parts[0]  # メモ名を取得
                break  # 該当する行が見つかったらループを抜ける
    if not memo_name:  # メモ名が見つからなかった場合
        print(f"ファイルパス {file_path} に対応するメモ名が見つかりませんでした。")
        return  # 処理を終了

    # メモ名を安全なファイル名に変換
    safe_memo_name = memo_name.replace("?", "_").replace("/", "_")

    # 出力ファイルパスをメモ名に基づいて設定
    output_file_path = os.path.join(output_dir, f"{safe_memo_name}.md")

    conversion_dict = {
        "html": {
            "module_name": "html_to_md",
            "function_name": "convert_html_to_md"
        },
        "pdf": {
            "module_name": "pdf_to_md",
            "function_name": "convert_pdf_to_md"
        },
        "txt": {
            "module_name": "txt_to_md",
            "function_name": "convert_txt_to_md"
        },
        "docx": {
            "module_name": "docx_to_md",
            "function_name": "convert_docx_to_md"
        },
        "mel": {
            "module_name": "mel_to_md",
            "function_name": "convert_mel_to_md"
        },
        "py": {
            "module_name": "py_to_md",
            "function_name": "convert_py_to_md"
        },
        "xlsx": {
            "module_name": "xlsx_to_md",
            "function_name": "convert_xlsx_to_md"
        },
        "xml": {
            "module_name": "xml_to_md",
            "function_name": "convert_xml_to_md"
        }
    }

    if file_path.startswith("https://"):  # URLの場合
        markdown_content, title = KAno_convert_web_to_md(file_path)  # タプルを受け取る
        with open(output_file_path, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)  # 文字列のみを渡す
    elif file_type in conversion_dict:  # ここでfile_typeがconversion_dictに含まれているかチェック
        # モジュールのフルパスを取得
        module_path = "converter." + conversion_dict[file_type]["module_name"]
        module = __import__(module_path, fromlist=[conversion_dict[file_type]["function_name"]])
        convert_function = getattr(module, conversion_dict[file_type]["function_name"])
        markdown_content = convert_function(file_path)
        # 変換したMarkdownをファイルに保存
        with open(output_file_path, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)
    else:
        print("サポートされていないファイルタイプです。")
    print("変換処理が完了しました。")

def KAno_convert_web_to_md(url):
    import requests
    from bs4 import BeautifulSoup  # BeautifulSoupのインポート
    from html2text import html2text

    # URLからHTMLを取得。文字化けを防ぐために、レスポンスのエンコーディングを明示的に指定します。
    response = requests.get(url)
    response.encoding = response.apparent_encoding  # 追加: 文字化け対策
    html_content = response.text

    # BeautifulSoupを使用してHTMLを解析し、タイトルを取得
    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.title.string.replace(" ", "_").replace("/", "_") if soup.title else "default_title"

    # HTMLをMarkdownに変換
    markdown_content = html2text(html_content)

    return markdown_content, title  # Markdown内容とタイトルを返す
