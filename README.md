# Batch Edit Tools

[简体中文](README.zh_CN.md) | **English**

## If you have a need to batch edit card tag or field or audio, you should try this plugin.

> NOTE: **The plug-in only in the windows operating system has been tested, the test text for the English language, if you edit the text of other languages, please make a backup first!**

**Tested version:** 
```
Win 11 23H2(10-10.0.22621), Anki 23.10.1 (Pyqt6), Python 3.9.15 Qt 6.6.0 PyQt 6.6.0
Win 10 22H2(10-10.0.19045), Anki 2.1.61 (Pyqt5), Python 3.9.15 Qt 6.4.2 PyQt 6.4.0
Win 10 21H2(10-10.0.22621), Anki 23.10.1 (Pyqt6), Python 3.9.15 Qt 5.15.2 PyQt 5.15.5
```

---

<img src=".\screenshot\white.png" alt="white" style="zoom:50%;" />

<img src=".\screenshot\black.png" alt="black" style="zoom:50%;" />

---

**Plugin Launch Portal:**

<img src=".\screenshot\start.png" alt="black" style="zoom:75%;" />

---

## Batch add tags according to the specified vocabulary list.

<img src=".\screenshot\tag_01.png" alt="black" style="zoom:75%;" />

Filter the cards according to the specified tags, then look up the contents of the card field, compare it with the word list, and add the specified tags to this card after a successful match.

The tag item is optional, it can make the search to the scope of more accurate, if you want to find the card does not contain the tag can be unselected.

As you can see, the word list file only supports the `.txt` `.xls` `.xlsx` file format.

For `.xls` `.xlsx` files, the plug-in reads only the first column of the first sheet.

**Please check your list of words carefully to make sure each is a complete word!**

You need to reopen the browser window to see the new add tags.

---

## Batch Replaces(or Empty ) the contents of the specified fields.

<img src=".\screenshot\text_01.png" alt="black" style="zoom:75%;" />

> NOTE: **If the field contains hypertext elements such as HTML, you need to be aware that incorrect text substitution can cause display problems for your card**!

Filter the cards according to the specified tags, find the text of the specified fields in the card, and match the part of the text to be replaced.

**Batch Empty Field Content:** Clicking the `All` button will populate the `totally-all-content` character, the plugin will select the content of the specified field of the card, and if the `Input New Some Content` text box is left **empty**, it will perform a field clearing operation.

---

## Batch add word pronunciations based on API.

<img src=".\screenshot\audio_01.png" alt="black" style="zoom:75%;" />

Get the pronunciation of the word through the API, then save the media file locally and add the media file to the specified field of the card.

The plugin uses **Youdao** API by default, you can also use other APIs, but be careful to make sure the format matches.
The plugin gets the address of the audio file in the format `api_link + word + sound_type`, which will eventually be combined into a link that can be accessed in the browser, all the plugin does is to simulate accessing and saving the file in the browser.

---

**If you trigger this error message, don't worry, the plugin will still work fine, I haven't figured out what's going on yet.**

```
Caught exception:
Traceback (most recent call last):
  File "aqt.main", line 275, in on_focus_changed
  File "_aqt.hooks", line 3460, in __call__
  File "aqt.main", line 822, in on_focus_did_change
AttributeError: 'QObject' object has no attribute 'window'
```

**If you trigger another bug, please copy the detailed error message and submit an issue, and I'll fix it as soon as possible.**

---

Gets the plug-in installation number: <a href="https://ankiweb.net/shared/info/1609139780">AnkiWeb</a>
