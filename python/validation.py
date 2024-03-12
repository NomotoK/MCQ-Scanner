import os
import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from PIL import Image
from models import CNN


def load_model(model_path):
    model = CNN()
    model.load_state_dict(torch.load(model_path))
    model.eval()  # 切换到评估模式
    return model



def predict_image(model, device, image_path, transform):
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)  # 增加一个批处理维度
    image = image.to(device)
    
    with torch.no_grad():
        output = model(image)
        pred = output.argmax(dim=1, keepdim=True)  # 获取最大概率的索引
    return pred.item()




def validate(model_path,device, inference_folder):  
    model = load_model(model_path)
    model.to(device)
    
    # 设置数据加载器
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((130, 24)),
        transforms.ToTensor(),
    ])

    filenames = sorted(os.listdir(inference_folder))
    filenames = sorted(filenames, key=lambda x: int(os.path.splitext(x)[0]))
    answers = []    

    for filename in filenames:
        image_path = os.path.join(inference_folder, filename)
        prediction = predict_image(model, device, image_path, transform)
        answer_name = ['A', 'B', 'C', 'D', 'E']

        answers.append(answer_name[prediction])
        print(f"{image_path} -> Prediction: {answer_name[prediction]}")  # 打印预测结果
    return answers





def main():
    model_path = 'python/models/cnn.pt' 
    inference_folder = 'images/cropped_answers/page_2_cropped'
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # 加载模型
    validate(model_path,device,inference_folder) # 模型文件路径





if __name__ == "__main__":
    main()
