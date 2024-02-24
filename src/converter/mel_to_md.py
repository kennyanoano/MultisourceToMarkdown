def convert_mel_to_md(file_path):
    """
    Convert a MEL file to Markdown format.

    Args:
        file_path (str): The path to the MEL file to convert.

    Returns:
        str: The content of the MEL file in Markdown format.
    """
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()

    md_content = "```mel\n" + content + "\n```"

    return md_content