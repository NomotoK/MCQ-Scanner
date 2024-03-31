import pandas as pd
import torch
import os
from validation import get_answers, get_id

def load_master_answer(master_answer_path):
    df = pd.read_csv(master_answer_path)
    return df

def format_answers_by_part(answers, master_answers_df):
    # 初始化各部分的答案列表
    parts_answers = {f"Part_{i+1}": [] for i in range(master_answers_df['Part'].max())}
    
    for index, row in master_answers_df.iterrows():
        part_key = f"Part_{row['Part']}"
        if index < len(answers):
            answer = answers[index]
            formatted_answer = answer.upper() if answer == row['Answer'] else answer.lower()
            parts_answers[part_key].append(formatted_answer)
    
    # 将各部分答案列表转换为字符串
    for key, value in parts_answers.items():
        parts_answers[key] = ''.join(value)
    
    return parts_answers

def answer_eval(ans_model_path, id_model_path, device, ans_inference_base_folder, id_inference_base_folder, master_answer_path):
    results = []
    master_answers_df = load_master_answer(master_answer_path)
    page_num = 1
    while True:
        ans_folder = os.path.join(ans_inference_base_folder, f'page_{page_num}')
        id_folder = os.path.join(id_inference_base_folder, f'page_{page_num}')
        if not os.path.exists(ans_folder) or not os.path.exists(id_folder):
            break
        
        answers = get_answers(ans_model_path, device, ans_folder)
        id = get_id(id_model_path, device, id_folder)
        id = ''.join(str(i) for i in id)

        parts_answers = format_answers_by_part(answers, master_answers_df)
        correct_count = sum(1 for i, ans in enumerate(answers) if i < len(master_answers_df) and ans == master_answers_df.at[i, 'Answer'])
        score = correct_count / len(answers) * 100 if answers else 0
        score = round(score, 1)
        result = {
            "ID": id, 
            "Correct": correct_count, 
            "Total": len(answers), 
            "Score": score
        }
        result.update(parts_answers)
        results.append(result)
        
        print(f"Processed: {ans_folder} | ID: {id} Correct: {correct_count}/{len(answers)} Score: {score:.2f}%")
        
        page_num += 1
    
    return results

def export_results_to_csv(results, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    csv_file_path = os.path.join(output_path, 'student_scores.csv')
    df = pd.DataFrame(results)
    df.to_csv(csv_file_path, index=False)
    print(f"Results exported to {csv_file_path}")

def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    ans_model_path = 'python/models/cnn.pt'
    id_model_path = 'python/models/cnn_id.pt'
    ans_inference_base_folder = 'images/cropped_answers'
    id_inference_base_folder = 'images/cropped_id'
    master_answer_path = 'csv/master_answers/master_answer1.csv'
    output_path = 'csv/output'

    results = answer_eval(ans_model_path, id_model_path, device, ans_inference_base_folder, id_inference_base_folder, master_answer_path)
    export_results_to_csv(results, output_path)

if __name__ == '__main__':
    main()
