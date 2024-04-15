import os
from validation import get_answers
from ans_eval import clear_cache

import csv


def export_master_to_csv(filepath):
    # 确保目录存在，如果不存在就创建
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # 获取答案列表
    answers = get_answers()
    
    # 检查文件是否存在，如果不存在则创建并写入头部
    header_needed = not os.path.exists(filepath)
    
    # 打开文件，准备写入
    with open(filepath, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # 如果文件是新创建的，写入CSV的头部
        if header_needed:
            writer.writerow(['Number', 'Answer', 'Weight', 'Part'])
        
        # 遍历答案列表，写入每个答案的数据
        for index, answer in enumerate(answers):
            number = index + 1  # 序号从1开始
            weight = 1  # 默认权重为1
            part = 1    # 默认部分为1
            
            # 写入一行数据
            writer.writerow([number, answer, weight, part])


def main():
    # 导出答案到CSV文件
    export_master_to_csv('csv/master_answers/master_answers.csv')
    
    # 清除缓存
    clear_cache()

if __name__ == '__main__':
    main()