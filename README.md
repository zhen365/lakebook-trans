# Lakebook-Trans

* 解析语雀lakebook格式，并转存为通用格式

## 实现

* 文档内容解析参照[语雀开发者文档](https://www.yuque.com/yuque/developer/lt69uo)，其中包含**lakebook格式说明**和**lake asl格式说明**
* 目前版本仅使用文档的**html**代码进行解析，文档中的公式和图像均为语雀 cdn 链接；在**lake asl**中保存了原始的公式 latex 以及链接，后续可据此进行改进
* 为了简洁删除了所有 html 标签中的语雀属性以及 id 锚点，但是语雀提供了[样式表](http://editor.yuque.com/ne-editor/lake-content-v1.css)，后续可以针对格式进行改进
* 目前仅支持导出所有文档，未保存层级信息。后续会添加此功能
## 用法示例
* 本地已有python环境，需要安装pyyaml、BeautifulSoup4
```
pip install -r requirements.txt
python lakebooktrans.py --lakebook test.lakebook --output output
```
* 本地无python环境，使用release版本
```
lakebooktrans.exe --lakebook test.lakebook --output output
```