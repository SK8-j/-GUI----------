import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QFileDialog, QAbstractItemView, QMenu, QAction, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QColor

class FolderSizeTool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Folder Size Tool")
        self.setGeometry(100, 100, 800, 600)
        self.setAcceptDrops(True)

        self.layout = QVBoxLayout()

        # 输入框和按钮
        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText("Drag and drop a folder here or paste a path")
        self.path_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ccc;")
        self.path_input.setFixedHeight(40)
        self.layout.addWidget(self.path_input)

        # 按钮
        self.button = QPushButton("Start Sorting", self)
        self.button.setStyleSheet("border-radius: 10px; background-color: #4CAF50; color: white; padding: 10px;")
        self.button.clicked.connect(self.process_path)
        self.layout.addWidget(self.button)

        # 表格
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)  # 2列：名称和大小
        self.table.setHorizontalHeaderLabels(["Name", "Size (bytes)"])
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setStyleSheet("""
            QTableWidget {
                border: none;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #f2f2f2;
                padding: 5px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
            }
        """)
        self.layout.addWidget(self.table)

        # 排序筛选器
        self.filter_layout = QHBoxLayout()

        self.sort_by_combo = QComboBox(self)
        self.sort_by_combo.addItem("Sort by Name")
        self.sort_by_combo.addItem("Sort by Size")
        self.sort_by_combo.currentIndexChanged.connect(self.sort_table)
        self.filter_layout.addWidget(self.sort_by_combo)

        self.order_combo = QComboBox(self)
        self.order_combo.addItem("Ascending")
        self.order_combo.addItem("Descending")
        self.order_combo.currentIndexChanged.connect(self.sort_table)
        self.filter_layout.addWidget(self.order_combo)

        self.layout.addLayout(self.filter_layout)

        # 主界面设置
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def process_path(self):
        path = self.path_input.text().strip()
        if os.path.exists(path):
            self.clear_table()
            self.load_directory(path)

    def load_directory(self, path):
        # 获取路径下的所有文件夹和文件
        items = [(name, os.path.getsize(os.path.join(path, name))) for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) or os.path.isfile(os.path.join(path, name))]
        
        # 更新表格
        self.table.setRowCount(len(items))
        for row, (name, size) in enumerate(items):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(str(size)))

        self.sort_table()  # 默认按选择的排序规则进行排序

    def sort_table(self):
        sort_by = self.sort_by_combo.currentText()  # 按名称还是按大小排序
        order = self.order_combo.currentText()  # 升序或降序
        
        column = 0 if sort_by == "Sort by Name" else 1  # 根据选择的排序类型确定列
        order_flag = Qt.AscendingOrder if order == "Ascending" else Qt.DescendingOrder
        
        # 排序
        self.table.sortItems(column, order_flag)

    def clear_table(self):
        self.table.setRowCount(0)  # 清空表格

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            folder_path = urls[0].toLocalFile()
            self.path_input.setText(folder_path)
            self.process_path()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FolderSizeTool()
    window.show()
    sys.exit(app.exec_())
