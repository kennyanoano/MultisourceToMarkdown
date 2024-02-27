from ui.file_converter_app import FileConverterApp
import os

def KAno_main():
    # tk.Tk() の呼び出しを削除
    app = FileConverterApp()
    # Get the absolute path of the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Check and create directories if they don't exist, using absolute paths
    for directory in ['sources', 'converted_md']:
        abs_directory_path = os.path.join(project_root, directory)
        if not os.path.exists(abs_directory_path):
            os.makedirs(abs_directory_path)
    app.root.mainloop()  # app.root.mainloop() を使用してイベントループを開始

if __name__ == "__main__":
    KAno_main()