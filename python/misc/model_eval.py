import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns
from models import CNN
from train import load_data

def plot_confusion_matrix(cm, class_names):
    """
    绘制混淆矩阵
    :param cm: 混淆矩阵
    :param class_names: 类别名称列表
    """
    fig, ax = plt.subplots(figsize=(5, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    # plt.show()
    plt.savefig('images/confusion_matrix.png')

def test_model_and_plot_cm(model, device, test_loader, class_names):
    """
    测试模型并绘制混淆矩阵
    :param model: 训练好的模型
    :param device: 设备，'cuda' 或 'cpu'
    :param test_loader: 测试数据加载器
    :param class_names: 类别名称列表
    """
    all_preds = []
    all_targets = []
    model.eval()
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            outputs = model(data)
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.view(-1).cpu().numpy())
            all_targets.extend(target.view(-1).cpu().numpy())

    cm = confusion_matrix(all_targets, all_preds)
    plot_confusion_matrix(cm, class_names)


def main():
    # 假设你的类别名称如下
    class_names = ['A', 'B', 'C', 'D', 'E', 'Blank']

    # 假设test_loader是你的测试数据加载器，model是你的模型
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = CNN()

    test_loader = load_data()[1]

    # 调用函数
    test_model_and_plot_cm(model, device, test_loader, class_names)

