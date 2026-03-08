import torch
import cv2
import numpy as np

class GradCAM:

    def __init__(self, model):

        self.model = model
        self.model.eval()

        self.gradients = None
        self.activations = None

        # Automatically hook the LAST convolution layer
        for module in reversed(list(self.model.modules())):
            if isinstance(module, torch.nn.Conv2d):
                module.register_forward_hook(self.forward_hook)
                module.register_backward_hook(self.backward_hook)
                break

    def forward_hook(self, module, input, output):
        self.activations = output

    def backward_hook(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]

    def generate(self, input_tensor, class_idx):

        output = self.model(input_tensor)

        self.model.zero_grad()

        score = output[:, class_idx]

        score.backward()

        gradients = self.gradients[0].cpu().detach().numpy()
        activations = self.activations[0].cpu().detach().numpy()

        # Global average pooling
        weights = np.mean(gradients, axis=(1, 2))

        cam = np.zeros(activations.shape[1:], dtype=np.float32)

        for i in range(len(weights)):
            cam += weights[i] * activations[i]

        cam = np.maximum(cam, 0)

        cam = cv2.resize(cam, (224, 224))

        cam = cam - cam.min()

        if cam.max() != 0:
            cam = cam / cam.max()

        return cam