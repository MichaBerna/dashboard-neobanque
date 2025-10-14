import json
import os


def load_translations(lang):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_root, "locales", f"{lang}.json")
    with open(file_path, encoding="utf-8") as tradfile:
        return json.load(tradfile)
