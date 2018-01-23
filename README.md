# Reference
解析论文提取参考文献实现自动下载题录，这是一个 Python 实现的项目。通过 pdfminer
这个第三方模块把 pdf 转变成文本，利用正则表达式提取参考文献，再获取每条文献的题目，使
用 biopython 模块提供的访问 Entrez 数据库的方法，对 PubMed 数据库进行访问下载相应的题
录。
