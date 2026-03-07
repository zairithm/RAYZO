import cv2
import numpy as np

def rib_edge_detection(image_path):

    image = cv2.imread(image_path)
    original = image.copy()

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Better contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)

    # Remove noise but keep edges
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    # Detect edges
    edges = cv2.Canny(gray, 30, 100)

    # Morphological dilation for thicker ribs
    kernel = np.ones((3,3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)

    # Remove small noise edges
    edges = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel)

    # Create colored overlay
    edge_overlay = np.zeros_like(original)
    edge_overlay[:,:,2] = edges

    # Blend edges with original image
    overlay = cv2.addWeighted(original, 0.85, edge_overlay, 0.7, 0)

    # Label
    cv2.putText(
        overlay,
        "Enhanced Rib Edge Detection",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255,255,255),
        2
    )

    return overlay