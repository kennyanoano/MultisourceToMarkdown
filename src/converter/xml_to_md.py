def convert_xml_to_md(file_path):
    import xml.etree.ElementTree as ET

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Markdown変換の基本的なロジック
        md_content = ""
        for child in root:
            if child.tag == "h1":
                md_content += f"# {child.text}\n\n"
            elif child.tag == "h2":
                md_content += f"## {child.text}\n\n"
            elif child.tag == "p":
                md_content += f"{child.text}\n\n"
            # 他のタグに対する処理もここに追加

        return md_content
    except Exception as e:
        print(f"Error converting XML to Markdown: {e}")
        return ""