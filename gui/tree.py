import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QFormLayout, QGroupBox, QPushButton, QLabel, QLineEdit, QTextEdit, 
                             QMessageBox, QHBoxLayout, QDialog, QDialogButtonBox, QMenuBar, QAction, QMainWindow, QFileDialog)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter, QImage, QPen
from PyQt5.QtCore import Qt, QPoint

class Individual:
    def __init__(self, name, birthdate):
        self.name = name
        self.birthdate = birthdate
        self.children = []

    def add_child(self, child):
        self.children.append(child)

class FamilyTree:
    def __init__(self, root_name, root_birthdate):
        self.root = Individual(root_name, root_birthdate)

    def add_child(self, parent_name, child):
        parent = self.find_individual(self.root, parent_name)
        if parent:
            parent.add_child(child)
            return True
        return False

    def find_individual(self, node, name):
        if node.name == name:
            return node
        for child in node.children:
            found = self.find_individual(child, name)
            if found:
                return found
        return None

    def delete_member(self, name):
        if self.root.name == name:
            return False  # Cannot delete the root
        return self._delete_member(self.root, name)

    def _delete_member(self, parent, name):
        for child in parent.children:
            if child.name == name:
                parent.children.remove(child)
                return True
            if self._delete_member(child, name):
                return True
        return False

    def visualize_tree(self, node, prefix="", is_left=True):
        if node:
            result = prefix
            result += "├── " if is_left else "└── "
            result += f"{node.name} ({node.birthdate})\n"
            for i, child in enumerate(node.children):
                next_prefix = prefix + ("│   " if is_left else "    ")
                result += self.visualize_tree(child, next_prefix, i < len(node.children) - 1)
            return result
        return ""

class InputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Welcome to Family Tree Generator')
        self.setGeometry(100, 100, 400, 200)
        self.setWindowIcon(QIcon('icon.png'))

        layout = QVBoxLayout()

        message_label = QLabel("Hello, welcome to the family tree generator app!\nPlease enter your name and birthdate to generate your family tree:")
        message_label.setWordWrap(True)
        layout.addWidget(message_label)

        self.form_layout = QFormLayout()
        self.name_input = QLineEdit(self)
        self.birthdate_input = QLineEdit(self)

        self.form_layout.addRow("Your Name:", self.name_input)
        self.form_layout.addRow("Your Birthdate:", self.birthdate_input)
        layout.addLayout(self.form_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.button_box)
        self.setLayout(layout)

        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
                font-size: 17px;
            }
            QLabel {
                font-weight: bold;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QDialogButtonBox {
                padding: 10px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def get_inputs(self):
        return self.name_input.text(), self.birthdate_input.text()

class FamilyTreeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        name, birthdate = self.show_input_dialog()
        if name and birthdate:
            self.family_tree = FamilyTree(name, birthdate)
        else:
            sys.exit()

    def show_input_dialog(self):
        dialog = InputDialog()
        if dialog.exec_() == QDialog.Accepted:
            return dialog.get_inputs()
        return None, None

    def initUI(self):
        self.setWindowTitle('Family Tree Generator')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('icon.png'))

        layout = QVBoxLayout()
        
        self.menu_bar = QMenuBar(self)
        self.actions_menu = self.menu_bar.addMenu('Options')
        
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_tree)
        self.actions_menu.addAction(save_action)
        
        start_over_action = QAction('Start Over', self)
        start_over_action.triggered.connect(self.start_over)
        self.actions_menu.addAction(start_over_action)
        
        layout.setMenuBar(self.menu_bar)
        
        self.form_group_box = QGroupBox("Add Family Member")
        form_layout = QFormLayout()
        self.name_input = QLineEdit(self)
        self.child_name_input = QLineEdit(self)
        self.birthdate_input = QLineEdit(self)

        form_layout.addRow(QLabel("Enter parent's name:"), self.name_input)
        form_layout.addRow(QLabel("Enter child's name:"), self.child_name_input)
        form_layout.addRow(QLabel("Enter child's birthdate:"), self.birthdate_input)

        self.form_group_box.setLayout(form_layout)
        
        self.add_button = QPushButton('Add Family Member', self)
        # self.add_button.setIcon(QIcon('icon.png'))
        self.add_button.clicked.connect(self.add_family_member)

        self.delete_group_box = QGroupBox("Delete Family Member")
        delete_form_layout = QFormLayout()
        self.delete_name_input = QLineEdit(self)
        delete_form_layout.addRow(QLabel("Enter member's name to delete:"), self.delete_name_input)
        self.delete_group_box.setLayout(delete_form_layout)

        self.delete_button = QPushButton('Delete Family Member', self)
        # self.delete_button.setIcon(QIcon('icon.png'))
        self.delete_button.clicked.connect(self.delete_family_member)
        
        self.visualize_button = QPushButton('Visualize Family Tree', self)
        # self.visualize_button.setIcon(QIcon('icon.png'))
        self.visualize_button.clicked.connect(self.visualize_tree)

        self.result_text = QTextEdit(self)
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont('Courier', 10))

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.visualize_button)

        layout.addWidget(self.form_group_box)
        layout.addWidget(self.delete_group_box)
        layout.addLayout(button_layout)
        layout.addWidget(self.result_text)

        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                font-size: 20px;
            }
            QPushButton {
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid gray;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 3px;
            }
            QTextEdit {
                background-color: #f0f0f0;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QDialogButtonBox {
                padding: 10px;
            }
        """)

    def add_family_member(self):
        parent_name = self.name_input.text().strip()
        child_name = self.child_name_input.text().strip()
        child_birthdate = self.birthdate_input.text().strip()

        if parent_name and child_name and child_birthdate:
            child = Individual(child_name, child_birthdate)
            if self.family_tree.add_child(parent_name, child):
                QMessageBox.information(self, 'Success', 'Family member added successfully.')
            else:
                QMessageBox.warning(self, 'Error', 'Parent not found in the family tree. Please check the name.')
        else:
            QMessageBox.warning(self, 'Error', 'All fields are required.')

    def delete_family_member(self):
        member_name = self.delete_name_input.text().strip()

        if member_name:
            if self.family_tree.delete_member(member_name):
                QMessageBox.information(self, 'Success', 'Family member deleted successfully.')
            else:
                QMessageBox.warning(self, 'Error', 'Member not found in the family tree. Please check the name.')
        else:
            QMessageBox.warning(self, 'Error', 'Member name is required.')

    def visualize_tree(self):
        tree_representation = self.family_tree.visualize_tree(self.family_tree.root)
        self.result_text.clear()
        self.result_text.append(tree_representation)

    def save_tree(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Family Tree", "", "PNG Files (*.png)")
        if file_path:
            pixmap = QPixmap(self.result_text.viewport().size())
            self.result_text.viewport().render(pixmap)
            pixmap.save(file_path)
            QMessageBox.information(self, 'Success', f'Family tree saved as {file_path}')

    def start_over(self):
        name, birthdate = self.show_input_dialog()
        if name and birthdate:
            self.family_tree = FamilyTree(name, birthdate)
            self.result_text.clear()
        else:
            sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tree_app = FamilyTreeApp()
    tree_app.show()
    sys.exit(app.exec_())
