import os
import shutil

def get_folder_size(folder_path):
    """
    计算文件夹的大小
    :param folder_path: 文件夹路径
    :return: 文件夹的大小（以字节为单位）
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # 跳过链接文件，避免计算错误的文件大小
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

# 指定目录
directory = r'E:\微信存储\WeChat Files\wxid_82d0w87fvwlv22\FileStorage\MsgAttach'

# 获取目录下的所有文件夹
folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

# 计算每个文件夹的大小并存储在列表中
folder_sizes = []
for folder in folders:
    folder_path = os.path.join(directory, folder)
    size = get_folder_size(folder_path)
    folder_sizes.append((folder, size))

# 按大小排序文件夹
folder_sizes.sort(key=lambda x: x[1], reverse=True)

# 打印排序后的文件夹及其大小
for folder, size in folder_sizes:
    print(f"文件夹：{folder}，大小：{size} 字节")