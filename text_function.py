from aqt import QMessageBox, QWidget
from aqt import mw


def replace_text(
    is_html,
    select_tag_value, 
    field_name_value, 
    was_replace_content_value, 
    replace_content_value
    ):
    self = QWidget()
    
    tag_v : str
    field_v: str
    was_replace_value: str
    replace_value: str
    
    tag_v = str(select_tag_value)
    field_v = str(field_name_value)
    was_replace_value = str(was_replace_content_value)
    replace_value = str(replace_content_value)
    
    if(not is_html):
        replace_value = str(replace_content_value).replace("\n", "<br>")
        
    if(tag_v == "" and field_v == ""):
        QMessageBox.warning(self, "Warning", "Tag Names and Field Names are required!",QMessageBox.StandardButton.Yes)
        return
    
    if(was_replace_value == ""):
        QMessageBox.warning(self, "Warning", "Enter what you want to replace!",QMessageBox.StandardButton.Yes)
        return
    
    # empty function
    if(was_replace_value == "totally-all-content"):
        # get card id list
        card_id_list = mw.col.find_cards("tag:" + tag_v)
        count = 0
        for card_id in card_id_list:
            # get field content
            #str_field_content = col.get_card(card_id).note()[field_v]
            note = mw.col.get_card(card_id).note() 
            try:
                note[field_v] = replace_value
            except:
                QMessageBox.critical(self, "Wrong!", "The filtered card does not have the specified Field, please select another one!",QMessageBox.StandardButton.Yes)
                return
            note.flush()
            count += 1
            
        if(replace_value == ""):
            QMessageBox.information(self, "Result", "Empty field content count: %d" % count,QMessageBox.StandardButton.Yes)
        else:
            QMessageBox.information(self, "Result", "Update cards count: %d" % count,QMessageBox.StandardButton.Yes)

    # replace function
    else:
        count = 0
        # get card id list
        card_id_list = mw.col.find_cards("tag:" + tag_v)
        for card_id in card_id_list:
            # get field content
            note = mw.col.get_card(card_id).note() 
            str_field_content = ""
            try:
                str_field_content = note[field_v]
            except:
                QMessageBox.critical(self, "Wrong!", "The filtered card does not have the specified Field, please select another one!",QMessageBox.StandardButton.Yes)
                return
            if(was_replace_value in str_field_content):
                note[field_v] = str_field_content.replace(was_replace_value, replace_value)
                note.flush()
                count += 1
                
        QMessageBox.information(self, "Result", "Update cards count: %d" % count,QMessageBox.StandardButton.Yes)
        
# Features updated in the next version: Fills the specified field contents based on the matching of the external file list and fields
