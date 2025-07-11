from aqt import QComboBox, QFileDialog, QLabel, QMainWindow, QVBoxLayout, mw

try:
    from PyQt6.QtWidgets import (QPushButton, QLineEdit)
except ImportError:
    from PyQt5.QtWidgets import (QPushButton, QLineEdit)

from . import audio_function


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
        self.setWindowTitle("Batch Add Audio")
        
        # select tag name
        self.select_tag_value = ""
        # field name
        self.find_field_name_value = ""
        self.save_field_name_value = ""
        # prefix file name
        self.prefix_name = ""
        # user name
        self.local_username = ""
        # emit sound
        self.emit_sound_type = ""
        # api
        self.api_value = ""
        # sleep time
        self.sleep_time = ""
        # folder path
        self.folder_path = ""

        # add audio layout
        # select a tag
        self.select_tag_title = QLabel('Select   Tag: ', self)
        self.select_tag_title.move(20, 20)
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
        self.field_name_dialog1 = QLineEdit(self)
        self.field_name_dialog1.setPlaceholderText(" Card's Fields Name")
        self.field_name_dialog1.resize(210, 30)
        self.field_name_dialog1.move(130, 55)
        self.field_name_dialog1.setMaxLength(30)
        # select field name button
        self.fields_name_btn1 = QPushButton("SelectField", self)
        self.fields_name_btn1.resize(150, 30)
        self.fields_name_btn1.move(350, 55)
        # write to field name
        self.w_fields_name_title = QLabel('Write  Field: ', self)
        self.w_fields_name_title.move(20, 100)
        # input write field name
        self.field_name_dialog2 = QLineEdit(self)
        self.field_name_dialog2.setPlaceholderText(" Fields Written To")
        self.field_name_dialog2.resize(210, 30)
        self.field_name_dialog2.move(130, 95)
        self.field_name_dialog2.setMaxLength(30)
        # select write field name button
        self.fields_name_btn2 = QPushButton("SelectField", self)
        self.fields_name_btn2.resize(150, 30)
        self.fields_name_btn2.move(350, 95)
        # prefix file name
        self.prefix_name_title = QLabel('Prefix Name: ', self)
        self.prefix_name_title.move(20, 140)
        # input prefix file name
        self.prefix_name_dialog = QLineEdit(self)
        self.prefix_name_dialog.setPlaceholderText(" Default is 'ODH_youdao_encn_'")
        self.prefix_name_dialog.resize(370, 30)
        self.prefix_name_dialog.move(130, 135)
        self.prefix_name_dialog.setMaxLength(30)
        # emit_sound
        self.emit_sound_name_title = QLabel('Emit  Sound: ', self)
        self.emit_sound_name_title.move(20, 180)
        # input emit_sound name
        self.emit_sound_name_dialog = QLineEdit(self)
        self.emit_sound_name_dialog.setPlaceholderText(" Pronunciation Type, 0:US, 1:UK, Default:0")
        self.emit_sound_name_dialog.resize(370, 30)
        self.emit_sound_name_dialog.move(130, 175)
        self.emit_sound_name_dialog.setMaxLength(30)
        # audio api
        self.audio_API_title = QLabel('Audio   API: ', self)
        self.audio_API_title.move(20, 220)
        # input audio api
        self.audio_API_text = QLineEdit(self)
        self.audio_API_text.setPlaceholderText(' Audio API(Default Built-in Youdao)')
        self.audio_API_text.resize(370, 30)
        self.audio_API_text.move(130, 215)
        # interval time
        self.interval_time_title = QLabel('Sleep  Time: ', self)
        self.interval_time_title.move(20, 260)
        # input interval time
        self.interval_time = QLineEdit(self)
        self.interval_time.setPlaceholderText(' Interval Time, Default 198 ms(milliseconds)')
        self.interval_time.resize(370, 30)
        self.interval_time.move(130, 255)

        # folder path button
        self.folder_btn = QPushButton("SaveFolder", self)
        self.folder_btn.resize(150, 30)
        self.folder_btn.move(350, 290)
        
        # start add audio
        self.batch_add_audio_btn = QPushButton("Batch Add Audios", self)
        self.batch_add_audio_btn.resize(210, 30)
        self.batch_add_audio_btn.move(130, 290)
        
        # help doc link
        helpDoc = QLabel(self)
        helpDoc.resize(600, 30)
        helpDoc.move(95, 330)
        helpDoc.setText(
            "If you have any question, Click here: <a href='https://github.com/RhettTien/Batch-Editor-Tools'> Github</a> <a href='https://ankiweb.net/shared/info/1609139780'>AnkiWeb</a>")
        # The setOpenExternalLinks (True) method of the tag is used to control the connection with the external environment
        helpDoc.setOpenExternalLinks(True)
        
        layout = QVBoxLayout()  
        layout.addWidget(self.select_tag_dialog)
        layout.addWidget(self.select_tag_btn) 
        layout.addWidget(self.field_name_dialog1) 
        layout.addWidget(self.fields_name_btn1) 
        layout.addWidget(self.field_name_dialog2) 
        layout.addWidget(self.fields_name_btn2) 
         
        # set window size
        self.setFixedSize(520, 360)
        self.show()
    
        # start button
        self.batch_add_audio_btn.clicked.connect(self.batch_add_audios)
        
        # button function
        self.select_tag_btn.clicked.connect(self.show_select_tag_window) 
        self.fields_name_btn1.clicked.connect(self.show_select_field_window)
        self.fields_name_btn2.clicked.connect(self.show_select_field_window)
        self.folder_btn.clicked.connect(self.select_folder_path)
        
    # add audios
    def batch_add_audios(self):
            self.select_tag_value = self.select_tag_dialog.text()
            self.find_field_name_value = self.field_name_dialog1.text()
            self.save_field_name_value = self.field_name_dialog2.text()
            self.prefix_name = self.prefix_name_dialog.text()
            self.emit_sound_type = self.emit_sound_name_dialog.text()
            self.api_value = self.audio_API_text.text()
            self.sleep_time = self.interval_time.text()
            # start function
            audio_function.add_audio(
                self.select_tag_value,
                self.find_field_name_value,
                self.save_field_name_value,
                self.prefix_name,
                self.emit_sound_type,
                self.api_value,
                self.sleep_time,
                self.folder_path
                )
        
    def show_select_tag_window(self):
        # select tag window
        select_window = SelectTagWindow(self)  
        select_window.show()  
        
    def show_select_field_window(self):
        global type
        if(self.sender() == self.fields_name_btn1):
            type = 1
        else:
            type = 2
        # select field window
        select_window = SelectFieldWindow(self)  
        select_window.show()  

    # if have filled in a username can not use this method
    def select_folder_path(self):
        directory = QFileDialog.getExistingDirectory(self,"Select Save Folder","C:/")
        self.folder_path = directory
        
def audio_start():
    # mw.tools_dialog = InputDialog(mw.app.activeWindow())
    mw.tools_dialog = MainWindow(mw.app.activeWindow())
    mw.tools_dialog.show()
