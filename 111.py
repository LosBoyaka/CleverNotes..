import json


from PyQt5.QtWidgets import *

app = QApplication([])
window = QWidget()
notes = {}

app.setStyleSheet("""


        QWidget
        {
        background-color: #FFC55A;
        
        
        
        }
        QPushButton
        {
            background-color: #FC4100;
            border-color: brown;
            color: white;
            border-style: groove;
            border-width: 5px;
            border-radius: 7px;
            font-family: "Times New Roman", Times, serif;
            min-width: 6em;
            padding: 6px;
            font-size: 15px;
        }
        QListWidget
        {
            font-size: 20px;
            font-style: oblique;
            color: white;
            font-family: "Times New Roman", Times, serif;
            background-color: #577B8D;
            border-style: groove;
            border-width: 5px;
            border-color: blue;
            border-radius: 7px;
        }
        QTextEdit
        {
            font-size: 20px;
            font-style: oblique;
            color: white;
            font-family: "Times New Roman", Times, serif;
            background-color: #2C4E80;
            border-style: groove;
            border-width: 5px;
            border-color: blue;
            border-radius: 7px;
        }
        QLineEdit
        {
            color: white;
            background-color: #00215E;
            border-style: groove;
            border-width: 4px;
            border-color: blue;
            border-radius: 3px;
        }
        QLabel
        {
            background-color: #ffffff;
            font-size: 15px;
            font-style: oblique;
            font-family: "Times New Roman", Times, serif;

        }
    """)




def read_data():
    global notes
    with open('notes.json', "r", encoding="utf-8") as f:
        notes = json.load(f)

read_data()


text_input = QTextEdit()
notes_lbl = QLabel("Список заміток")
notes_list = QListWidget()
notes_list.addItems(notes)
tag_input = QLineEdit()
tag_input.setPlaceholderText("Підказка")
create_note_btn = QPushButton("Створити замітку")
delete_note_btn = QPushButton("Видалити замітку")
change_note_btn = QPushButton("Змінити замітку")
add_to_note_btn = QPushButton("Додати до замітки")
delete_to_note_btn = QPushButton("Видалити від замітки")
tag_search_btn = QPushButton("Шукати по тегу")

tag_lbl = QLabel("Список тегів")
tags_list = QListWidget()

main_line = QHBoxLayout()
main_line.addWidget(text_input)


v1 = QVBoxLayout()
h1 = QHBoxLayout()
h2 = QHBoxLayout()
v1.addWidget(notes_lbl)
v1.addWidget(notes_list)
v1.addLayout(h1)
h1.addWidget(create_note_btn)
h1.addWidget(delete_note_btn)
v1.addWidget(change_note_btn)
v1.addWidget(tag_lbl)
v1.addWidget(tags_list)
v1.addWidget(tag_input)
v1.addLayout(h2)
h2.addWidget(add_to_note_btn)
h2.addWidget(delete_to_note_btn)
v1.addWidget(tag_search_btn)
main_line.addLayout(v1)

def create_note_func():
    note_name, ok = QInputDialog.getText(window, "Створення", "Введіть назву")
    if ok == True:
        notes[note_name] = {
                "text": "",
                "tags": []
        }
        notes_list.clear()
        notes_list.addItems(notes)
        with open("notes.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False, indent=4)


def change_note_func():
    key = notes_list.selectedItems()[0].text()
    notes[key]["text"] = text_input.toPlainText()
    with open("notes.json", "w", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False, indent=4)


def note_show():
    key = notes_list.selectedItems()[0].text()
    text_input.setText(notes[key]["text"])
    tags_list.clear()
    tags_list.addItems(notes[key]["tags"])


def delete_notes_func():
    key = notes_list.selectedItems()[0].text()
    text_input.setText("")
    notes_list.clear()
    notes.pop(key)
    notes_list.addItems(notes)
    tags_list.addItems([])


def add_tag():
    tags_name, ok = QInputDialog.getText(window, "Створення","Введіть назву")
    if ok == True:
        selected_items = notes_list.selectedItems()
        if selected_items:
            key = selected_items[0].text()
            notes[key]['tags'].append(tags_name)

def change_tags_func():
    key = tags_list.selectedItems()[0].text()
    notes[key]["tags"] = text_input.toPlainText()
    with open("notes.json", "w", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False, indent=4)





def delete_tags_func():
    key = tags_list.selectedItems()[0].text()
    text_input.setText("")
    tags_list.clear()
    key2 = notes_list.selectedItems()[0].text()
    notes[key2]["tags"].remove(key)
    tags_list.addItems(notes[key2]["tags"])


def search():
    search_element = tag_input.text()
    if search_element == "":
        notes_list.clear()
        notes_list.addItems(notes)
    korzuna = {}
    for zamitka in notes:
        if search_element in notes[zamitka]["tags"]:
            korzuna[zamitka] = notes[zamitka]
            notes_list.clear()
            notes_list.addItems(korzuna)



change_note_btn.clicked.connect(change_note_func)

tag_search_btn.clicked.connect(search)

add_to_note_btn.clicked.connect(add_tag)

delete_to_note_btn.clicked.connect(delete_tags_func)

delete_note_btn.clicked.connect(delete_notes_func)

notes_list.itemClicked.connect(note_show)

create_note_btn.clicked.connect(create_note_func)





window.setLayout(main_line)
window.show()
app.exec()