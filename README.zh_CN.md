# 批量编辑工具箱

**简体中文** | [English](README.md)

## 根据指定的词汇表文件，批量添加标签到匹配到的卡片；批量修改卡片字段的内容；批量移除字段中 HTML 的标签等。

> 注意：**这个插件仅在 windows 平台测试通过，测试中处理的卡片文本为英文，如果你需要处理的卡片是别的语言，请先做好数据库备份！**

**通过测试的版本:** 

```
Win 11 23H2(10-10.0.22621), Anki 23.10.1 (Pyqt6), Python 3.9.15 Qt 6.6.0 PyQt 6.6.0
Win 10 22H2(10-10.0.19045), Anki 2.1.61 (Pyqt5), Python 3.9.15 Qt 6.4.2 PyQt 6.4.0
Win 10 21H2(10-10.0.22621), Anki 23.10.1 (Pyqt6), Python 3.9.15 Qt 5.15.2 PyQt 5.15.5
```

---

<img src=".\screenshot\white.png" alt="white" style="zoom:50%;" />

<img src=".\screenshot\black.png" alt="black" style="zoom:50%;" />

---

**工具入口：**

<img src=".\screenshot\start.png" alt="black" style="zoom:75%;" />

---

## 根据词汇表文件批量添加标签。

<img src=".\screenshot\tag_01.png" alt="black" style="zoom:75%;" />

根据指定的标签筛选卡片，然后查找指定卡片字段的内容，与单词列表进行比较，匹配成功后将添加指定的标签到该卡片。

标签项是可选的，它可以让搜索到的范围更准确，如果要查找的卡片不包含任何标签，可以不选。确保你的笔记模板只记录一种笔记类型，要筛选的字段最好是唯一的，可以避免在无关的卡片也添加标签。

单词列表文件格式仅支持 `.txt` `.xls` `.xlsx` 。

对于 `.xls` `.xlsx` 格式的文件，只会读取第一个 sheet 中的第一列的内容。

**确保你的单词列表中都是完整的单词，以避免出现未知错误。**

最后，你需要重新打开卡片浏览窗口才能看到新添加的标签。

---

## 批量替换(清空)指定字段的内容。

<img src=".\screenshot\text_01.png" alt="black" style="zoom:75%;" />

> 注意：**如果卡片中存在 HTML 代码，错误的文本替换可能会造成卡片不能正常显示内容！**

根据指定的标签筛选卡片，查找卡片中指定字段的文本，并匹配要替换的文本部分。

如果新的文本包含 HTML 渲染样式，勾选 **Replace As HTML** 可以保存原来的样式。

**批量清空卡片字段：**点击 `All` 按钮，将自动填充 `totally-all-content` 文本，这个特定文本会被插件识别，然后让 `Input New Some Content` 新文本框留空，会清空所有匹配到的卡片的指定字段内容。

---

## 根据API添加单词的发音。

<img src=".\screenshot\audio_01.png" alt="black" style="zoom:75%;" />

根据标签筛选卡片，读取到卡片指定字段的单词，然后根据 API 获取单词的发音，并保存媒体文件，添加到卡片的指定字段。

插件默认使用 **Youdao** API，你也可以使用其他 API，但要确保 API 的调用格式和插件相匹配。插件会获取音频文件的地址，格式为 "api_link + word + sound_type"，这些地址最终会组合成一个可以在浏览器中访问的链接，插件所做的只是模拟在浏览器中访问和保存文件。

---

**如果你在使用中遇到了这个错误弹窗，忽略就好，它不会影响插件的正常运行，我还没搞明白哪里出的问题。**

```
Caught exception:
Traceback (most recent call last):
  File "aqt.main", line 275, in on_focus_changed
  File "_aqt.hooks", line 3460, in __call__
  File "aqt.main", line 822, in on_focus_did_change
AttributeError: 'QObject' object has no attribute 'window'
```

**如果你遇到了其他的 bug，请复制完整的错误信息，你可以在 Github 提交一个 issue，或者在Anki插件页面留言，我会尽快修复。**

---

获取插件的安装代码：<a href="https://ankiweb.net/shared/info/1609139780">AnkiWeb</a>
