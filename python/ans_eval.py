import pandas as pd
import torch
from validation import validate

def load_master_answer(master_answer_path):
    df = pd.read_csv(master_answer_path )
    master_answer = df['Answer'].tolist()
    return master_answer


def answer_eval(model_path, device, inference_folder, master_answer_path):

    answers = validate(model_path,device, inference_folder)
    master_answer = load_master_answer(master_answer_path)
    #compare answers with master_answer
    correct = 0
    for i in range(len(answers)):
        if answers[i] == master_answer[i]:
            correct += 1
    print(f"Correct: {correct}/{len(answers)} ({correct/len(answers)*100:.2f}%)")
    return correct/len(answers)*100
    return answers



def main():
    model_path = 'python/models/cnn.pt'
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    inference_folder = 'images/cropped_answers/page_2_cropped'
    master_answer_path = 'csv/master_answers/master_answer1.csv'
    answer_eval(model_path,device, inference_folder,master_answer_path)

if __name__ == '__main__':
    main()
