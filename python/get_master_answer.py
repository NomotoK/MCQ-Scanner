import os
import pandas as pd
import torch
import shutil
from validation import get_answers
import crop_pdf_input



def create_master_answer(path):
    # 创建一个DataFrame，包含所需的列和行
    data = {
        "Number": range(1, 121),  # 生成1到120的数字
        "Answer": [''] * 120,     # 初始化为空字符串的列表
        "Weight": [1] * 120,      # 初始化权重为1
        "Part": [1] * 120         # 初始化部分为1
    }
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    # 保存到指定路径的CSV文件
    df.to_csv(path, index=False)





def export_master_to_csv(path, answers):
    # 读取现有的CSV文件
    df = pd.read_csv(path)
    # 更新"Answer"列
    df['Answer'] = answers
    # 再次保存到CSV
    df.to_csv(path, index=False)





def process_files_in_subfolder(base_path, master_csv_path, model_path, device):
    subfolder_path = next(os.walk(base_path))[1][0]  # 获取第一个子文件夹的路径
    full_subfolder_path = os.path.join(base_path, subfolder_path)
    
    # 从get_answers函数获取答案列表
    answers = get_answers(model_path, device, full_subfolder_path)
    
    # 更新CSV文件的路径
    csv_file_path = master_csv_path
    export_master_to_csv(csv_file_path, answers)



def clear_cache():
    folders = [
        'images/cropped_answers',
        'images/cropped_id',
        'pdf_master'
    ]
    for folder in folders:
        shutil.rmtree(folder)
        os.makedirs(folder)
    print("Cache cleared successfully.")



def main():
    master_csv_path = 'csv/master_answers/master_answer.csv'
    base_path = 'images/cropped_answers'
    ans_model_path = 'python/models/cnn_enhanced.pt' 
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # 导出答案到CSV文件
    create_master_answer(master_csv_path)
    crop_pdf_input.main('pdf_master')
    process_files_in_subfolder(base_path, master_csv_path, ans_model_path, device)
    clear_cache()



if __name__ == '__main__':
    main()