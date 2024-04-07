import pandas as pd
import torch
import os
from collections import defaultdict
from validation import get_answers, get_id
import shutil
import glob



def load_master_answers(master_answers_folder):
    master_dfs = []  # 用于存储所有master答案DataFrame的列表
    for file_name in glob.glob(os.path.join(master_answers_folder, '*.csv')):
        df = pd.read_csv(file_name)
        master_dfs.append(df)
    return master_dfs






def calculate_part_correct_and_total(answers, master_df):
    part_correct = defaultdict(int)  # Default to 0 for each part for correct answers
    part_total = defaultdict(int)  # Default to 0 for each part for total questions
    for i, ans in enumerate(answers):
        if i < len(master_df):
            part = master_df.iloc[i]['Part']
            part_total[part] += 1  # Increment total question count for the part
            if ans == master_df.iloc[i]['Answer']:
                part_correct[part] += 1  # Increment correct answer count for the part
    return part_correct, part_total






def format_answers(answers, master_df):
    formatted_answers = []
    for i, ans in enumerate(answers):
        if i < len(master_df):
            master_ans = master_df.iloc[i]['Answer']
            formatted_answers.append(ans.upper() if ans == master_ans else ans.lower())
    return ''.join(formatted_answers)






def answer_eval(ans_model_path, id_model_path, device, ans_inference_base_folder, id_inference_base_folder, master_answers_folder):
    results = []
    # 获取答案和ID文件夹中所有子文件夹的名称
    ans_folders = sorted([f for f in os.listdir(ans_inference_base_folder) if os.path.isdir(os.path.join(ans_inference_base_folder, f))])
    id_folders = sorted([f for f in os.listdir(id_inference_base_folder) if os.path.isdir(os.path.join(id_inference_base_folder, f))])

    # 遍历所有的master答案文件
    for master_answer_path in os.listdir(master_answers_folder):
        if master_answer_path.endswith('.csv'):
            master_df = pd.read_csv(os.path.join(master_answers_folder, master_answer_path))  # 加载单个答案文件
            total_weight = master_df['Weight'].sum()  # 计算总权重
            
            # 遍历对应的答案和ID文件夹
            for ans_folder_name, id_folder_name in zip(ans_folders, id_folders):
                # 构建完整路径
                ans_folder = os.path.join(ans_inference_base_folder, ans_folder_name)
                id_folder = os.path.join(id_inference_base_folder, id_folder_name)
                
                # 获取答案和ID
                answers = get_answers(ans_model_path, device, ans_folder)
                id = get_id(id_model_path, device, id_folder)
                id = ''.join(str(i) for i in id)

                formatted_answers = format_answers(answers, master_df)
                part_correct, part_total = calculate_part_correct_and_total(answers, master_df)

                # 计算总分和错误的题号
                total_score = 0
                incorrect_numbers = []
                for i, ans in enumerate(answers):
                    if i < len(master_df):
                        question_number = master_df.iloc[i]['Number']
                        if ans == master_df.iloc[i]['Answer']:
                            total_score += master_df.iloc[i]['Weight']
                        else:
                            incorrect_numbers.append(str(question_number))

                grade = (total_score / total_weight) * 100 if total_weight > 0 else 0
                incorrect_answers_str = ';'.join(incorrect_numbers)

                accuracy = sum(part_correct.values()) / sum(part_total.values()) * 100 if sum(part_total.values()) > 0 else 0
                result = {
                    "ID": id,
                    "Correct": sum(part_correct.values()),
                    "Total": sum(part_total.values()),
                    "Accuracy": f"{accuracy:.1f}%",
                    "Grade": f"{grade:.2f}%",
                    "Answers": formatted_answers,
                    "Incorrect_Answers": incorrect_answers_str
                }

                for part, total in part_total.items():
                    result[f"Part_{part}"] = f"{part_correct[part]}/{total}"

                results.append(result)
                print(f"Page: {ans_folder_name} | ID: {id} | Correct: {result['Correct']}/{result['Total']} | Grade: {result['Grade']} | Incorrect Answers: {result['Incorrect_Answers']}")
    
    
    return results




def clear_cache():
    folders = [
        'images/cropped_answers',
        'images/cropped_id',
        'csv/master_answers',
        'pdf'
    ]
    for folder in folders:
        shutil.rmtree(folder)
        os.makedirs(folder)
    print("Cache cleared successfully.")




def export_results_to_csv(results, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    csv_file_path = os.path.join(output_path, 'student_scores.csv')
    
    # 创建DataFrame之前先对results按ID排序
    # 确保ID列为字符串类型，以便正确解析数字
    sorted_results = sorted(results, key=lambda x: int(x['ID']))
    
    # 如果需要特定的列顺序，可以在这里指定
    columns_order = ['ID'] + [col for col in sorted_results[0] if col != 'ID']
    
    # 创建DataFrame时指定列的顺序
    df = pd.DataFrame(sorted_results, columns=columns_order)
    df.to_csv(csv_file_path, index=False)
    print(f"Results exported to {csv_file_path}")   

    clear_cache()






def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    ans_model_path = 'python/models/cnn_enhanced.pt'
    id_model_path = 'python/models/cnn_id.pt'
    ans_inference_base_folder = 'images/cropped_answers'
    id_inference_base_folder = 'images/cropped_id'
    master_answers_folder = 'csv/master_answers'  # 更改为文件夹路径
    output_path = 'csv/output'

    results = answer_eval(ans_model_path, id_model_path, device, ans_inference_base_folder, id_inference_base_folder, master_answers_folder)
    export_results_to_csv(results, output_path)




if __name__ == '__main__':
    main()