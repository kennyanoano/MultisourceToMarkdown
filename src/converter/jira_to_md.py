import requests
from requests.auth import HTTPBasicAuth
import os
import re
import json

def adf_to_md(adf):
    """
    Convert Atlassian Document Format (ADF) to Markdown.
    """
    md = ""
    # 修正: adfがNoneであるか、'content'キーが存在しない場合に空のリストを使用
    content = adf.get('content', []) if adf else []
    for block in content:
        for elem in block.get('content', []):
            if elem['type'] == 'text':
                text_content = elem.get('text', '')
                text_content = text_content.replace('\\n', '\n')  # Convert \n to newline
                md += text_content
            elif elem['type'] == 'hardBreak':
                md += '\n'
        md += '\n\n'  # Add empty line between paragraphs
    return md

def convert_jira_to_md(file_path):
    try:
        USERNAME = os.environ['MKZ_USER_EMAIL']
        API_TOKEN = os.environ['MKZ_API_KEY']
        JIRA_DOMAIN = os.environ['MKZ_CONFLUENCE_DOMAIN']
    except KeyError as e:
        print(f"Environment variable {e} not set. Please ensure all required environment variables are set.")
        return None, None  # Return two None values to match the expected tuple structure

    # Regular expression to extract the Jira issue key from the file_path
    match = re.search(r'/jira/software/c/projects/.*/issues/(.*)', file_path)
    if match:
        issue_key = match.group(1)
    else:
        print("Invalid file path.")
        return None, None  # Return two None values to match the expected tuple structure

    url = f"https://{JIRA_DOMAIN}.atlassian.net/rest/api/3/issue/{issue_key}"

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

    issue_data = json.loads(response.text)
    summary = issue_data['fields']['summary']
    try:
        description = issue_data['fields']['description']
    except KeyError:
        description = {}  # 修正: 説明がない場合は空の辞書を使用

    # 担当者を取得
    try:
        assignee = issue_data['fields']['assignee']['displayName']
    except (KeyError, TypeError):
        assignee = "notAssigned"  # 担当者が割り当てられていない場合

    # コンポーネントを取得
    try:
        components = [component['name'] for component in issue_data['fields']['components']]
        components_str = ", ".join(components)
    except KeyError:
        components_str = "noComponent"  # コンポーネントが割り当てられていない場合

    # Jira課題データからステータスを取得
    try:
        status = issue_data['fields']['status']['name']
    except KeyError:
        status = "Unknown"  # ステータスが取得できない場合は"Unknown"とする

    # Convert description from ADF to Markdown
    description_md = adf_to_md(description)

    markdown_content = f"## {summary}\n\n{description_md}\n\n**Status:** {status}\n\n**Assignee:** {assignee}\n\n**Components:** {components_str}"

    # Directly return markdown_content and summary
    return markdown_content, summary