import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import models


def load_data():
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((125, 24)),# modify here to train id model
        # transforms.Resize((24, 186)),
        transforms.ToTensor(),
    ])

    train_data = datasets.ImageFolder(root='data/answer_data/train', transform=transform)
    test_data = datasets.ImageFolder(root='data/answer_data/test', transform=transform)# modify here to train id model

    train_loader = DataLoader(train_data, batch_size=16, shuffle=True)
    test_loader = DataLoader(test_data, batch_size=16, shuffle=False)

    return train_loader, test_loader


# 3. 训练模型
def train(model, device, train_loader, optimizer, epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data) 
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % 10 == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))
        

# 4. 测试模型
# def test(model, device, test_loader):
#     model.eval()
#     test_loss = 0
#     correct = 0
#     with torch.no_grad():
#         for data, target in test_loader:
#             data, target = data.to(device), target.to(device)
#             output = model(data)
#             test_loss += criterion(output, target).item()
#             pred = output.argmax(dim=1, keepdim=True)
#             correct += pred.eq(target.view_as(pred)).sum().item()

#     test_loss /= len(test_loader.dataset)
#     print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
#         test_loss, correct, len(test_loader.dataset),
#         100. * correct / len(test_loader.dataset)))
    

# 修改后的测试函数，用于收集预测结果和真实标签
def test(model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    all_preds = []
    all_targets = []
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += criterion(output, target).item()
            pred = output.argmax(dim=1, keepdim=True).squeeze()
            correct += pred.eq(target.view_as(pred)).sum().item()
            all_preds.extend(pred.tolist())
            all_targets.extend(target.tolist())

    test_loss /= len(test_loader.dataset)
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))
    
    return all_targets, all_preds



# 绘制混淆矩阵的函数
def plot_confusion_matrix(targets, preds, classes):
    cm = confusion_matrix(targets, preds)
    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=classes, yticklabels=classes,
           title='Confusion Matrix',
           ylabel='True label',
           xlabel='Predicted label')

    plt.xticks(rotation=45)
    plt.yticks(rotation=45)

    fmt = 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    plt.show()
    plt.savefig('images/confusion_matrix.png')



# 5. 主函数
def main():
    num_epochs = 50
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)
    train_loader, test_loader = load_data()
    
    model = models.get_EnhancedCNN().to(device)
    # model = models.get_CNN_id().to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.0001)
    
    global criterion
    weights = torch.tensor([1.0, 1.0, 1.0, 1.0, 1.0, 10.0]).to(device)
    criterion = nn.CrossEntropyLoss(weight=weights)


    # for epoch in range(num_epochs):
    #     train(model, device, train_loader, optimizer, epoch)
    #     test(model, device, test_loader)

    # torch.save(model.state_dict(), "python/models/cnn1.pt")

    for epoch in range(num_epochs):
        train(model, device, train_loader, optimizer, epoch)
        targets, preds = test(model, device, test_loader)
        
    # 假设你有一个类名的列表
    class_names = ['A', 'B', 'C', 'D', 'E', 'Blank']
    plot_confusion_matrix(targets, preds, classes=class_names)

    torch.save(model.state_dict(), "python/models/cnn2.pt")


        
if __name__ == '__main__':
    main()