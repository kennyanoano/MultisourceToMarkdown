import openpyxl

def convert_xlsx_to_md(file_path):
    workbook = openpyxl.load_workbook(file_path)
    md_content = ""

    for sheet_name in workbook.sheetnames:
        md_content += f"## {sheet_name}\n\n"  # シート名を見出しとして追加

        sheet = workbook[sheet_name]
        for row in sheet.iter_rows(values_only=True):
            # Markdownのテーブル形式に変換
            md_row = "| " + " | ".join([str(cell) if cell is not None else "" for cell in row]) + " |"
            md_content += md_row + "\n"
        md_content += "\n"  # シート間に空行を追加

    return md_content