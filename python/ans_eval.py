import os
from validation import validate


def load_master_answer(master_answer_path):
    with open(master_answer_path, 'r') as f:
        master_answer = f.read().splitlines()
    return master_answer


def answer_eval():
    answers = validate('model.pth', 'cuda', 'images/cropped_answers/page_1_cropped')
    master_answer = load_master_answer('data/master_answer.csv')
    #compare answers with master_answer
    correct = 0
    for i in range(len(answers)):
        if answers[i] == master_answer[i]:
            correct += 1
    print(f"Correct: {correct}/{len(answers)} ({correct/len(answers)*100:.2f}%)")
    return correct/len(answers)*100

