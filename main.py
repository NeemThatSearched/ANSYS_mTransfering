from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QComboBox, QFileDialog, QMessageBox, QTextEdit
import os
import sqlite3
import json
from module_ansys import extract_materials, save_to_json

def get_prop(material, db_name):
    pass

def check_databases():
    base_path = 'ex_db'
    expected_dbs = 14
    actual_dbs = len([name for name in os.listdir(base_path) if name.endswith('.db')])
    return actual_dbs == expected_dbs

def extract_materials_from_db(db_path):
    materials = []
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT TreeName FROM Table_1Tree WHERE IsFolder=0 AND HasData=1")
    materials = [row[0] for row in cursor.fetchall()]
    conn.close()
    return materials

def extract_materials_from_project(folder_path):
    js = extract_materials(folder_path)
    materials = [i["name"] for i in js]
    return materials

class MaterialExtractorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Material Extractor")
        self.setGeometry(100, 100, 800, 600)

        if not check_databases():
            QMessageBox.critical(self, "Ошибка", "Некоторые базовые базы данных отсутствуют.")
            self.close()
            return

        main_layout = QHBoxLayout()

        project_widget = QWidget()
        project_layout = QVBoxLayout()

        self.db_combo = QComboBox()
        self.db_combo.addItems(self.get_databases())
        self.db_combo.currentIndexChanged.connect(self.on_db_selected)
        project_layout.addWidget(self.db_combo)

        self.materials_list = QListWidget()
        project_layout.addWidget(self.materials_list)

        button_layout = QHBoxLayout()
        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.clear_materials)
        button_layout.addWidget(self.clear_button)

        self.select_all_button = QPushButton("Выбрать все")
        self.select_all_button.clicked.connect(self.select_all)
        button_layout.addWidget(self.select_all_button)

        self.convert_button = QPushButton("Конвертировать")
        self.convert_button.clicked.connect(self.convert)
        button_layout.addWidget(self.convert_button)

        project_layout.addLayout(button_layout)
        project_widget.setLayout(project_layout)

        # Log area
        log_widget = QWidget()
        log_layout = QVBoxLayout()

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)

        log_widget.setLayout(log_layout)

        main_layout.addWidget(project_widget)
        main_layout.addWidget(log_widget)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.materials = []

    def get_databases(self):
        base_path = 'ex_db'
        return [name for name in os.listdir(base_path) if name.endswith('.db')] + ["Пользовательский проект"]

    def on_db_selected(self):
        selected_db = self.db_combo.currentText()
        if selected_db == "Пользовательский проект":
            folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку")
            if folder_path:
                materials = extract_materials_from_project(folder_path)
                self.log(folder_path)
                self.update_materials_list(materials, folder_path)
        else:
            db_path = os.path.join('ex_db', selected_db)
            materials = extract_materials_from_db(db_path)
            self.update_materials_list(materials, selected_db)

    def update_materials_list(self, materials, source):
        self.materials = [{'name': material, 'source': source} for material in materials]
        for material in materials:
            self.materials_list.addItem(material)

    def clear_materials(self):
        self.materials_list.clear()
        self.materials.clear()
        self.log("Список очищен.")

    def select_all(self):
        for index in range(self.materials_list.count()):
            item = self.materials_list.item(index)
            item.setSelected(True)
        self.log("Все материалы выбраны.")

    def convert(self):
        selected_items = self.materials_list.selectedItems()
        selected_materials = [self.materials[self.materials_list.row(item)] for item in selected_items]
        ans = []
        for el in selected_materials:
            if el["source"].endswith('.db'):
                ans.append(get_prop(el["name"], el["source"]))
            else:
                js = extract_materials(el["source"])
                for sub_el in js:
                    if sub_el["name"] == el["name"]:
                        ans.append(sub_el)
        save_to_json(ans, "out.json")
        self.log(f"Конвертация завершена для: {selected_materials}.\n\n Все сохранено в файл out.json")

    def log(self, message):
        self.log_text.append(message)

if __name__ == "__main__":
    app = QApplication([])
    window = MaterialExtractorApp()
    window.show()
    app.exec_()
