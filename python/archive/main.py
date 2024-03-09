import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
from collections import OrderedDict
from torch.utils.data import DataLoader
from torchvision import transforms
from PIL import Image
import time

if torch.cuda.is_available():
    print("CUDA is ready and set, GPU acceleration is initiated .")
else:
    print("CUDA is not available. CPU initiated.")

# Download training and testing data
# transform = transforms.Compose([transforms.ToTensor(),
#                                 transforms.Normalize((0.5,), (0.5,))])
# train_ds = datasets.FashionMNIST('F_MNIST_data', download=True, train=True, transform=transform)
# test_ds = datasets.FashionMNIST('F_MNIST_data', download=True, train=False, transform=transform)

transform = transforms.Compose([
    transforms.Resize((52, 300)),
    transforms.Grayscale(num_output_channels=1),
    transforms.ToTensor(),
    # Add more transformations as needed
])
train_dataset = datasets.ImageFolder(root='dataset/train_ds', transform=transform)
test_dataset = datasets.ImageFolder(root='dataset/test_ds', transform=transform)

sample, label = train_dataset[0]
print(f'{sample.size()} is the size, {label} is the label')
# if sample.dim() == 3 and sample.shape[0] == 1:  # Grayscale image of shape (1, H, W)
#     image_np = sample.squeeze().numpy()
# elif sample.dim() == 3:  # RGB image of shape (C, H, W)
#     image_np = sample.permute(1, 2, 0).numpy()
#
# # Plot the image
# plt.imshow(image_np, cmap='gray' if sample.shape[0] == 1 else None)
# plt.title(f'Label: {label}')
# plt.axis('off')  # Hide the axis
# plt.show()

# split train set into training (80%) and validation set (20%)
train_num = len(train_dataset)
print("number of training data: ", train_num)
indices = list(range(train_num))
np.random.shuffle(indices)
split = int(np.floor(0.2 * train_num))
val_idx, train_idx = indices[:split], indices[split:]
print(len(val_idx), len(train_idx))

epochs = 100
batch_siz = 8
learning_rate = 0.001

cnn_kernel_size = 3
padding_size = cnn_kernel_size // 2
dropout_rate = 0.3
dropout_rate2 = 0.4

# prepare dataloaders
# train_sampler = torch.utils.data.sampler.SubsetRandomSampler(train_idx)
# train_dl = torch.utils.data.DataLoader(train_ds, batch_size=batch_siz, sampler=train_sampler)

train_loader = DataLoader(dataset=train_dataset, batch_size=batch_siz, shuffle=True)
test_loader = DataLoader(dataset=test_dataset, batch_size=batch_siz, shuffle=False)


val_sampler = torch.utils.data.sampler.SubsetRandomSampler(val_idx)
val_dl = torch.utils.data.DataLoader(train_dataset, batch_size=batch_siz, sampler=val_sampler)
# test_dl = torch.utils.data.DataLoader(test_ds, batch_size=batch_siz, shuffle=True)


def network():
    model = nn.Sequential(OrderedDict([
        # # Convolutional layers
        # ('conv1', nn.Conv2d(1, 16, cnn_kernel_size, padding=padding_size)),
        # # 1 input channel (grayscale), 32 output channels, kernel size 3
        # ('bn1', nn.BatchNorm2d(16)),  # Batch Normalization
        # ('relu1', nn.ReLU()),
        # # ('bn1', nn.BatchNorm2d(16)),  # Batch Normalization
        # ('pool1', nn.MaxPool2d(2, 2)),  # Pooling layer
        #
        # ('conv2', nn.Conv2d(16, 32, cnn_kernel_size, padding=padding_size)),
        # ('bn2', nn.BatchNorm2d(32)),  # Batch Normalization
        # ('relu2', nn.ReLU()),
        # # ('bn2', nn.BatchNorm2d(32)),  # Batch Normalization
        # ('pool2', nn.MaxPool2d(2, 2)),  # Pooling layer

        # Flattening the output for the fully connected layers
        ('flatten', nn.Flatten()),

        # Fully connected layers
        # ('fc1', nn.Linear(32 * 13 * 75, 128)),
        ('fc1', nn.Linear(52 * 300, 128)),
        ('relu3', nn.ReLU()),
        ('drop1', nn.Dropout(dropout_rate)),

        ('fc2', nn.Linear(128, 64)),
        ('relu4', nn.ReLU()),
        ('drop2', nn.Dropout(dropout_rate2)),

        ('output', nn.Linear(64, 5)),
        ('logsoftmax', nn.LogSoftmax(dim=1))
    ]))

    # # Use GPU if available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = model.to(device)

    # define the criterion and optimizer
    # loss_fn = nn.CrossEntropyLoss()
    loss_fn = nn.NLLLoss()
    # optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    optimizer = optim.SGD(model.parameters(), lr=learning_rate)
    return model, loss_fn, optimizer, device


model, loss_fn, optimizer, device = network()
print(model)


def train_model(model, loss_fn, optimizer, trainloader, valloader, device, n_epochs=epochs):
    train_losses = []
    val_losses = []
    val_accuracies = []

    for epoch in range(n_epochs):
        model.train()  # Set the model to training mode
        train_epoch_loss = 0

        for images, labels in trainloader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            train_batch_loss = loss_fn(outputs, labels)
            train_batch_loss.backward()
            optimizer.step()

            train_epoch_loss += train_batch_loss.item()

        train_epoch_loss = train_epoch_loss / len(trainloader)
        train_losses.append(train_epoch_loss)

        # Validation phase
        model.eval()  # Set the model to evaluation mode
        val_epoch_loss = 0
        val_epoch_acc = 0

        with torch.no_grad():
            for images, labels in valloader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                val_batch_loss = loss_fn(outputs, labels)
                val_epoch_loss += val_batch_loss.item()

                proba = torch.exp(outputs)
                top_p, top_class = proba.topk(1, dim=1)
                equals = top_class == labels.view(*top_class.shape)
                val_epoch_acc += torch.mean(equals.type(torch.FloatTensor)).item()

        val_epoch_loss = val_epoch_loss / len(valloader)
        val_epoch_acc = val_epoch_acc / len(valloader)
        val_losses.append(val_epoch_loss)
        val_accuracies.append(val_epoch_acc)

        print(
            f'Epoch {epoch + 1}: Train Loss: {train_epoch_loss:.19f}, Validation Loss: {val_epoch_loss:.19f}, Validation Accuracy: {val_epoch_acc * 100:.2f}%')

    # Plotting
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(train_losses, label='Train Loss')
    plt.plot(val_losses, label='Validation Loss')
    plt.title("Training and Validation Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(val_accuracies, label='Validation Accuracy')
    plt.title("Validation Accuracy")
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend()

    plt.show()

    return model


def test_model(model, loss_fn, testloader, device):
    test_losses = []
    test_acc = 0

    model.eval()  # Set the model to evaluation mode
    with torch.no_grad():
        for images, labels in testloader:
            images, labels = images.to(device), labels.to(device)
            # images = images.view(images.shape[0], -1)  # Flatten the images

            outputs = model(images)
            test_batch_loss = loss_fn(outputs, labels)
            test_losses.append(test_batch_loss.item())

            proba = torch.exp(outputs)
            top_p, top_class = proba.topk(1, dim=1)
            equals = top_class == labels.view(*top_class.shape)
            test_acc += torch.mean(equals.type(torch.FloatTensor)).item()

    test_loss = sum(test_losses) / len(test_losses)  # average testing loss
    test_acc = test_acc / len(testloader)
    print(f'Testing Loss: {test_loss:.19f}, Testing Accuracy: {test_acc * 100:.2f}%')


# # # To train the model
# model = train_model(model, loss_fn, optimizer, train_loader, val_dl, device)
# #
# # # To test the model
# test_model(model, loss_fn, test_loader, device)
# torch.save(model.state_dict(), 'model.pth')


def Test_model():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.load_state_dict(torch.load('model.pth'))
    model.eval()

    # Load your image in grayscale
    image_path = 'dataset/model_testing/B1.png'
    image = Image.open(image_path).convert('L')
    # Define the transformations
    transform = transforms.Compose([
        transforms.Resize((52, 300)),  # Resize the image to the expected size
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5]),  # Adjust normalization parameters if necessary
    ])
    # Apply transformations
    image = transform(image)

    # Add a batch dimension
    image = image.unsqueeze(0).to(device)
    with torch.no_grad():  # No need to track gradients for inference
        output = model(image)
        # Assuming your model outputs raw scores (logits)
        probabilities = torch.softmax(output, dim=1)
        predicted_class = probabilities.argmax(dim=1)

    print(f'Predicted class index: {predicted_class.item()}')
    # If you have a class index to name mapping
    class_names = ['A', 'B', 'C', 'D', 'E']
    print(f'Predicted class name: {class_names[predicted_class.item()]}')


import os
import torch
from torchvision import transforms
from PIL import Image


def test_model_on_folder(folder_path):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Load the model onto the correct device
    model.load_state_dict(torch.load('model.pth', map_location=device))
    model.to(device)
    model.eval()

    # Define the transformations
    transform = transforms.Compose([
        transforms.Resize((52, 300)),  # Resize the image to the expected size
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5]),  # Adjust normalization parameters if necessary
    ])

    # Sort the list of filenames to ensure the processing order is consistent
    filenames = sorted(os.listdir(folder_path))
    filenames = sorted(filenames, key=lambda x: int(os.path.splitext(x)[0]))
    answers = []

    # Iterate through all images in the folder
    for filename in filenames:
        if filename.endswith('.jpg'):  # Check if the file is an image
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path).convert('L')
            image = transform(image)
            image = image.unsqueeze(0).to(device)

            with torch.no_grad():  # No need to track gradients for inference
                output = model(image)
                probabilities = torch.softmax(output, dim=1)
                predicted_class = probabilities.argmax(dim=1)

            # Assuming you have a list of class names
            class_names = ['A', 'B', 'C', 'D', 'E']
            print(f'Image: {filename}, Predicted class name: {class_names[predicted_class.cpu().item()]}')
            answers.append(class_names[predicted_class])
    print(answers)



# Example usage
folder_path = 'dataset/model_testing/'


start_time = time.perf_counter()

# The operation you want to measure
test_model_on_folder(folder_path)

end_time = time.perf_counter()
duration = end_time - start_time

print(f"The operation took {duration} seconds.")
# Test_model()