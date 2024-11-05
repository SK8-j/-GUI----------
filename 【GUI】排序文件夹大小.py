import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QFileDialog, QAbstractItemView, QMenu, QAction
from PyQt5.QtCore import Qt, QUrl

class FolderSizeTool(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化UI
        self.setWindowTitle("文件夹排序工具")
        self.setGeometry(100, 100, 800, 600)

        # 布局
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # 输入路径框
        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText("拖拽文件夹到这里，或手动输入路径")
        self.layout.addWidget(self.path_input)

        # 排序结果表格
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

        # 重置按钮
        self.reset_button = QPushButton("重置", self)
        self.layout.addWidget(self.reset_button)

        # 连接按钮事件
        self.reset_button.clicked.connect(self.reset)

        # 设置拖拽功能
        self.setAcceptDrops(True)

        self.current_path = None

    def reset(self):
        """重置排序结果"""
        self.table.clear()
        self.path_input.clear()

    def dragEnterEvent(self, event):
        """启用拖拽进入事件"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """处理拖拽释放事件"""
        if event.mimeData().hasUrls():
            # 获取拖拽的路径
            path = event.mimeData().urls()[0].toLocalFile()
            if os.path.isdir(path):
                self.current_path = path
                self.path_input.setText(path)  # 显示路径
                self.process_directory(path)

    def process_directory(self, path):
        """计算文件夹下一级的所有文件和文件夹，并显示排序结果"""
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["名称", "大小 (字节)"])

        items = []

        # 获取路径下一级的所有文件和文件夹
        for item_name in os.listdir(path):
            item_path = os.path.join(path, item_name)
            if os.path.isdir(item_path):
                size = self.get_folder_size(item_path)
            elif os.path.isfile(item_path):
                size = os.path.getsize(item_path)
            else:
                continue

            items.append((item_name, size))

        # 按照大小排序
        items.sort(key=lambda x: x[1])

        # 填充表格
        for i, (name, size) in enumerate(items):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(name))
            self.table.setItem(i, 1, QTableWidgetItem(str(size)))

    def get_folder_size(self, folder_path):
        """计算文件夹大小"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FolderSizeTool()
    window.show()
    sys.exit(app.exec_())
