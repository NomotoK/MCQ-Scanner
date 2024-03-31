import pandas as pd
import torch
from validation import get_answers,get_id

def load_master_answer(master_answer_path):
    df = pd.read_csv(master_answer_path )
    master_answer = df['Answer'].tolist()
    return master_answer


def answer_eval(ans_model_path, id_model_path, device, ans_inference_folder, id_inference_folder, master_answer_path):

    answers = get_answers(ans_model_path,device, ans_inference_folder)
    id = get_id(id_model_path,device, id_inference_folder)
    id = ''.join(str(i) for i in id)

    master_answer = load_master_answer(master_answer_path)
    #compare answers with master_answer
    correct = 0
    for i in range(len(answers)):
        if answers[i] == master_answer[i]:
            correct += 1
    print(f" ID: {id} Correct: {correct}/{len(answers)} acc: ({correct/len(answers)*100:.2f}%)")
    acc = correct/len(answers)*100
    return answers,id,acc


def write_to_csv(answers,id,acc):
    df = pd.DataFrame({'ID': [id],  'Accuracy': [acc], 'Answer': [answers]})
    df.to_csv('csv/eval.csv', index=False)



def main():
    ans_model_path = 'python/models/cnn.pt'
    id_model_path = 'python/models/cnn_id.pt'
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    ans_inference_folder = 'images/cropped_answers/page_2_cropped'
    id_inference_folder = 'images/cropped_id/page_2_id'
    master_answer_path = 'csv/master_answers/master_answer1.csv'
    answer_eval(ans_model_path,id_model_path, device, ans_inference_folder, id_inference_folder, master_answer_path)


if __name__ == '__main__':
    main()
