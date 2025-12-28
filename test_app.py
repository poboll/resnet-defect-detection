"""
测试 Streamlit 应用的核心功能
"""

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import os

# 定义类别名称
class_names = ['crazing', 'inclusion', 'patches', 'pitted_surface', 'rolled-in_scale', 'scratches']
class_names_cn = {
    'crazing': '裂纹',
    'inclusion': '夹杂',
    'patches': '斑块',
    'pitted_surface': '麻点',
    'rolled-in_scale': '氧化皮',
    'scratches': '划痕'
}

print("="*50)
print("测试 ResNet 缺陷检测系统")
print("="*50)

# 1. 测试模型加载
print("\n[1/3] 加载模型...")
model = models.resnet18(pretrained=False)
num_ftrs = model.fc.in_features
model.fc = nn.Sequential(
    nn.Linear(num_ftrs, 256),
    nn.ReLU(),
    nn.Linear(256, 6)
)

if os.path.exists('best_model.pth'):
    model.load_state_dict(torch.load('best_model.pth', map_location='cpu'))
    print("✅ 模型加载成功！")
else:
    print("❌ 未找到模型文件 'best_model.pth'")
    exit(1)

model.eval()

# 2. 测试图像预处理
print("\n[2/3] 测试图像预处理...")
test_image_path = 'data/train/images/crazing/crazing_1.jpg'

if os.path.exists(test_image_path):
    image = Image.open(test_image_path).convert('RGB')
    print(f"✅ 测试图片加载成功: {test_image_path}")
    
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    image_tensor = preprocess(image)
    image_tensor = image_tensor.unsqueeze(0)
    print(f"✅ 图像预处理完成，张量形状: {image_tensor.shape}")
else:
    print(f"❌ 测试图片不存在: {test_image_path}")
    exit(1)

# 3. 测试模型推理
print("\n[3/3] 测试模型推理...")
with torch.no_grad():
    outputs = model(image_tensor)
    probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
    confidence, predicted_idx = torch.max(probabilities, 0)

predicted_class = class_names[predicted_idx.item()]
confidence_percent = confidence.item() * 100

print(f"\n{'='*50}")
print(f"检测结果:")
print(f"{'='*50}")
print(f"预测类别: {class_names_cn[predicted_class]} ({predicted_class})")
print(f"置信度: {confidence_percent:.2f}%")
print(f"\n各类别概率分布:")
print(f"{'='*50}")

for i, class_name in enumerate(class_names):
    prob = probabilities[i].item() * 100
    bar = '█' * int(prob / 5)
    print(f"{class_names_cn[class_name]:8s} ({class_name:15s}): {prob:6.2f}% {bar}")

print(f"\n{'='*50}")
print("✅ 所有测试通过！系统运行正常。")
print(f"{'='*50}")
