import json
import os


def load_translations(lang):
    file_path = os.path.join("locales", f"{lang}.json")
    with open(file_path, encoding="utf-8") as tradfile:
        return json.load(tradfile)
