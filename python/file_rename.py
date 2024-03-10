import os
import shutil

def rename_files_in_folder(folder_path, first_file_name):
    # 提取文件扩展名
    _, file_extension = os.path.splitext(first_file_name)
    
    # 获取指定文件夹内的所有文件名，不包括子文件夹内的文件
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # 确保文件按照某种逻辑顺序排序
    # 这里我们简单地按照文件名排序，这取决于文件的当前命名
    # 你可能需要根据你的具体情况调整排序逻辑
    files.sort()
    
    # 计算起始编号，假设起始文件名如"1.jpg"意味着起始编号为1
    start_number = 1
    
    # 遍历所有文件，重命名除了第一个文件之外的文件
    for i, file in enumerate(files, start=start_number):
        # 构造新文件名
        new_file_name = f"{i}{file_extension}"
        
        # 如果文件不是起始文件，则重命名
        if file != first_file_name:
            # 构造原始文件和新文件的完整路径
            original_path = os.path.join(folder_path, file)
            new_path = os.path.join(folder_path, new_file_name)
            
            # 重命名文件
            shutil.move(original_path, new_path)
            print(f"Renamed '{file}' to '{new_file_name}'")
        else:
            # 对于起始文件，只更新其名称以反映已经处理过
            print(f"Skipped renaming '{first_file_name}' as it is the starting file.")

# 使用示例
folder_path = '/path/to/your/folder'  # 将此路径替换为你的文件夹路径
first_file_name = '121.jpg'  # 指定第一个文件的名称
rename_files_in_folder(folder_path, first_file_name)
