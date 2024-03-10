import os

def rename_images(folder_path, start_number):
    # 检查文件夹路径是否存在
    if not os.path.isdir(folder_path):
        print(f"The specified folder does not exist: {folder_path}")
        return

    # 获取所有jpg文件，并按文件名排序
    files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    files.sort(key=lambda x: int(x.split('.')[0]))  # 假设文件名完全是数字加.jpg

    # 重命名文件
    for i, file in enumerate(files, start=start_number):
        new_name = f"{i}.jpg"
        old_path = os.path.join(folder_path, file)
        new_path = os.path.join(folder_path, new_name)
        
        # 重命名操作
        os.rename(old_path, new_path)
        print(f"Renamed {file} to {new_name}")

# 使用示例
folder_path = "images/cropped_answers/page_10_cropped"  # 替换为实际文件夹路径
start_number = 1081  # 从此数字开始重命名
rename_images(folder_path, start_number)
