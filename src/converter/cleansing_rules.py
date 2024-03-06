import os

class CleansingRule:
    def __init__(self, rule_type, condition, action):
        self.rule_type = rule_type  # ルールの種類（例：'replace', 'remove_whitespace', 'remove_tag'）
        self.condition = condition  # ルールが適用される条件（例：特定の文字列やパターン）
        self.action = action  # ルールによって実行されるアクション（例：置換する文字列、削除するタグ）

    def __str__(self):
        return f'CleansingRule(type={self.rule_type}, condition={self.condition}, action={self.action})'

    @staticmethod
    def split_file_by_tokens(file_path, token_limit=500):
        import os
        # ファイル名に既に分割パターンが含まれているかチェック
        if '_partMKZ_' in file_path:
            print(f"File {file_path} is already a part of a split. Skipping.")
            return f"File {file_path} is already a part of a split. Skipping."

        # ファイルサイズをチェック
        if os.path.getsize(file_path) < token_limit * 10:
            print("デバッグ")
            print(file_path)
            return f"File {file_path} is too small to split."

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        tokens = content.split()
        # 元のファイル名から最後の .md 拡張子を取り除く
        base_file_path = file_path.rsplit('.md', 1)[0]
        for i in range(0, len(tokens), token_limit):
            part_tokens = tokens[i:i+token_limit]
            part_content = ' '.join(part_tokens)
            part_file_path = f"{base_file_path}_partMKZ_{i//token_limit}.md"
            with open(part_file_path, 'w', encoding='utf-8') as part_file:
                part_file.write(part_content)
        os.remove(file_path)
        return f"File {file_path} split into parts and saved as Markdown files."

rules = [
    CleansingRule('replace', 'http://', 'https://'),
    CleansingRule('remove_whitespace', None, None),
    CleansingRule('remove_tag', '<script>', '</script>'),
    CleansingRule('remove_before', 'SpecialMojiretsu', 'None'),
    CleansingRule('remove_after', 'SpecialMojiretsu2', 'None'),
    CleansingRule('remove_until_newline', 'SpecialMojiretsu2', 'None'),
    CleansingRule('remove_empty_lines', None, None)
    #CleansingRule('split_file_by_tokens', None, None),  # ファイル分割処理をルールとして追加  #うまくいっていない partMKZが入っていたら処理しないようにしたいのだができてない
]

def apply_cleansing_rule(rule, text, file_path=None):
    if rule.rule_type == 'replace':
        return text.replace(rule.condition, rule.action)
    elif rule.rule_type == 'remove_whitespace':
        return ''.join(text.split())
    elif rule.rule_type == 'remove_tag':
        import re
        tag_pattern = re.escape(rule.condition) + '.*?' + re.escape(rule.action)
        return re.sub(tag_pattern, '', text, flags=re.DOTALL)
    elif rule.rule_type == 'remove_before':
        return text.split(rule.condition, 1)[-1] if rule.condition in text else text
    elif rule.rule_type == 'remove_after':
        return text.split(rule.condition, 1)[0] if rule.condition in text else text
    elif rule.rule_type == 'remove_until_newline':
        import re
        pattern = re.escape(rule.condition) + '.*?\\n'
        return re.sub(pattern, '', text, flags=re.DOTALL)
    elif rule.rule_type == 'remove_empty_lines':
        import re
        return re.sub(r'^\s*$\n', '', text, flags=re.MULTILINE)  # 空っぽの行を削除
    elif rule.rule_type == 'split_file_by_tokens':
        if file_path:  # ファイルパスが提供されている場合のみ分割を実行
            return CleansingRule.split_file_by_tokens(file_path)
        else:
            print("File path is required for 'split_file_by_tokens' rule.")
            return text
    else:
        return text


def load_rules():
    global ruleFromText
    ruleFromText = []
    # プロジェクトのルートディレクトリに基づいてファイルパスを設定（修正前：base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))）
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_path = os.path.join(base_dir, 'sourcerule.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                rule_type, condition, action = line.strip().split(',')
                ruleFromText.append(CleansingRule(rule_type, condition if condition != 'None' else None, action if action != 'None' else None))
    except FileNotFoundError:
        with open(file_path, 'w', encoding='utf-8') as file:  # ファイルが存在しない場合は、正しいパスでファイルを作成する
            pass
    print(f"Loaded {len(ruleFromText)} rules.")

load_rules()