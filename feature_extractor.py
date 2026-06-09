import torch
import numpy as np

from PIL import Image
from torchvision.models import resnet50
from torchvision import transforms

model = resnet50(weights="DEFAULT")
model = torch.nn.Sequential(*list(model.children())[:-1])
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def extract_feature(path):

    img = Image.open(path).convert("RGB")
    img = transform(img).unsqueeze(0)

    with torch.no_grad():
        feature = model(img)

    feature = feature.squeeze().numpy()

    feature /= np.linalg.norm(feature)

    return feature