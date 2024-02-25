import requests
from requests.auth import HTTPBasicAuth
import os
import re
import json

def convert_jira_to_md(file_path):
    try:
        USERNAME = os.environ['MKZ_USER_EMAIL']
        API_TOKEN = os.environ['MKZ_API_KEY']
        JIRA_DOMAIN = os.environ['MKZ_CONFLUENCE_DOMAIN']
    except KeyError as e:
        print(f"Environment variable {e} not set. Please ensure all required environment variables are set.")
        return None, None  # Return two None values to match the expected tuple structure

    # file_pathからJiraの課題キーを抽出する正規表現
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
    # Assuming you want to extract the issue's summary and description for markdown
    # Adjust the keys based on your Jira's response structure
    summary = issue_data['fields']['summary']
    try:
        description = issue_data['fields']['description']
    except KeyError:
        description = "No description provided."

    # 現在のステータスを取得
    status = issue_data['fields']['status']['name']

    markdown_content = f"## {summary}\n\n{description}\n\n**Status:** {status}"

    return markdown_content, summary