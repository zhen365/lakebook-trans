import os
import re
import shutil
import argparse

import json
import yaml
import tarfile
from bs4 import BeautifulSoup


class BaseInfo:
    def __init__(self, data) -> None:
        self.type = data["type"]
        self.title = data["title"]
        self.level = data["level"]
        self.uuid = data["uuid"]
        

class Doc(BaseInfo):
    def __init__(self, data, path) -> None:
        super().__init__(data)
        self.path = path
        self.url = data["url"]
        self.content = None
        self.get_body()

    def get_body(self):
        with open(f"{self.path}/{self.url}.json", encoding="utf-8") as f:
            doc = json.load(f)
        body = BeautifulSoup(doc["doc"]["body"], "html.parser")
        for tag in body():
            attrs = dict(tag.attrs)
            for attr in attrs:
                if attr != 'src':
                    del tag[attr]
        self.content = str(body)
    
    def save_as_html(self, output):
        if self.content != "":
            content = BeautifulSoup(self.content,  "html.parser")
            body = str(content.contents[2])
        else:
            body = ""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <link rel="stylesheet" type="text/css" href="{css_file}">
        </head>
        <body>
        {body}
        </body>
        </html>
        """
        html = html_template.format(title = self.title, css_file = "", body = body)
        html = BeautifulSoup(html, "html.parser")
        print(self.title)
        filename = re.sub(r'[\\/*?:"<>|]', '_', self.title)
        with open(f"{output}/{filename}.html", mode="a+", encoding="utf-8") as f:
            f.write(html.prettify())
        

class Dir(BaseInfo):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.child = []


class Book:
    def __init__(self, path) -> None:
        self.path = path
        self.metas = self.parser_meta_file()
        self.count = 0
        self.dir_list = []
        self.doc_list = []
        self.parser_tocYml()
        assert int(self.count) == len(self.dir_list) + len(self.doc_list), "元信息错误"

    def parser_meta_file(self):
        with open(f"{self.path}/$meta.json", encoding="utf-8") as f:
            info =json.load(f)
        tocYml = json.loads(info["meta"])["book"]["tocYml"]
        return yaml.load(tocYml, yaml.FullLoader)
    
    def parser_tocYml(self):
        for item in self.metas:
            if item["type"] == "META":
                self.count = item["count"]
                self.maxlevel = item["max_level"]
            elif item["type"] == "TITLE":
                self.dir_list.append(Dir(item))
            elif item["type"] == "DOC":
                self.doc_list.append(Doc(item, self.path))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='lakebook转换')
    parser.add_argument('--lakebook', type=str, help='lakebook文件地址')
    parser.add_argument('--output', type=str, help='输出地址')
    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.mkdir(args.output)
    lakebook = tarfile.TarFile(args.lakebook)
    lakebook.extractall(".laketmp")

    extract_dir = [item for item in os.listdir(".laketmp")][0]
    
    book = Book(os.path.join(".laketmp", extract_dir))
    for doc in book.doc_list:
        doc.save_as_html(args.output)
    
    shutil.rmtree(".laketmp", ignore_errors=True)