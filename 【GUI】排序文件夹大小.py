import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QFileDialog, QAbstractItemView, QMenu, QAction
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDragEnterEvent, QDropEvent

class FolderSizeTool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("文件夹大小排序工具")
        self.setGeometry(100, 100, 800, 600)

        self.folder_path = ""
        self.folder_data = []  # 存储文件夹及其大小数据

        # UI布局
        self.init_ui()

    def init_ui(self):
        # 创建布局
        layout = QVBoxLayout()

        # 输入路径的文本框
        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText("拖拽文件夹或输入路径")
        layout.addWidget(self.path_input)

        # 创建显示排序结果的表格
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["文件夹/文件名", "大小 (字节)"])

        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止编辑
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 行选择
        self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)  # 单选模式

        # 按钮
        self.sort_button = QPushButton("排序", self)
        self.sort_button.setStyleSheet("border-radius: 10px; background-color: #4CAF50; color: white; font-size: 16px; padding: 10px;")
        self.sort_button.clicked.connect(self.sort_data)
        layout.addWidget(self.sort_button)

        # 将表格添加到布局
        layout.addWidget(self.table_widget)

        # 设置窗口的中央小部件
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 支持拖拽
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        # 获取拖拽的路径
        url = event.mimeData().urls()[0].toLocalFile()
        if os.path.isdir(url):
            self.folder_path = url
            self.path_input.setText(url)
            self.clear_and_sort_data(url)

    def clear_and_sort_data(self, path):
        self.folder_data.clear()
        self.populate_data(path)
        self.update_table()

    def populate_data(self, path):
        # 获取该路径下所有文件夹和文件，并计算大小
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                size = self.get_folder_size(item_path)
            else:
                size = os.path.getsize(item_path)
            self.folder_data.append((item, size))

    def get_folder_size(self, folder_path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                total_size += os.path.getsize(file_path)
        return total_size

    def update_table(self):
        # 更新表格内容
        self.table_widget.setRowCount(len(self.folder_data))
        for row, (name, size) in enumerate(self.folder_data):
            self.table_widget.setItem(row, 0, QTableWidgetItem(name))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(size)))

    def sort_data(self):
        # 排序并更新表格
        if not self.folder_data:
            return
        self.folder_data.sort(key=lambda x: x[1], reverse=True)
        self.update_table()

    def header_clicked(self, index):
        # 点击表头时，按列进行排序
        if index == 0:  # 按名称排序
            self.folder_data.sort(key=lambda x: x[0], reverse=False)
        elif index == 1:  # 按大小排序
            self.folder_data.sort(key=lambda x: x[1], reverse=False)
        self.update_table()


app = QApplication(sys.argv)
window = FolderSizeTool()
window.show()
sys.exit(app.exec_())
