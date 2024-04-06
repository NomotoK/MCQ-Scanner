import os
import torch
from torchvision import transforms
from PIL import Image
import models


def load_model(model_path, model):
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



def get_answers(model_path,device, inference_folder, model=models.get_EnhancedCNN()):  
    model = load_model(model_path,model)
    model.to(device)
    
    # 设置数据加载器
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((125, 24)),
        transforms.ToTensor(),
    ])

    filenames = sorted(os.listdir(inference_folder))
    filenames = sorted(filenames, key=lambda x: int(os.path.splitext(x)[0]))
    answers = []    

    for filename in filenames:
        image_path = os.path.join(inference_folder, filename)
        prediction = predict_image(model, device, image_path, transform)
        answer_name = ['A', 'B', 'C', 'D', 'E','-']

        answers.append(answer_name[prediction])
        # print(f"{image_path} -> Prediction: {answer_name[prediction]}")  # 打印预测结果
    return answers


def get_id(model_path,device, inference_folder, model= models.get_CNN_id()):
    model = load_model(model_path, model)
    model.to(device)
    
    # 设置数据加载器
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((24, 186)),
        transforms.ToTensor(),
    ])

    filenames = sorted(os.listdir(inference_folder))
    filenames = sorted(filenames, key=lambda x: int(os.path.splitext(x)[0]))
    id = []    

    for filename in filenames:
        image_path = os.path.join(inference_folder, filename)
        prediction = predict_image(model, device, image_path, transform)
        id_name = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        id.append(id_name[prediction])
        # print(f"{image_path} -> Prediction: {id_name[prediction]}")  # 打印预测结果
    # print (id)
    return id





# def main():
#     ans_model_path = 'python/models/cnn.pt' 
#     id_model_path = 'python/models/cnn_id.pt'
#     ans_inference_folder = 'images/cropped_answers/page_2_cropped'
#     id_inference_folder = 'images/cropped_id/page_10_id'
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
#     # 加载模型
#     get_answers(ans_model_path,device,ans_inference_folder) # 模型文件路径
#     get_id(id_model_path,device,id_inference_folder) # 模型文件路径





# if __name__ == "__main__":
#     main()
