import cv2
import numpy as np

def lung_segmentation(image_path):

    # 1. Read image
    image = cv2.imread(image_path)
    original = image.copy()

    # 2. Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 3. Improve contrast using CLAHE (better than equalizeHist)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)

    # 4. Reduce noise while preserving edges
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    # 5. Adaptive threshold (better than fixed threshold)
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )

    # 6. Morphological cleaning
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)

    # 7. Find contours (possible lung regions)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    lung_mask = np.zeros_like(mask)

    # 8. Keep only large contours (lungs)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:  # remove small regions
            cv2.drawContours(lung_mask, [cnt], -1, 255, -1)

    # 9. Smooth mask
    lung_mask = cv2.GaussianBlur(lung_mask, (11,11), 0)

    # 10. Create colored heatmap
    colored_mask = cv2.applyColorMap(lung_mask, cv2.COLORMAP_JET)

    # 11. Overlay with original image
    overlay = cv2.addWeighted(original, 0.75, colored_mask, 0.25, 0)

    # 12. Add label
    cv2.putText(
        overlay,
        "Enhanced Lung Segmentation",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255,255,255),
        2
    )

    return overlay
