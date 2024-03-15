import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import models


def load_data():
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        # transforms.Resize((130, 24)),# modify here to train id model
        transforms.Resize((24, 186)),
        transforms.ToTensor(),
    ])

    train_data = datasets.ImageFolder(root='data/id_data/train', transform=transform)
    test_data = datasets.ImageFolder(root='data/id_data/test', transform=transform)# modify here to train id model

    train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
    test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

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
def test(model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += criterion(output, target).item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))
    

# 5. 主函数
def main():
    num_epochs = 50
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)
    train_loader, test_loader = load_data()
    
    # model = models.get_CNN().to(device)
    model = models.get_CNN_id().to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.0005)
    
    global criterion
    criterion = nn.CrossEntropyLoss()


    for epoch in range(num_epochs):
        train(model, device, train_loader, optimizer, epoch)
        test(model, device, test_loader)

    torch.save(model.state_dict(), "python/models/cnn_id.pt")


        
if __name__ == '__main__':
    main()