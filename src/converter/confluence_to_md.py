import tkinter as tk
from tkinter import simpledialog
import platform
if platform.system() == 'Windows':
    import winreg as reg
else:
    print ("Not Windows")
import os
import re
import requests
import json
from requests.auth import HTTPBasicAuth
import html2text

def set_user_env_variable(name, value):
    if platform.system() == 'Windows':
        # ユーザー環境変数をレジストリに設定
        key_path = 'Environment'
        try:
            with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_ALL_ACCESS) as key:
                reg.SetValueEx(key, name, 0, reg.REG_SZ, value)
        except Exception as e:
            print(f"Failed to set environment variable: {e}")
    else:
        print("This script cannot set environment variables on non-Windows systems.")

def set_env_variables():
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを表示しない

    user_email = os.environ.get('MKZ_USER_EMAIL')
    api_key = os.environ.get('MKZ_API_KEY')
    confluence_domain = os.environ.get('MKZ_CONFLUENCE_DOMAIN')
    print ("デバッグ")
    print("MKZ_USER_EMAIL:", os.environ.get('MKZ_USER_EMAIL'))

    if not user_email or not api_key or not confluence_domain:
        user_email = simpledialog.askstring("Input", "Please enter your email address:", parent=root)
        api_key = simpledialog.askstring("Input", "Please enter your API key:", parent=root)
        confluence_domain = simpledialog.askstring("Input", "Please enter your Confluence domain:", parent=root)

        if user_email and api_key and confluence_domain:
            # 環境変数を設定
            set_user_env_variable('MKZ_USER_EMAIL', user_email)
            set_user_env_variable('MKZ_API_KEY', api_key)
            set_user_env_variable('MKZ_CONFLUENCE_DOMAIN', confluence_domain)
            print("Environment variables set successfully.")
        else:
            print("No input provided.")

def convert_confluence_to_md(file_path):
    try:
        USERNAME = os.environ['MKZ_USER_EMAIL']
        API_TOKEN = os.environ['MKZ_API_KEY']
        CONFLUENCE_DOMAIN = os.environ['MKZ_CONFLUENCE_DOMAIN']
    except KeyError as e:
        print(f"Environment variable {e} not set. Please ensure all required environment variables are set.")
        return None, None  # Return two None values to match the expected tuple structure

    # ファイルパスからIDを抽出する正規表現
    match = re.search(r'/pages/(\d+)/', file_path)
    if match:
        ID_get_from_filepath = match.group(1)
    else:
        print("Invalid file path.")
        return None, None  # Return two None values to match the expected tuple structure

    PAGE_ID = ID_get_from_filepath

    url = "https://" + CONFLUENCE_DOMAIN + ".atlassian.net/wiki/rest/api/content/{}?expand=body.storage".format(PAGE_ID)
    auth = HTTPBasicAuth(USERNAME, API_TOKEN)

    headers = {
        "Accept": "application/json"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )

    page_content = json.loads(response.text)
    html_content = page_content['body']['storage']['value']
    title = page_content['title']

    # HTMLをマークダウンに変換
    h = html2text.HTML2Text()
    h.ignore_links = False  # リンクを無視しない
    markdown_content = h.handle(html_content)

    return markdown_content, title

if __name__ == "__main__":
    set_env_variables()

