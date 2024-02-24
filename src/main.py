from ui.file_converter_app import FileConverterApp
import os

def KAno_main():
    # tk.Tk() の呼び出しを削除
    app = FileConverterApp()
    # Check and create directories if they don't exist
    for directory in ['sources', 'converted_md']:
        if not os.path.exists(directory):
            os.makedirs(directory)
    app.root.mainloop()  # app.root.mainloop() を使用してイベントループを開始

if __name__ == "__main__":
    KAno_main()