import tkinter as tk
from tkinter import ttk
import sys
import os
import tkinter.simpledialog
import json
import ctypes
from tkinterdnd2 import DND_FILES, TkinterDnD
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except AttributeError:
    pass
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)
config_path = os.path.join(project_root, "configs", "application_config.json")
sources_dir = os.path.join(project_root, "sources")
converted_md_dir = os.path.join(project_root, "converted_md")
from converter.KAno_convert_script import KAno_convert_script as KAno_run_conversion
from ui.cleansing_rules_ui import CleansingRulesUI
from ui.source_manager import SourceManager
class FileConverterApp:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title("File Converter")
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[20, 8])
        self.notebook = ttk.Notebook(self.root)
        config = self.load_config()
        tab_names = config.get("tab_names", ["Tab 1", "Tab 2", "Tab 3"])
        self.tabs = []
        self.source_listboxes = {}
        for i, name in enumerate(tab_names):
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=name)
            self.setup_tab(tab, i)
            self.tabs.append(tab)
            self.source_listboxes[i] = self.setup_tab(tab, i)
        self.notebook.pack(expand=True, fill='both')
        self.notebook.bind('<Double-1>', self.rename_tab)
        self.source_manager = SourceManager()
        for i in range(len(tab_names)):  # Update source list for all tabs
            self.update_source_list(i)
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)
    def setup_tab(self, tab, tab_index):
        main_frame = ttk.Frame(tab, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        source_listbox = self.setup_common_ui_components(main_frame, tab_index)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        return self.setup_common_ui_components(main_frame, tab_index)
    def setup_common_ui_components(self, main_frame, tab_index):
        source_name_label = ttk.Label(main_frame, text="Memo:")
        source_name_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        source_name_entry = ttk.Entry(main_frame, width=50)
        source_name_entry.grid(row=0, column=1, sticky=tk.E, padx=5, pady=5)
        source_path_label = ttk.Label(main_frame, text="Source Path:")
        source_path_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        source_path_entry = ttk.Entry(main_frame, width=50)
        source_path_entry.grid(row=1, column=1, sticky=tk.E, padx=5, pady=5)
        save_button = ttk.Button(main_frame, text="Save Source", command=lambda: self.KAno_save_source(tab_index))
        save_button.grid(row=2, column=1, sticky=tk.E, padx=5, pady=5)
        source_list_label = ttk.Label(main_frame, text="Sources:")
        source_list_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        source_listbox = tk.Listbox(main_frame, height=10, width=50)
        source_listbox.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        source_listbox.bind('<1>', self.KAno_toggle_selection)
        delete_button = ttk.Button(main_frame, text="Delete Source", command=self.delete_source)
        delete_button.grid(row=4, column=1, sticky=tk.E, padx=5, pady=5)
        convert_button = ttk.Button(main_frame, text="Convert", command=self.KAno_convert_source)
        convert_button.grid(row=5, column=1, sticky=tk.E, padx=5, pady=5)
        open_folder_button = ttk.Button(main_frame, text="Open MD Folder", command=self.open_md_folder)
        open_folder_button.grid(row=6, column=0, sticky=tk.E, padx=5, pady=5)
        cleansing_rules_button = ttk.Button(main_frame, text="Cleansing Rules", command=self.open_cleansing_rules_ui)
        cleansing_rules_button.grid(row=6, column=1, sticky=tk.E, padx=5, pady=5)
        if not hasattr(self, 'source_entries'):
            self.source_entries = {}
        self.source_entries[tab_index] = {
            "source_name_entry": source_name_entry,
            "source_path_entry": source_path_entry,
            "save_button": save_button
        }
        return source_listbox
    def open_md_folder(self):
        import subprocess
        import platform
        tab_index = self.notebook.index("current")
        folder_path = os.path.join(converted_md_dir, str(tab_index))
        print(folder_path)
        if platform.system() == "Windows":
            subprocess.Popen(f'explorer "{folder_path}"')
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", folder_path])
        else:  # Linux and others
            subprocess.Popen(["xdg-open", folder_path])
    def rename_tab(self, event=None):
        tab_index = self.notebook.index("@%d,%d" % (event.x, event.y))
        new_name = tkinter.simpledialog.askstring("Rename Tab", "New tab name:")
        if new_name:
            self.notebook.tab(tab_index, text=new_name)
            self.save_tab_names()
            old_name = list(self.source_listboxes.keys())[tab_index]
            self.source_listboxes[new_name] = self.source_listboxes.pop(old_name)
            self.source_entries[new_name] = self.source_entries.pop(old_name)
    def save_tab_names(self):
        tab_names = [self.notebook.tab(i, "text") for i in range(self.notebook.index("end"))]
        config = {"tab_names": tab_names}
        self.save_config(config)
    def save_config(self, config):
        with open(config_path, "w") as config_file:
            json.dump(config, config_file, indent=4)
    def load_config(self):
        try:
            with open(config_path, "r") as config_file:
                config = json.load(config_file)
                return config
        except FileNotFoundError:
            return {}
    def KAno_process_source_name(self, source_name):
        if source_name.startswith('"') and source_name.endswith('"'):
            return source_name[1:-1]
        return source_name
    def KAno_save_source(self, tab_index):
        entries = self.source_entries[tab_index]
        source_name = entries["source_name_entry"].get()
        source_name = self.KAno_process_source_name(source_name)
        source_path = entries["source_path_entry"].get()
        self.source_manager.add_or_update_source(tab_index, source_name, source_path)
        self.update_source_list(tab_index)
        print(f"Source saved: {source_name}, {source_path}")
    def KAno_toggle_selection(self, event=None):
        tab_index = self.notebook.index("current")
        current_listbox = self.source_listboxes[tab_index]
        current_selection = current_listbox.curselection()
        if current_selection:
            clicked_index = current_listbox.nearest(event.y)
            if clicked_index in current_selection:
                current_listbox.selection_clear(clicked_index)
            else:
                self.KAno_enter_edit_mode(clicked_index, tab_index)
        else:
            clicked_index = current_listbox.nearest(event.y)
            self.KAno_enter_edit_mode(clicked_index, tab_index)
    def KAno_enter_edit_mode(self, clicked_index, tab_index):
        self.root.after(50, lambda: self.KAno_delayed_edit_mode(clicked_index, tab_index))
    def KAno_delayed_edit_mode(self, clicked_index, tab_index):
        try:
            current_listbox = self.source_listboxes[tab_index]
            selection = current_listbox.curselection()[0]
            source_name = current_listbox.get(selection)
            source_path = self.source_manager.load_sources(tab_index).get(source_name, "")
            entries = self.source_entries[tab_index]
            source_name_entry = entries["source_name_entry"]
            source_path_entry = entries["source_path_entry"]
            source_name_entry.delete(0, tk.END)
            source_name_entry.insert(0, source_name)
            source_path_entry.delete(0, tk.END)
            source_path_entry.insert(0, source_path)
            save_button = entries["save_button"]
            save_button.config(text="Finish Edit", command=lambda: self.KAno_update_source(tab_index))
        except IndexError:
            print("not selected")
    def delete_source(self):
        tab_index = self.notebook.index("current")
        current_listbox = self.source_listboxes[tab_index]
        try:
            selection = current_listbox.curselection()[0]
            source_name = current_listbox.get(selection)
            self.source_manager.delete_source(tab_index, source_name)
            self.update_source_list(tab_index)
        except IndexError:
            print("No source selected for deletion.")
    def edit_source(self):
        tab_index = self.notebook.index("current")
        current_listbox = self.source_listboxes[tab_index]
        try:
            selection = current_listbox.curselection()[0]
            source_name = current_listbox.get(selection)
            source_path = self.source_manager.load_sources(tab_index).get(source_name, "")
            entries = self.source_entries[tab_index]
            source_name_entry = entries["source_name_entry"]
            source_path_entry = entries["source_path_entry"]
            source_name_entry.delete(0, tk.END)
            source_name_entry.insert(0, source_name)
            source_path_entry.delete(0, tk.END)
            source_path_entry.insert(0, source_path)
            save_button = entries["save_button"]
            save_button.config(text="Update Source", command=lambda: self.KAno_update_source(tab_index))
        except IndexError:
            print("not selected")
    def KAno_update_source(self, tab_index):
        current_listbox = self.source_listboxes[tab_index]
        original_source_name = current_listbox.get(tk.ACTIVE)  # アクティブなリストアイテム（編集前の名前）を取得
        entries = self.source_entries[tab_index]
        source_name = entries["source_name_entry"].get()
        source_name = self.KAno_process_source_name(source_name)  # ソース名の処理を追加
        source_path = entries["source_path_entry"].get()
        self.source_manager.delete_source(tab_index, original_source_name)  # 修正前の名前をリストから削除
        self.source_manager.add_or_update_source(tab_index, source_name, source_path)
        self.update_source_list(tab_index)
        save_button = entries["save_button"]
        save_button.config(text="Save Source", command=lambda: self.KAno_save_source(tab_index))
    def KAno_convert_source(self):
        tab_index = self.notebook.index("current")
        current_listbox = self.source_listboxes[tab_index]
        items = current_listbox.get(0, tk.END)
        if not items:
            print("no source")
            return
        try:
            selected_items = current_listbox.curselection()
            if not selected_items:  #
                selected_items = range(len(items))
            for i in selected_items:
                source_name = current_listbox.get(i)
                source_path = self.source_manager.load_sources(tab_index).get(source_name, "")
                if source_path:
                    if source_path.startswith('"') and source_path.endswith('"'):
                        source_path = source_path[1:-1]
                    if source_path.startswith("https://"):  #
                        KAno_run_conversion(source_path, "web", tab_index)  # 'web'として扱う
                    else:
                        KAno_run_conversion(source_path, source_path.split('.')[-1], tab_index)
                else:
                    print(f"path not found: {source_name}")
        except IndexError:
            print("not selected")
    def update_source_list(self, tab_index):
        try:
            source_listbox = self.source_listboxes[tab_index]
            source_listbox.delete(0, 'end')  # Clear the current list
            sources = self.source_manager.load_sources(tab_index)
            for name in sources.keys():
                source_listbox.insert('end', name)
        except KeyError as e:
            print(f"Error: No source listbox found for tab index '{tab_index}'. This tab may have been renamed or removed.")
            print(f"KeyError: {e}")  #
    def open_cleansing_rules_ui(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Cleansing Rules")
        CleansingRulesUI(new_window)
    def on_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        for f in files:
            self.KAno_add_dropped_source(f)
    def KAno_add_dropped_source(self, file_path):
        tab_index = self.notebook.index("current")
        source_name = os.path.basename(file_path)
        self.source_manager.add_or_update_source(tab_index, source_name, file_path)
        self.update_source_list(tab_index)