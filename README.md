# Obsidian2MkDocs

**Obsidian2MkDocs**是用于将 Obsidian 文档导出为 MkDocs 文档的脚本工具，它是一套基于文本匹配的转化工具，能够把你的 Obsidian 笔记转化为符合 MkDocs 笔记

## Features

- 将 Obsidian 文档导出为 MkDocs 文档
    - 提示块转化
    - 代码块转化
    - 行内代码转化
- 批量导出
    - 转化单个Markdown文件
    - 批量导出指定目录下的所有 Obsidian 文档
    - 自动复制非 Markdown 文件
    - 自主选择是否覆盖已存在的文件
- 配置文件
    - 缩进配置
    - 代码块高亮行自定义关键词
    - `.gitignore` 语法忽略特定文件
    - 设置 Markdown 的元数据
- 基于命令行的使用

## Usages

顶层模块为`src/Obsidian2MkDocs.py`，所有的操作都封装在`src.Obsidian2MkDocs.Obsidian2Mkdocs`类中，你可以直接调用这个类提供的两个接口，也可以直接使用已经完全封装的`src.Obsidian2MkDocs.main`方法在命令行中一键转化

### Command Line Interface

运行`main.py`即可使用命令行

```shell
python main.py [-h] [-c CONFIG] [-o] [--debug] src [dest]
```

### APIs

1. 类初始化`__init__`，解析配置文件
2. 转化`convert`
   1. 源路径中所有文件路径解析
   2. 使用`ignores`配置进行忽略
   3. 解析每个文件，进行转化
   4. 输出到目标路径

### Configurations

配置文件应该在当前工作目录下，默认名为`configs.yml`

配置文件应该包含以下内容：

```yaml
# 配置文件默认名：configs.yml
indent: 4 # 缩进
frontmatter: # 元数据中保留的配置项
  - "tags"
code_block: # 代码块配置
  highlight_keywords: # 自定义高亮关键词列表
    - "hl" # Obsidian 默认值
    - "error"
    - "warning"
    - "info"
ignores: # 忽略文件列表，遵守.gitignore语法
  - ".vscode/"
  - ".git/"
  - ".github/"
  - "__pycache__/"
  - ".obsidian/"
```

## About

关于这个工具的来由

- Obsidian：对于我个人来说，我是忠实的 [Obsidian](https://obsidian.md/) 用户，对于 Obsidian 来说，它已经非常强大了，能够满足我本地使用作为笔记管理软件和个人知识库构建的绝大部分功能，其扩展市场也非常优良
- MkDocs：这是一个非常优秀的静态站点生成器，其基于 Python 和 Markdown，并且非常容易扩展，易于使用，功能也很强大，因此把它作为个人知识库的静态站点生成器使用

注意到 MkDocs 的使用更多需要实时启用以实现即时渲染，而对于很多的笔记情况来说比较麻烦，所以目前来说，我更偏向于使用 Obsidian 记录，但是 Obsidian 又无法直接发布为静态站点，只能在本地使用，所以需要一个把本地的笔记转化为静态站点的工具

探索过程：

1. 最初我就想到了，因为 MkDocs 可以直接生成静态站点，并且上手简单，功能强大，因此可以直接使用它
2. 但是，Obsidian 的 Markdown 语法和 MkDocs 的语法并不完全一致，比如它们的提示块语法就有很大的差异
3. 所以，我需要一个基于字符匹配和替换的工具，能够把 Obsidian 的文档转化为 MkDocs 的文档，考虑到 Python 的方便和一些强大的库，决定上手
4. 开发过程中其实有很多的问题，需要考虑很多情况，而且这其实有点造轮子，所以中途重新思考过如何做
5. 后来思考和查阅后，得出几个方案：
   1. 搜索直接基于 Obsidian 的发布为静态站点的开源项目作为使用，也找到了几个，但是使用后都感觉不是很符合个人的一些想法（并不是说这些项目不好，只是不符合个人的习惯）
   2. 更换静态站点生成器，比如 Hexo，但是这个也感觉不太符合个人习惯，而且需要从头学习它们的用法
   3. 自己写一个工具，把这个工具直接集成到笔记仓库里，最后用 Github Action 来自动发布为静态站点
      1. 方案一是半途而废的基于字符串匹配和替换的方案，这个方案还是可以的，只是需要考虑很多，但是假期时间其实充裕，可以做
      2. 方案二是直接写一个 PyMarkdown 的扩展，因为 MkDocs 是基于 [PyMarkdown](https://python-markdown.github.io) 的，它的转化 Markdown 为 HTML 的过程是完全调用 PyMarkdown 的，所以可以写一个 PyMarkdown 的扩展，识别 Obsidian 中不一样的语法（比如提示块），但是这个方案难度比方案一大，需要考虑很多细节，所以这个方案就暂时没有开启

基于这个探索过程，最后选择了继续原来的方案，最后经过不断的完善就写成这样一个小的脚本工具

我更多称它为一个脚本工具，因为它只实现了一些简单的功能（提示块、代码块），但是我给它封装完全了，应该可以很方便地进行使用了，总体来说它转化出的 MkDocs 文档肯定和你在 Obsidian 里的文档的样式会有不同，但是应该是大体上渲染效果不会有很大的差别了

**但是，这不代表这个工具可以万无一失了**，因为可能还有很多的 bug 需要修复，或者有些地方考虑不全，所以**使用的时候请注意备份你的源文件！！！**

关于代码块，这里是使用了一个 Obsidian 的插件 [Obsidian-Code-Styler](https://github.com/mayurankv/Obsidian-Code-Styler)，我觉得这个插件能够更多丰富代码块的内容，比如添加代码块标题、显示行号、高亮等，也和 MkDocs 有很大相似之处，所以我的代码块转化是基于这个插件的

最后，希望这个工具能够对您有些许帮助，如果您在使用过程中发现任何 bug 或者有更好的建议，欢迎提交 Issue 或 Pull Request ，我会尽量尽快解决，或者接受您的建议，感谢您的支持！

## Structure

```shell
.
├── README.md              # 自述文件
├── clean.sh               # 清理脚本
├── configs.yml            # 配置文件
├── main.py                # 主程序
├── requirements.txt       # 依赖文件
└── src                    # 源代码
    ├── Obsidian2MkDocs.py # 顶层模块
    ├── __init__.py
    ├── admonitions        # 提示块模块
    │   ├── __init__.py
    │   └── admonition.py
    ├── codes              # 代码块模块
    │   ├── __init__.py
    │   ├── code_block.py
    │   └── inline_code.py
    ├── converter.py       # 转化器
    ├── frontmatters       # 元数据模块
    │   ├── __init__.py
    │   └── frontmatter.py
    ├── parser.py          # 解析器
    └── utils              # 工具模块
        ├── __init__.py
        ├── algorithm.py
        ├── cli.py
        ├── file_manager.py
        ├── logger.py
        └── statistics.py
```
