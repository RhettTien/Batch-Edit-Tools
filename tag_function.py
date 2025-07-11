from aqt import QMessageBox, QWidget
from aqt import mw

from . import xlrd_local


def add_tag(select_tag_value, add_tag_value, field_name_value, file_path_value):

    self = QWidget()

    if field_name_value == "" or add_tag_value == "":
        QMessageBox.warning(
            self,
            "Warning",
            "The Field Name or the Tag cannot be null!",
            QMessageBox.StandardButton.Yes,
        )
        return

    # wrong file path
    if len(file_path_value) < 2:
        QMessageBox.warning(
            self,
            "Warning",
            "Must select a word list file to execute!",
            QMessageBox.StandardButton.Yes,
        )
        return

    # wrong file type
    file_type = file_path_value[file_path_value.rfind(".") + 1 :]
    if file_type != "xls" and file_type != "xlsx" and file_type != "txt":
        QMessageBox.critical(
            self,
            "Wrong!",
            "Please select the correct file format!\r\n.txt .xls .xlsx",
            QMessageBox.StandardButton.Yes,
        )
        return

    word_list = []
    if file_type == "txt":
        # txt
        t = open(file_path_value, encoding="UTF-8")
        for line in t:
            line = line.strip().replace("\n", "").replace("\r", "")
            word_list.append(line)
    else:
        # xls, xlsx
        workbook = xlrd_local.open_workbook(file_path_value)
        sheet = workbook.sheet_by_index(0)
        for i in range(0, sheet.nrows):
            word = sheet.row_values(i)[0].strip()
            if word != "":
                word_list.append(word)

    word_list = set(word_list)

    number = 0
    if select_tag_value == "":
        for word in word_list:
            cards_id = mw.col.find_cards(field_name_value + ":" + word)
            if cards_id:
                for card_id in cards_id:
                    note = mw.col.get_card(card_id).note()
                    # tags = note.tags
                    # if select_tag_value not in tags:
                    note.add_tag(add_tag_value)
                    mw.col.update_note(note)
                    number += 1

    else:
        cards_id = mw.col.find_cards("tag:" + select_tag_value)
        if cards_id:
            for card_id in cards_id:
                note = mw.col.get_card(card_id).note()
                word = mw.col.get_card(card_id).note()[field_name_value]
                if word in word_list:
                    note.add_tag(add_tag_value)
                    mw.col.update_note(note)
                    number += 1

    # show a message box
    QMessageBox.information(
        self,
        "Result",
        "Update cards count: %d" % number
        + "\r\nReopen the window to refresh the changes.",
        QMessageBox.StandardButton.Yes,
    )
