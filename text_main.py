from aqt import QComboBox, QLabel, QMainWindow, QMessageBox, QVBoxLayout, mw

try:
    from PyQt6.QtWidgets import (QPushButton, QLineEdit)
except ImportError:
    from PyQt5.QtWidgets import (QPushButton, QLineEdit)

from . import text_function


class SelectTagWindow(QMainWindow):  
    def __init__(self, parent=None):  
        # select window
        super(SelectTagWindow, self).__init__(parent) 
        # window title
        self.setWindowTitle('Tags')  
        self.setGeometry(750, 350, 290, 190)  
        # message
        self.label_info = QLabel('Select a tag', self)  
        self.label_info.resize(300,30)
        self.label_info.setStyleSheet("QLabel{font-size : 20px; font: bold}");
        self.label_info.move(40,20)
        # pull-down option
        self.combo = QComboBox(self)
        self.combo.resize(220,30)  
        self.combo.move(40, 60)
        # fill options
        taglist = mw.col.tags.all()
        for tag in taglist:
            self.combo.addItem(tag)
        # set layout
        layout = QVBoxLayout()  
        layout.addWidget(self.label_info)  
        layout.addWidget(self.combo)  
        # confirmation button
        btn = QPushButton('Ok', self)  
        btn.move(90, 120)
        btn.clicked.connect(self.ok_clicked)  
        layout.addWidget(btn)  
  
    def ok_clicked(self):  
        # passed value
        selected_item = self.combo.currentText()  
        self.parent().select_tag_dialog.setText(selected_item)
        # mw.col.close()    
        self.close()
        
class SelectFieldWindow(QMainWindow):  
    def __init__(self, parent=None):  
        # select window
        super(SelectFieldWindow, self).__init__(parent) 
        # window title
        self.setWindowTitle('Fields')  
        self.setGeometry(750, 350, 290, 190)  
        # message
        self.label_info = QLabel('Select a field', self)  
        self.label_info.resize(300,30)
        self.label_info.setStyleSheet("QLabel{font-size : 20px; font: bold}");
        self.label_info.move(40,20)
        # pull-down option
        self.combo = QComboBox(self)
        self.combo.resize(220,30)  
        self.combo.move(40, 60)
        # fill options
        note_id_list = []
        # all tags
        tag_list = mw.col.tags.all()
        for tag in tag_list:
            # get card id
            card_id_list = mw.col.find_cards("tag:" + tag)
            for card_id in card_id_list:
                # turn to note id
                note_id_list.append(mw.col.get_card(card_id).note().id)
        field_name_list = []
        for note_id in note_id_list:
            # get field name
            list = mw.col.field_names_for_note_ids([note_id])
            for i in list:
                field_name_list.append(i)
        temp_list = []
        for i in field_name_list:
            if i not in temp_list:
                temp_list.append(i)
        for i in temp_list:
            self.combo.addItem(i)
        # set layout
        layout = QVBoxLayout()  
        layout.addWidget(self.label_info)  
        layout.addWidget(self.combo)  
        # confirmation button
        btn = QPushButton('Ok', self)  
        btn.move(90, 120)
        btn.clicked.connect(self.ok_clicked)  
        layout.addWidget(btn)  
  
    def ok_clicked(self):  
        # passed value
        selected_item = self.combo.currentText()  
        self.parent().field_name_dialog.setText(selected_item)
        # mw.col.close()
        self.close()
        
class MainWindow(QMainWindow):  
    def __init__(self, browser):  
        # main window
        super(MainWindow, self).__init__()  
    
        # set window title
        self.setWindowTitle("Batch Replace Text")
        
        # field name
        self.field_name_value = ""
        # select tag name
        self.select_tag_value = ""
        # was replaced text
        self.replace_content_value = ""
        # replace text
        self.was_replace_content_value = ""
        
        # replace content layout
        # select a tag
        self.search_tag_title = QLabel('Select   Tag: ', self)
        self.search_tag_title.move(20, 20)
        # input select tag name
        self.select_tag_dialog = QLineEdit(self)
        self.select_tag_dialog.setPlaceholderText(' Tags To Look For')
        self.select_tag_dialog.resize(210, 30)
        self.select_tag_dialog.move(130, 15)
        self.select_tag_dialog.setMaxLength(30)
        # select tag button
        self.select_tag_btn = QPushButton("SelectTag", self)
        self.select_tag_btn.resize(150, 30)
        self.select_tag_btn.move(350, 15)
        # select field name
        self.fields_name_title = QLabel('Field   Name: ', self)
        self.fields_name_title.move(20, 60)
        # input field name
        self.field_name_dialog = QLineEdit(self)
        self.field_name_dialog.setPlaceholderText(" Card's Fields Name")
        self.field_name_dialog.resize(210, 30)
        self.field_name_dialog.move(130, 55)
        self.field_name_dialog.setMaxLength(30)
        # select field name button
        self.fields_name_btn = QPushButton("SelectField", self)
        self.fields_name_btn.resize(150, 30)
        self.fields_name_btn.move(350, 55)
        # was replaced text
        self.was_replaced_title = QLabel('WasReplaced: ', self)
        self.was_replaced_title.move(20, 100)
        # input was replaced text
        self.was_replaced_text = QLineEdit(self)
        self.was_replaced_text.setPlaceholderText(' Was Replaced Content')
        self.was_replaced_text.resize(210, 30)
        self.was_replaced_text.move(130, 95)
        # select all content function button
        self.select_all_btn = QPushButton("AllContent", self)
        self.select_all_btn.resize(150, 30)
        self.select_all_btn.move(350, 95)
        # replace new text
        self.new_content = QLabel('New Content: ', self)
        self.new_content.move(20, 140)
        # input new text
        self.new_content_text = QLineEdit(self)
        self.new_content_text.setPlaceholderText(' Input Some New Content')
        self.new_content_text.resize(370, 30)
        self.new_content_text.move(130, 135)
        # start replace, if was replaced text is null, equal delete
        self.batch_eplace_content_btn = QPushButton("Batch Replace Content", self)
        self.batch_eplace_content_btn.resize(210, 30)
        self.batch_eplace_content_btn.move(130, 170)
        
        # help doc link
        helpDoc = QLabel(self)
        helpDoc.resize(600, 30)
        helpDoc.move(110, 210)
        helpDoc.setText(
            "If you have any question, Click here: <a href='https://github.com/Anki-Tools/BatchTools'> Github</a> <a href='https://github.com/Anki-Tools/BatchTools'>AnkiWeb</a>")
        # The setOpenExternalLinks (True) method of the tag is used to control the connection with the external environment
        helpDoc.setOpenExternalLinks(True)
        
        layout = QVBoxLayout()  
        layout.addWidget(self.select_tag_dialog)
        layout.addWidget(self.select_tag_btn) 
        layout.addWidget(self.field_name_dialog) 
        layout.addWidget(self.fields_name_btn) 
         
        # set window size
        self.setFixedSize(520, 240)
        self.show()
    
        # start button
        self.batch_eplace_content_btn.clicked.connect(self.batch_replace_text)
        
        # button function
        self.select_tag_btn.clicked.connect(self.show_select_tag_window) 
        self.fields_name_btn.clicked.connect(self.show_select_field_window)
        self.select_all_btn.clicked.connect(self.help_doc)
        
    # replace text
    def batch_replace_text(self):
        choice = QMessageBox.question(self, "Confirm", "Confirmation to start?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if(choice == QMessageBox.StandardButton.Yes):
            # select tag , was replaced text, new text
            self.select_tag_value = self.select_tag_dialog.text()
            self.field_name_value = self.field_name_dialog.text()
            self.was_replace_content_value = self.was_replaced_text.text()
            self.replace_content_value = self.new_content_text.text()
            text_function.replace_text(self.select_tag_value, self.field_name_value, self.was_replace_content_value, self.replace_content_value)
        
    def show_select_tag_window(self):
        # select tag window
        select_window = SelectTagWindow(self)  
        select_window.show()  
        
    def show_select_field_window(self):
        # select field window
        select_window = SelectFieldWindow(self)  
        select_window.show()  

    def help_doc(self):
        self.was_replaced_text.setText("totally-all-content")
        
def text_start():
    # mw.tools_dialog = InputDialog(mw.app.activeWindow())
    mw.tools_dialog = MainWindow(mw.app.activeWindow())
    mw.tools_dialog.show()
