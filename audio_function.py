import os
import time
from aqt import QApplication, QLabel, QMainWindow, QMessageBox, QWidget, mw
import requests


def add_audio(
    # select tag name
    select_tag_value,
    # field name
    find_word_name_value,
    save_field_name_value,
    # prefix file name
    prefix_name,
    # emit sound
    emit_sound_type,
    # api
    audio_API,
    # sleep time
    sleep_time,
    # folder path
    folder_path
    ):
    self = QWidget()
    
    # tag or field name not null
    if(find_word_name_value == "" or select_tag_value == ""):
        QMessageBox.warning(self, "Waring", "The Field Name or the Tag cannot be null!",QMessageBox.StandardButton.Yes)
        return
    
    if(save_field_name_value == ""):
        QMessageBox.warning(self, "Waring", "Please select the field to which the audio file will be written!",QMessageBox.StandardButton.Yes)
        return
    
    # save file prefix
    if(prefix_name == ""):
        prefix_name = "ODH_youdao_encn_"
        
    # US or UK sound, default US
    if(emit_sound_type == ""):
        emit_sound_type = "0"
    
    # default Youdao API
    if(audio_API == ""):
        audio_API = "https://dict.youdao.com/dictvoice?audio="
    
    if(sleep_time == ""):
        sleep_time = 198
    
    sleep_times = 0
    try:
        sleep_times = int(sleep_time)
    except:
        QMessageBox.critical(self, "Wrong!", "The sleep time must be a Number!",QMessageBox.StandardButton.Yes)
        return
    
    if(sleep_times < 0):
        QMessageBox.critical(self, "Waring", "Time cannot be negative.!",QMessageBox.StandardButton.Yes)
        return
    
    if(sleep_times > 20000):
        choice = QMessageBox.warning(self, "Waring", "There's been a pause of more than 20 seconds.\r\nAre you sure you want to continue?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if(choice == QMessageBox.StandardButton.No):
            return
    
    # save file path
    if(folder_path == ""):
        QMessageBox.warning(self, "Waring", "Please select the folder where you want to save your media, the default path is\r\n'C:/Users/PC_user_name/AppData/Roaming/Anki2/anki_local_user_name/collection.media'",QMessageBox.StandardButton.Yes)
        return
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    
    global count
    count = 0
    not_word = 0
    cards_id_list = mw.col.find_cards("tag:" + select_tag_value)
    for i in cards_id_list:

        card = mw.col.get_card(i)
        note = card.note()
        
        # try block definitions to the outside can be faster
        # get a word
        word = ""
        try:
            # whether the field you are looking for exists
            word = note[find_word_name_value]
        except:
            QMessageBox.critical(self, "Wrong!", "The filtered card does not have the specified Field, please select another one!",QMessageBox.StandardButton.Yes)
            return
        
        if(str(word) == ""):
            not_word += 1
            if(not_word == 20):
                QMessageBox.warning(self, "Waring", "The field doesn't seem to be a word field!",QMessageBox.StandardButton.Yes)
                return
            return
        
        if(is_english_word(word) == False):
            QMessageBox.warning(self, "Waring", "The field doesn't seem to be a word field!",QMessageBox.StandardButton.Yes)
            return
        
        try:
            # existence of fields that can be written to
            temp = note[save_field_name_value]
        except:
            QMessageBox.critical(self, "Wrong!", "Media file field does not exist!",QMessageBox.StandardButton.Yes)
            return
        
        # audio file link
        # audio = "https://dict.youdao.com/dictvoice?audio=" + word + "%7D&type=1"
        audio_link = audio_API + word + "%7D&type=" + str(emit_sound_type)
        
        # file name
        media_name = prefix_name + word + "_" + str(emit_sound_type) + ".mp3"
        
        # save file path
        file_save_path = folder_path + "/" + media_name
        
        time.sleep( sleep_times / 1000 )
        
        # save the audio file
        save_audio_file = requests.get(url=audio_link, headers=headers).content
        with open(file_save_path, "wb") as f:
            f.write(save_audio_file)
            
        is_exist = os.path.exists(file_save_path)
        if(is_exist):
            # write to card
            fill_str = "[sound:" + media_name + "]"
            note[save_field_name_value] = fill_str
            note.flush()
            count += 1
            
        # QApplication.processEvents()
        
        update_window = ShowChangeCount(self)  
        update_window.show()
        
    QMessageBox.information(self, "Result", "Update cards count: %d" % count,QMessageBox.StandardButton.Yes)
    
# Next version update: Enabling multithreading can speed up execution, need to consider the accuracy of the counting function.

def is_english_word(character):
    for cha in character:
        if not 'A' <= cha <= 'Z' and not 'a' <= cha <= 'z':
            return False
    else:
        return True

class ShowChangeCount(QMainWindow):
    def __init__(self, parent=None):
        super(ShowChangeCount, self).__init__(parent) 
        # window title
        self.setWindowTitle('Wait a minute.')  
        self.setGeometry(700, 300, 320, 100)
        # message
        self.label_info = QLabel("Update cards count: %d" % count, self)  
        self.label_info.resize(300,30)
        self.label_info.setStyleSheet("QLabel{font-size : 20px; font: bold; color : green;}");
        self.label_info.move(40,40)
        
        self.show()
        QApplication.processEvents()