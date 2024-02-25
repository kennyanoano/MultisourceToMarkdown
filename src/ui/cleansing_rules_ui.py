import tkinter as tk
from tkinter import ttk
import sys
import os
import glob
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = 1
except (AttributeError, OSError):
    pass  # Windows以外のOS、または対応していないWindowsバージョンでは何もしない

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from converter.cleansing_rules import rules, CleansingRule, apply_cleansing_rule, load_rules, ruleFromText

def get_rule_types():
    from converter.cleansing_rules import rules
    unique_rule_types = set(rule.rule_type for rule in rules)
    return list(unique_rule_types)

class CleansingRulesUI:
    def __init__(self, master):
        self.rulesFromText = []  # インスタンス変数としてrulesFromTextを初期化
        self.load_rules()  # Load rules from sourcerule.txt when the window is opened
        self.master = master
        self.master.title('Cleansing Rules Manager')

        self.frame = ttk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)

        self.rules_listbox = tk.Listbox(self.frame, height=10, width=50)
        self.rules_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.add_button = ttk.Button(self.frame, text='Add Rule', command=self.add_rule_dialog)
        self.add_button.pack(side=tk.LEFT, padx=(0, 10))

        self.edit_button = ttk.Button(self.frame, text='Edit Rule', command=self.edit_rule)
        self.edit_button.pack(side=tk.LEFT, padx=(0, 10))

        self.delete_button = ttk.Button(self.frame, text='Delete Rule', command=self.delete_rule)
        self.delete_button.pack(side=tk.LEFT, padx=(0, 10))

        # Apply ALL ボタン
        self.apply_button = tk.Button(self.frame, text='Apply ALL', command=self.apply_rule, bg='#4CAF50', fg='white')
        self.apply_button.pack(side=tk.LEFT)

        # Tab1 ボタン
        self.apply_to_tab1_button = tk.Button(self.frame, text='Tab1', command=lambda: self.apply_rule_to_tab(1), width=6, bg='#4CAF50', fg='white')
        self.apply_to_tab1_button.pack(side=tk.LEFT)

        # Tab2 ボタン
        self.apply_to_tab2_button = tk.Button(self.frame, text='Tab2', command=lambda: self.apply_rule_to_tab(2), width=6, bg='#4CAF50', fg='white')
        self.apply_to_tab2_button.pack(side=tk.LEFT)

        # Tab 3 ボタン
        self.apply_to_tab3_button = tk.Button(self.frame, text='Tab 3', command=lambda: self.apply_rule_to_tab(3), width=6, bg='#4CAF50', fg='white')
        self.apply_to_tab3_button.pack(side=tk.LEFT)

        self.update_rules_list()

    def load_rules(self):
        load_rules()  # converter.cleansing_rulesモジュールのload_rules関数を呼び出す
        self.rulesFromText = ruleFromText  # グローバルなrulesリストをインスタンス変数にコピー

    def update_rules_list(self):
        self.rules_listbox.delete(0, tk.END)  # 既存のリストをクリア
        for rule in self.rulesFromText:  # self.rulesFromTextの内容をリストボックスに追加
            self.rules_listbox.insert(tk.END, f'{rule.rule_type}: {rule.condition} -> {rule.action}')

    def add_rule(self):
        new_rule = CleansingRule(rule_type, condition, action)
        self.rulesFromText.append(new_rule)
        self.save_rules()

    def edit_rule(self):
        try:
            rule_index = self.rules_listbox.curselection()[0]
            self.edit_rule_dialog(rule_index)
        except IndexError:
            print('Please select a rule to edit.')

    def delete_rule(self):
        try:
            rule_index = self.rules_listbox.curselection()[0]
            del self.rulesFromText[rule_index]  # 選択されたルールをリストから削除
            self.update_rules_list()  # リストボックスの表示を更新
            self.save_rules()  # 変更をファイルに保存
            print(f'Rule at index {rule_index} deleted.')
        except IndexError:
            print('Please select a rule to delete.')

    def apply_rule(self):
        selected_indices = self.rules_listbox.curselection()
        if not selected_indices:  # 何も選択されていない場合
            md_files = glob.glob('converted_md/**/*.md', recursive=True)
            for file_path in md_files:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                for rule in self.rulesFromText:  # すべてのルールを適用
                    file_content = apply_cleansing_rule(rule, file_content)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(file_content)
            print(f'Cleansing applied to {len(md_files)} files using all rules.')
        else:
            try:
                rule_index = selected_indices[0]
                selected_rule = self.rulesFromText[rule_index]
                md_files = glob.glob('converted_md/**/*.md', recursive=True)
                for file_path in md_files:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        file_content = file.read()
                    cleansed_content = apply_cleansing_rule(selected_rule, file_content)
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(cleansed_content)
                print(f'Cleansing applied to {len(md_files)} files using selected rule.')
            except IndexError:
                print('Please select a rule to apply.')

    def apply_rule_to_tab(self, tab_index):
        folder_index = {1: '0', 2: '1', 3: '2'}[tab_index]  # タブのインデックスに応じてフォルダ名を変更
        selected_indices = self.rules_listbox.curselection()
        md_files = glob.glob(f'converted_md/{folder_index}/*.md', recursive=True)

        if not selected_indices:  # 何も選択されていない場合、すべてのルールを適用
            for file_path in md_files:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                for rule in self.rulesFromText:
                    file_content = apply_cleansing_rule(rule, file_content)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(file_content)
            print(f'Cleansing applied to {len(md_files)} files in {folder_index} using all rules.')
        else:
            try:
                for rule_index in selected_indices:
                    selected_rule = self.rulesFromText[rule_index]
                    for file_path in md_files:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            file_content = file.read()
                        cleansed_content = apply_cleansing_rule(selected_rule, file_content)
                        with open(file_path, 'w', encoding='utf-8') as file:
                            file.write(cleansed_content)
                print(f'Cleansing applied to {len(md_files)} files in {folder_index} using selected rules.')
            except IndexError:
                print('Please select a rule to apply.')

    def save_rules(self):
        with open('sourcerule.txt', 'w', encoding='utf-8') as file:  # UTF-8を指定
            for rule in self.rulesFromText:
                condition = rule.condition if rule.condition is not None else 'None'
                action = rule.action if rule.action is not None else 'None'
                file.write(f'{rule.rule_type},{condition},{action}\n')


    def add_rule_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.title('Add New Rule')

        ttk.Label(dialog, text='Rule Type:').grid(row=0, column=0, padx=10, pady=5, sticky='w')

        rule_type_options = get_rule_types()  # ★★★この値がおかしい！

        rule_type_combobox = ttk.Combobox(dialog, values=rule_type_options)
        rule_type_combobox.grid(row=0, column=1, padx=10, pady=5, sticky='we')

        ttk.Label(dialog, text='Condition:').grid(row=1, column=0, padx=10, pady=5, sticky='w')
        condition_entry = ttk.Entry(dialog)
        condition_entry.grid(row=1, column=1, padx=10, pady=5, sticky='we')

        ttk.Label(dialog, text='Action:').grid(row=2, column=0, padx=10, pady=5, sticky='w')
        action_entry = ttk.Entry(dialog)
        action_entry.grid(row=2, column=1, padx=10, pady=5, sticky='we')

        def on_submit():
            rule_type = rule_type_combobox.get()
            condition = condition_entry.get()
            action = action_entry.get()
            self.rulesFromText.append(CleansingRule(rule_type, condition, action))
            self.update_rules_list()
            self.save_rules()  # Save rules to sourcerule.txt immediately after submitting
            print(f'Rule added: {rule_type}, {condition}, {action}')
            dialog.destroy()

        submit_button = ttk.Button(dialog, text='Submit', command=on_submit)
        submit_button.grid(row=3, column=1, padx=10, pady=10, sticky='e')
        dialog.transient(self.master)  # Set to be on top of the main window
        dialog.grab_set()  # Modal
        self.master.wait_window(dialog)  # Wait for the dialog to be destroyed

    def edit_rule_dialog(self, rule_index):
        selected_rule = self.rulesFromText[rule_index]
        dialog = tk.Toplevel(self.master)
        dialog.title('Edit Rule')

        ttk.Label(dialog, text='Rule Type:').grid(row=0, column=0, padx=10, pady=5, sticky='w')
        rule_type_options = get_rule_types()  # 利用可能なルールタイプを取得
        rule_type_combobox = ttk.Combobox(dialog, values=rule_type_options)
        rule_type_combobox.insert(0, selected_rule.rule_type)
        rule_type_combobox.grid(row=0, column=1, padx=10, pady=5, sticky='we')

        ttk.Label(dialog, text='Condition:').grid(row=1, column=0, padx=10, pady=5, sticky='w')
        condition_entry = ttk.Entry(dialog)
        condition_entry.insert(0, selected_rule.condition)
        condition_entry.grid(row=1, column=1, padx=10, pady=5, sticky='we')

        ttk.Label(dialog, text='Action:').grid(row=2, column=0, padx=10, pady=5, sticky='w')
        action_entry = ttk.Entry(dialog)
        action_entry.insert(0, selected_rule.action)
        action_entry.grid(row=2, column=1, padx=10, pady=5, sticky='we')

        def on_submit():
            selected_rule.rule_type = rule_type_combobox.get()
            selected_rule.condition = condition_entry.get()
            selected_rule.action = action_entry.get()
            self.update_rules_list()
            self.save_rules()  # Save rules to sourcerule.txt immediately after submitting
            dialog.destroy()

        submit_button = ttk.Button(dialog, text='Submit', command=on_submit)
        submit_button.grid(row=3, column=1, padx=10, pady=10, sticky='e')
        dialog.transient(self.master)  # Set to be on top of the main window
        dialog.grab_set()  # Modal
        self.master.wait_window(dialog)  # Wait for the dialog to be destroyed

if __name__ == '__main__':
    root = tk.Tk()
    app = CleansingRulesUI(root)
    root.mainloop()
