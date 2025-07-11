from aqt import QCheckBox, QComboBox, QLabel, QMainWindow, QMessageBox, QTextEdit, QVBoxLayout, mw

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
        for tag in sorted(taglist):
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
        if self.parent().select_tag_dialog.text() == "":
            fields_list = []
            for tag in set(mw.col.tags.all()):
                notes_list = mw.col.find_notes("tag:" + tag)
                # fields = mw.col.get_note(notes_list[0]).keys()
                fields = mw.col.field_names_for_note_ids([notes_list[0]])
                for field in fields:
                    fields_list.append(field)
            for field_name in sorted(set(fields_list)):
                self.combo.addItem(field_name)
        else:
            notes_list = mw.col.find_notes("tag:" + self.parent().select_tag_dialog.text())
            if notes_list:
                fields_list = set(mw.col.field_names_for_note_ids([notes_list[0]]))
                for field_name in sorted(fields_list):
                    self.combo.addItem(field_name)
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
        # insert as html
        self.is_html = False
        
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
        self.was_replaced_text = QTextEdit(self)
        self.was_replaced_text.setPlaceholderText(' Was Replaced Content(Plain text only)')
        self.was_replaced_text.resize(370, 130)
        self.was_replaced_text.move(130, 95)
        # select all content function button
        self.select_all_btn = QPushButton("All", self)
        self.select_all_btn.resize(95, 30)
        self.select_all_btn.move(15, 135)
        # clear
        self.w_clear_btn = QPushButton("Clear", self)
        self.w_clear_btn.resize(95, 30)
        self.w_clear_btn.move(15, 175)
        # as html or text
        self.chkBox = QCheckBox(self)
        self.chkBox.setText("Replace As HTML")
        self.chkBox.move(360, 375)
        self.chkBox.resize(200, 24)
        self.chkBox.stateChanged.connect(self.btnState)
        # self.chkBox.stateChanged.connect(lambda: self.btnState(self.chkBox))
        
        # replace new text
        self.new_content = QLabel('New Content: ', self)
        self.new_content.move(20, 240)
        # clear
        self.n_clear_btn = QPushButton("Clear", self)
        self.n_clear_btn.resize(95, 30)
        self.n_clear_btn.move(15, 275)
        # input new text
        self.new_content_text = QTextEdit(self)
        self.new_content_text.setPlaceholderText(' Input Some New Content(Text or HTML)')
        self.new_content_text.resize(370, 130)
        self.new_content_text.move(130, 235)
        # start replace, if was replaced text is null, equal delete
        self.batch_eplace_content_btn = QPushButton("Batch Replace", self)
        self.batch_eplace_content_btn.resize(210, 30)
        self.batch_eplace_content_btn.move(130, 370)
        
        # help doc link
        helpDoc = QLabel(self)
        helpDoc.resize(600, 30)
        helpDoc.move(95, 410)
        helpDoc.setText(
            "If you have any question, Click here: <a href='https://github.com/RhettTien/Batch-Editor-Tools'> Github</a> <a href='https://ankiweb.net/shared/info/1609139780'>AnkiWeb</a>")
        # The setOpenExternalLinks (True) method of the tag is used to control the connection with the external environment
        helpDoc.setOpenExternalLinks(True)
        
        layout = QVBoxLayout()  
        layout.addWidget(self.select_tag_dialog)
        layout.addWidget(self.select_tag_btn) 
        layout.addWidget(self.field_name_dialog) 
        layout.addWidget(self.fields_name_btn) 
         
        # set window size
        self.setFixedSize(520, 440)
        self.show()
    
        # start button
        self.batch_eplace_content_btn.clicked.connect(self.batch_replace_text)
        
        # button function
        self.select_tag_btn.clicked.connect(self.show_select_tag_window) 
        self.fields_name_btn.clicked.connect(self.show_select_field_window)
        self.select_all_btn.clicked.connect(self.all_content)
        self.w_clear_btn.clicked.connect(self.clear_content)
        self.n_clear_btn.clicked.connect(self.clear_content)
    
    def btnState(self):
        self.is_html = self.chkBox.isChecked()
        
    # replace text
    def batch_replace_text(self):
        choice = QMessageBox.question(self, "Confirm", "Confirmation to start?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if(choice == QMessageBox.StandardButton.Yes):
            # if html, select tag , was replaced text, new text
            self.select_tag_value = self.select_tag_dialog.text()
            self.field_name_value = self.field_name_dialog.text()
            
            if(self.is_html):
                # html
                
                was_v : str
                if(str(self.was_replaced_text.toPlainText()) == "totally-all-content"):
                    was_v = "totally-all-content"
                else:
                    was_v = str(self.was_replaced_text.toPlainText())
                
                text_function.replace_text(
                    self.is_html,
                    self.select_tag_value, 
                    self.field_name_value, 
                    was_v, 
                    str(self.new_content_text.toHtml()))
            elif(not self.is_html):
                # text
                text_function.replace_text(
                    self.is_html,
                    self.select_tag_value, 
                    self.field_name_value, 
                    str(self.was_replaced_text.toPlainText()), 
                    str(self.new_content_text.toPlainText()))
        
    def show_select_tag_window(self):
        # select tag window
        select_window = SelectTagWindow(self)  
        select_window.show()  
        
    def show_select_field_window(self):
        # select field window
        select_window = SelectFieldWindow(self)  
        select_window.show()  

    def all_content(self):
        self.was_replaced_text.setText("totally-all-content")
        
    def clear_content(self):
        if(self.sender() == self.w_clear_btn):
            self.was_replaced_text.setText("")  
        else:
            self.new_content_text.setText("")  
            
def text_start():
    # mw.tools_dialog = InputDialog(mw.app.activeWindow())
    mw.tools_dialog = MainWindow(mw.app.activeWindow())
    mw.tools_dialog.show()
