# MultiSourceMD

MultiSourceMD is an AI-assisted tool that converts various source formats into Markdown (MD). It supports formats like HTML, PDF, TXT, docx, mel, py, xlsx, and xml. The tool also compresses MD files into ZIP format and allows post-processing rules to clean the MD files.

## Supported Formats

- HTML, PDF, TXT, docx, mel, py, xlsx, xml

## Setup

1. Ensure Python is installed.
2. Clone the repository.
3. Run `pip install -r requirements.txt` in the project directory.

## Usage

Execute `MultiSourceToMakdown.bat`

## Features

- **Source Management**: Add, edit, and convert sources (files or URLs) to MD.
- **Cleansing Rules**: Set rules to clean text before conversion, such as replacing strings, removing whitespace/tags, and more.

## Modifying

- To add conversion formats, modify `KAno_convert_script.py` and add `format_to_md.py`.
- To add cleansing rules, modify `cleansing_rules.py`.

## License

MIT License


[日本語版はこちら](README_ja.md)