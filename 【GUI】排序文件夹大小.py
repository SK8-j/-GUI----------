import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QFileDialog, QAbstractItemView, QMenu, QAction
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QColor


class FolderSizeTool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("文件夹大小排序工具")
        self.setGeometry(100, 100, 800, 600)

        self.folder_path = ""
        self.folder_data = []  # 存储文件夹及其大小数据
        self.sort_order = Qt.AscendingOrder  # 初始排序为升序

        # UI布局
        self.init_ui()

    def init_ui(self):
        # 主窗口的中央小部件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # 输入路径框
        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText("拖拽或输入路径")
        layout.addWidget(self.path_input)

        # 拖拽区
        self.setAcceptDrops(True)

        # 排序按钮
        self.sort_button = QPushButton("重新排序", self)
        self.sort_button.setStyleSheet("QPushButton {border-radius: 10px; background-color: #4CAF50; color: white; padding: 10px 20px;} QPushButton:hover {background-color: #45a049;}")
        self.sort_button.clicked.connect(self.sort_folders)
        layout.addWidget(self.sort_button)

        # 表格展示
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)  # 两列: 文件夹/文件名 和 大小
        self.table.setHorizontalHeaderLabels(["文件夹/文件名", "大小 (MB)"])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(0)  # 文件夹列自适应
        self.table.horizontalHeader().sectionClicked.connect(self.handle_header_click)  # 表头点击事件
        layout.addWidget(self.table)

        # 右键菜单
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

    def handle_header_click(self, index):
        """处理表头点击事件"""
        if index == 0:
            # 按文件夹/文件名排序
            self.folder_data.sort(key=lambda x: x[0], reverse=self.sort_order == Qt.DescendingOrder)
        elif index == 1:
            # 按大小排序
            self.folder_data.sort(key=lambda x: x[1], reverse=self.sort_order == Qt.DescendingOrder)

        # 切换排序顺序
        self.sort_order = Qt.DescendingOrder if self.sort_order == Qt.AscendingOrder else Qt.AscendingOrder

        # 更新表格显示
        self.display_folder_data()

    def dragEnterEvent(self, event):
        """处理拖拽进入事件"""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """处理拖拽放下事件"""
        urls = event.mimeData().urls()
        if urls:
            folder_path = urls[0].toLocalFile()
            self.path_input.setText(folder_path)
            self.load_folder_data(folder_path)

    def load_folder_data(self, path):
        """加载文件夹数据并计算大小"""
        self.folder_path = path
        self.folder_data.clear()  # 清空之前的数据
        self.table.setRowCount(0)  # 清空表格

        try:
            # 获取路径下的所有文件和文件夹
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    size = self.get_folder_size(item_path)
                elif os.path.isfile(item_path):
                    size = os.path.getsize(item_path) / (1024 * 1024)  # 转换为MB
                else:
                    continue
                self.folder_data.append((item, size))
            
            self.display_folder_data()  # 显示数据
        except Exception as e:
            print(f"加载文件夹数据失败: {e}")

    def get_folder_size(self, folder):
        """递归计算文件夹的大小"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder):
            for f in filenames:
                filepath = os.path.join(dirpath, f)
                total_size += os.path.getsize(filepath)
        return total_size / (1024 * 1024)  # 转换为MB

    def display_folder_data(self):
        """将文件夹数据展示在表格中"""
        self.table.setRowCount(len(self.folder_data))
        for i, (name, size) in enumerate(self.folder_data):
            self.table.setItem(i, 0, QTableWidgetItem(name))
            self.table.setItem(i, 1, QTableWidgetItem(f"{size:.2f}"))

    def sort_folders(self):
        """按文件夹大小排序"""
        self.folder_data.sort(key=lambda x: x[1])
        self.display_folder_data()

    def show_context_menu(self, pos):
        """右键菜单"""
        menu = QMenu(self)

        reset_action = QAction("重置", self)
        reset_action.triggered.connect(self.reset_path)
        menu.addAction(reset_action)

        delete_action = QAction("删除", self)
        delete_action.triggered.connect(self.delete_path)
        menu.addAction(delete_action)

        menu.exec_(self.table.mapToGlobal(pos))

    def reset_path(self):
        """重置路径和数据"""
        self.path_input.clear()
        self.folder_data.clear()
        self.table.setRowCount(0)

    def delete_path(self):
        """删除路径"""
        try:
            if self.folder_path:
                shutil.rmtree(self.folder_path)
                self.reset_path()
                print(f"已删除路径: {self.folder_path}")
        except Exception as e:
            print(f"删除路径失败: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FolderSizeTool()
    window.show()
    sys.exit(app.exec_())
