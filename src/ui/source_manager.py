import os

class SourceManager:
    def __init__(self, filepath=None):
        if filepath is None:
            # プロジェクトのルートディレクトリを取得
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            # ルートディレクトリにある 'sources' フォルダへの絶対パスを設定
            filepath = os.path.join(project_root, "sources")
        self.filepath = filepath
        self.sources = {"tab1": {}, "tab2": {}, "tab3": {}}

    def load_sources(self, tab_index):
        sources = {}
        try:
            with open(f"{self.filepath}/Tab {str(tab_index + 1)}.txt", "r", encoding='utf-8') as file:
                for line in file:
                    name, path = line.strip().split(",", 1)
                    sources[name] = path
        except FileNotFoundError:
            pass
        self.sources[f"tab{str(tab_index + 1)}"] = sources
        return sources

    def save_sources(self, tab_index):
        sources = self.sources[f"tab{str(tab_index + 1)}"]
        with open(f"{self.filepath}/Tab {str(tab_index + 1)}.txt", "w", encoding='utf-8') as file:
            for name, path in sources.items():
                file.write(f"{name},{path}\n")

    def add_or_update_source(self, tab_index, name, path):
        self.load_sources(tab_index)
        self.sources[f"tab{str(tab_index + 1)}"][name] = path
        self.save_sources(tab_index)

    def delete_source(self, tab_index, name):
        self.load_sources(tab_index)
        if name in self.sources[f"tab{str(tab_index + 1)}"]:
            del self.sources[f"tab{str(tab_index + 1)}"][name]
            self.save_sources(tab_index)
