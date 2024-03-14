import os
import shutil

def move_subfolders_content_to_first_subfolder(folder_path):
    # 确保提供的路径存在
    if not os.path.exists(folder_path):
        print(f"The path {folder_path} does not exist.")
        return

    # 获取所有子目录
    subfolders = [os.path.join(folder_path, o) for o in os.listdir(folder_path) 
                  if os.path.isdir(os.path.join(folder_path,o))]
    subfolders.sort()

    # 检查是否有至少两个子文件夹
    if len(subfolders) < 2:
        print("There are not enough subfolders to move content.")
        return

    # 第一个子文件夹的路径
    first_subfolder = subfolders[0]

    # 遍历其余的子文件夹，并将它们的内容移动到第一个子文件夹中
    for subfolder in subfolders[1:]:
        for item in os.listdir(subfolder):
            source = os.path.join(subfolder, item)
            destination = os.path.join(first_subfolder, item)
            
            # 检查目标路径是否已存在文件/文件夹
            if os.path.exists(destination):
                print(f"Cannot move {source} because {destination} already exists.")
                continue
            
            # 移动文件或文件夹
            shutil.move(source, destination)
            print(f"Moved {source} to {destination}")

    print("All contents have been moved to the first subfolder.")

# 使用示例
folder_path = "images/cropped_id"  # 替换为实际文件夹路径
move_subfolders_content_to_first_subfolder(folder_path)
