def convert_mel_to_md(file_path):
    """
    Convert a MEL file to Markdown format., trying Shift_JIS encoding first, then falling back to UTF-8 if necessary.
    Args:
        file_path (str): The path to the MEL file to convert.
    Returns:
        str: Thecontent of the MEL file in Markdown format.
    """
    try:
        with open(file_path, 'r', encoding='shift_jis') as file:
            content = file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            content = file.read()

    md_content = "```mel\n" + content + "\n```"

    return md_content