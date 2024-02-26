import os

def KAno_convert_script(file_path, file_type, tab_index):
    output_dir = os.path.join(os.getcwd(), f"converted_md/{tab_index}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    sourcetextfolder = os.path.join(os.getcwd(), "sources")
    memo_file_path = os.path.join(sourcetextfolder, f"Tab {tab_index + 1}.txt")

    memo_name = ""  # Initialize memo name
    with open(memo_file_path, "r", encoding="utf-8") as memo_file:
        for line in memo_file:
            parts = line.strip().split(',')  # Split the line by comma
            if len(parts) == 2 and file_path.strip() in parts[1].strip():
                memo_name = parts[0]  # Get the memo name
                break  # Exit the loop if the corresponding line is found
    if not memo_name:  # If the memo name is not found
        print(f"Memo name not found for file path {file_path}.")
        return  # End the process

    # Convert memo name to a safe file name
    safe_memo_name = memo_name.replace("?", "_").replace("/", "_")

    # Set the output file path based on the memo name
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
        if "atlassian.net/wiki/" in file_path:  # Atlassian ConfluenceのURLの場合
            # 環境変数の設定を確認し、必要に応じて設定する
            from converter.confluence_to_md import set_env_variables, convert_confluence_to_md
            set_env_variables()  # 環境変数を設定する関数を呼び出す
            markdown_content, title = convert_confluence_to_md(file_path)
        elif "atlassian.net/jira/" in file_path:  # Atlassian jiraのURLの場合
            from converter.confluence_to_md import set_env_variables
            set_env_variables()  # 環境変数を設定する関数を呼び出す
            from converter.jira_to_md import convert_jira_to_md
            markdown_content, title = convert_jira_to_md(file_path)
        else:
            markdown_content, title = KAno_convert_web_to_md(file_path)  # その他のURLの場合、既存の関数を使用
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
        print("type not supported")
    print("done")

def KAno_convert_web_to_md(url):
    import requests
    from bs4 import BeautifulSoup  # BeautifulSoupのインポート
    from html2text import html2text

    response = requests.get(url)
    response.encoding = response.apparent_encoding  # 追加: 文字化け対策
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.title.string.replace(" ", "_").replace("/", "_") if soup.title else "default_title"

    markdown_content = html2text(html_content)

    return markdown_content, title  # Markdown内容とタイトルを返す
