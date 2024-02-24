# This script converts Python files to Markdown format
def convert_py_to_md(file_path):
    """
    Convert a Python file to Markdown format.

    Args:
        file_path (str): The path to the Python file to convert.

    Returns:
        str: The content of the Python file in Markdown format.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Assuming the conversion logic is similar to txt_to_md.py
    # This is a placeholder for the actual conversion logic
    md_content = "```python\n" + content + "\n```"

    return md_content
