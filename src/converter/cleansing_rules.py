class CleansingRule:
    def __init__(self, rule_type, condition, action):
        self.rule_type = rule_type  # ルールの種類（例：'replace', 'remove_whitespace', 'remove_tag'）
        self.condition = condition  # ルールが適用される条件（例：特定の文字列やパターン）
        self.action = action  # ルールによって実行されるアクション（例：置換する文字列、削除するタグ）

    def __str__(self):
        return f'CleansingRule(type={self.rule_type}, condition={self.condition}, action={self.action})'

# クレンジングルールの例
rules = [
    CleansingRule('replace', 'http://', 'https://'),
    CleansingRule('remove_whitespace', None, None),
    CleansingRule('remove_tag', '<script>', '</script>'),  # ここにカンマを追加
    CleansingRule('remove_before', 'SpecialMojiretsu', 'None'),  # ここにカンマを追加
    CleansingRule('remove_after', 'SpecialMojiretsu2', 'None'),
    CleansingRule('remove_until_newline', 'SpecialMojiretsu2', 'None')   
]

def apply_cleansing_rule(rule, text):
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
        # 特定の文字列から改行までを削除する
        import re
        pattern = re.escape(rule.condition) + '.*?\\n'
        return re.sub(pattern, '', text, flags=re.DOTALL)
    else:
        return text

def load_rules():
    global ruleFromText
    ruleFromText = []
    try:
        with open('sourcerule.txt', 'r', encoding='utf-8') as file:
            for line in file:
                rule_type, condition, action = line.strip().split(',')
                ruleFromText.append(CleansingRule(rule_type, condition if condition != 'None' else None, action if action != 'None' else None))
    except FileNotFoundError:
        with open('sourcerule.txt', 'w', encoding='utf-8') as file:  # sourcerule.txtが存在しない場合は、ファイルを作成する
            pass
    print(f"Loaded {len(ruleFromText)} rules.")  # 読み込んだルールの数をログ出力

load_rules()