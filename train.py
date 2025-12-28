"""
基于 ResNet18 的工业零件表面缺陷分类训练脚本
课程作业：《人工智能应用技术》期末作业
选题：基于 ResNet 的工业零件表面缺陷分类
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import numpy as np
import os
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

# 设置随机种子以保证结果可复现
torch.manual_seed(42)
np.random.seed(42)

# ============================================
# 1. 数据预处理（考核要求：数据预处理）
# ============================================
data_transforms = {
    'train': transforms.Compose([
        transforms.RandomResizedCrop(224),      # 随机裁剪并调整为224x224（数据增强）
        transforms.RandomHorizontalFlip(),      # 随机水平翻转（数据增强）
        transforms.ToTensor(),                  # 转换为Tensor
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # ImageNet标准化
    ]),
    'validation': transforms.Compose([
        transforms.Resize(256),                 # 调整大小为256
        transforms.CenterCrop(224),             # 中心裁剪为224x224
        transforms.ToTensor(),                  # 转换为Tensor
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # ImageNet标准化
    ]),
}

# 数据集路径（根据实际数据结构调整）
data_dir = './data'
image_datasets = {
    'train': datasets.ImageFolder(os.path.join(data_dir, 'train/images'), data_transforms['train']),
    'validation': datasets.ImageFolder(os.path.join(data_dir, 'validation/images'), data_transforms['validation'])
}

# 数据加载器（考核要求：Batch Size = 16）
batch_size = 16
dataloaders = {
    'train': DataLoader(image_datasets['train'], batch_size=batch_size, shuffle=True, num_workers=0),
    'validation': DataLoader(image_datasets['validation'], batch_size=batch_size, shuffle=False, num_workers=0)
}

# 获取数据集大小和类别名称
dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'validation']}
class_names = image_datasets['train'].classes

print(f"数据集加载完成！")
print(f"训练集样本数: {dataset_sizes['train']}")
print(f"验证集样本数: {dataset_sizes['validation']}")
print(f"类别数量: {len(class_names)}")
print(f"类别名称: {class_names}")

# ============================================
# 2. 模型构建（考核要求：ResNet18 + 参数冻结 + 自定义FC层）
# ============================================
# 加载预训练的 ResNet18 模型
model = models.resnet18(pretrained=True)

# 冻结 ResNet18 的前8层参数（考核要求：冻结参数）
# ResNet18 的结构：conv1 -> bn1 -> relu -> maxpool -> layer1 -> layer2 -> layer3 -> layer4 -> avgpool -> fc
# 我们冻结除全连接层以外的所有层
for name, param in model.named_parameters():
    if 'fc' not in name:  # 冻结所有非fc层的参数
        param.requires_grad = False

# 获取原始全连接层的输入特征数
num_ftrs = model.fc.in_features

# 修改全连接层（考核要求：Linear(输入,256) -> ReLU -> Linear(256,6)）
model.fc = nn.Sequential(
    nn.Linear(num_ftrs, 256),   # 第一层全连接：输入特征 -> 256维
    nn.ReLU(),                   # ReLU激活函数
    nn.Linear(256, 6)           # 第二层全连接：256维 -> 6类缺陷
)

# 将模型移动到GPU（如果可用）
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

print(f"\n模型构建完成！")
print(f"模型设备: {device}")
print(f"全连接层结构: Linear({num_ftrs}, 256) -> ReLU -> Linear(256, 6)")

# ============================================
# 3. 训练配置（考核要求：损失函数、优化器、Epochs）
# ============================================
criterion = nn.CrossEntropyLoss()  # 交叉熵损失函数

# 仅训练全连接层的参数（冻结的层不需要梯度）
optimizer = optim.SGD(filter(lambda p: p.requires_grad, model.parameters()),
                      lr=0.001,
                      momentum=0.9)  # SGD优化器

# 训练轮数
num_epochs = 15

# 用于记录训练过程
train_loss_history = []
train_acc_history = []
val_loss_history = []
val_acc_history = []
best_acc = 0.0

# ============================================
# 4. 训练循环
# ============================================
print("\n" + "="*50)
print("开始训练...")
print("="*50)

for epoch in range(num_epochs):
    print(f'\nEpoch {epoch+1}/{num_epochs}')
    print('-' * 30)
    
    # 每个epoch包含训练和验证两个阶段
    for phase in ['train', 'validation']:
        if phase == 'train':
            model.train()  # 训练模式
        else:
            model.eval()   # 评估模式
        
        running_loss = 0.0
        running_corrects = 0
        
        # 遍历数据
        for inputs, labels in tqdm(dataloaders[phase], desc=f'{phase.capitalize()}'):
            inputs = inputs.to(device)
            labels = labels.to(device)
            
            # 清零梯度
            optimizer.zero_grad()
            
            # 前向传播
            with torch.set_grad_enabled(phase == 'train'):
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)
                
                # 反向传播和优化（仅在训练阶段）
                if phase == 'train':
                    loss.backward()
                    optimizer.step()
            
            # 统计
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
        
        # 计算epoch的平均loss和准确率
        epoch_loss = running_loss / dataset_sizes[phase]
        epoch_acc = running_corrects.double() / dataset_sizes[phase]
        
        print(f'{phase.capitalize()} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')
        
        # 记录历史数据
        if phase == 'train':
            train_loss_history.append(epoch_loss)
            train_acc_history.append(epoch_acc.item())
        else:
            val_loss_history.append(epoch_loss)
            val_acc_history.append(epoch_acc.item())
            
            # 保存最佳模型（考核要求：保存准确率最高的模型）
            if epoch_acc > best_acc:
                best_acc = epoch_acc
                torch.save(model.state_dict(), 'best_model.pth')
                print(f'>>> 保存最佳模型，验证集准确率: {best_acc:.4f}')

print("\n" + "="*50)
print(f"训练完成！最佳验证集准确率: {best_acc:.4f}")
print("="*50)

# ============================================
# 5. 绘制训练曲线（考核要求：绘制 Loss 和 Accuracy 曲线）
# ============================================
plt.figure(figsize=(12, 5))

# Loss 曲线
plt.subplot(1, 2, 1)
plt.plot(range(1, num_epochs+1), train_loss_history, 'b-', label='Training Loss')
plt.plot(range(1, num_epochs+1), val_loss_history, 'r-', label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)

# Accuracy 曲线
plt.subplot(1, 2, 2)
plt.plot(range(1, num_epochs+1), train_acc_history, 'b-', label='Training Accuracy')
plt.plot(range(1, num_epochs+1), val_acc_history, 'r-', label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('training_curve.png', dpi=300, bbox_inches='tight')
print("\n训练曲线已保存为 'training_curve.png'")

# ============================================
# 6. 模型测试（在验证集上评估最佳模型）
# ============================================
print("\n" + "="*50)
print("加载最佳模型进行测试...")
print("="*50)

# 加载最佳模型
model.load_state_dict(torch.load('best_model.pth'))
model.eval()

# 在验证集上进行最终测试
test_corrects = 0
all_preds = []
all_labels = []

with torch.no_grad():
    for inputs, labels in dataloaders['validation']:
        inputs = inputs.to(device)
        labels = labels.to(device)
        
        outputs = model(inputs)
        _, preds = torch.max(outputs, 1)
        
        test_corrects += torch.sum(preds == labels.data)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

test_acc = test_corrects.double() / dataset_sizes['validation']
print(f"验证集最终准确率: {test_acc:.4f}")

# 打印各类别的准确率
from sklearn.metrics import classification_report
print("\n各类别分类报告:")
print(classification_report(all_labels, all_preds, target_names=class_names))

print("\n所有任务完成！")

if __name__ == '__main__':
    pass
