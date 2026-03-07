import os
import torch
import torch.nn as nn
from torchvision import models
import gdown

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

MODEL_PATH = "models/best_model.pth"
MODEL_URL = "https://drive.google.com/file/d/16hGq39rB4VDZ-ivWRh3EKmVP8Mm14A4e/view?usp=sharing"

LABELS = ["Atelectasis", "Effusion", "Pneumonia", "No Finding"]

def download_model():
    os.makedirs("models", exist_ok=True)
    if not os.path.exists(MODEL_PATH):
        gdown.download(MODEL_URL, MODEL_PATH, quiet=False, fuzzy=True)

def load_model():
    download_model()
    model = models.densenet121(weights=None)
    model.classifier = nn.Linear(1024, 4)
    model.load_state_dict(
    torch.load(MODEL_PATH, map_location=DEVICE, weights_only=False)
)
    model.to(DEVICE)
    model.eval()
    return model