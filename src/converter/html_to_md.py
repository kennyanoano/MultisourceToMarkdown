import html2text
import os

def convert_html_to_md(html_file_path):
    if not os.path.exists(html_file_path):
        print(f"File not found: {html_file_path}")
        return None

    try:
        # Attempt to read the HTML file using 'utf-8' encoding first, then try other encodings like 'cp932' (for Windows) if UnicodeDecodeError occurs.
        try:
            with open(html_file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
        except UnicodeDecodeError:
            with open(html_file_path, 'r', encoding='cp932') as file:  # Common encoding in Japan
                html_content = file.read()

        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = False
        markdown_content = text_maker.handle(html_content)
        return markdown_content
    except Exception as e:
        print(f"Error occurred during file reading or conversion: {e}")
        return None