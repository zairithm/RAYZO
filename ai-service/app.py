from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from torchvision import transforms
from PIL import Image
from segmentation import lung_segmentation
from edges import rib_edge_detection
import torch
import numpy as np
import io
import cv2
import base64

from model import load_model, LABELS, DEVICE
from triage import compute_triage
from confidence import compute_confidence
from gradcam import GradCAM
from clinician_llm import generate_clinician_note, answer_medical_question

app = FastAPI(title="Complete Clinician AI Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_model()
gradcam = GradCAM(model)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485], [0.229])
])

def predict_image(image_bytes):

    # Convert image
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Save temp image for anatomical analysis
    import uuid

    temp_path = f"temp_{uuid.uuid4()}.jpg"
    image.save(temp_path)


    input_tensor = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(input_tensor)
        probs = torch.sigmoid(outputs).cpu().numpy()[0]

    probabilities = {
        LABELS[i]: float(round(probs[i], 4))
        for i in range(len(LABELS))
    }

    # ----------------------------
    # Confidence
    # ----------------------------

    certainty_score, certainty_level, max_prob = compute_confidence(probabilities)

    # ----------------------------
    # Triage
    # ----------------------------

    triage_score, priority = compute_triage(probabilities)

    # ----------------------------
    # Anatomical Analysis
    # ----------------------------

    lung_mask = lung_segmentation(temp_path)
    rib_edges = rib_edge_detection(temp_path)

    # Convert lung mask to base64
    _, lung_buffer = cv2.imencode(".jpg", lung_mask)
    lung_base64 = base64.b64encode(lung_buffer).decode()

    # Convert rib edges to base64
    _, rib_buffer = cv2.imencode(".jpg", rib_edges)
    rib_base64 = base64.b64encode(rib_buffer).decode()

    # ----------------------------
    # LLM Note
    # ----------------------------

    clinician_note = generate_clinician_note(
        probabilities,
        priority,
        certainty_level
    )


    # ----------------------------
    # GradCAM
    # ----------------------------

    top_class = np.argmax(probs)

    cam = gradcam.generate(input_tensor, top_class)

    heatmap = cv2.applyColorMap(
        np.uint8(255 * cam),
        cv2.COLORMAP_JET
    )

    _, buffer = cv2.imencode(".jpg", heatmap)
    heatmap_base64 = base64.b64encode(buffer).decode()

    # ----------------------------
    # Final Response
    # ----------------------------

    return {

        "probabilities": probabilities,

        "max_probability": max_prob,

        "confidence_score": certainty_score,
        "confidence_level": certainty_level,

        "triage_score": triage_score,
        "priority": priority,

        "clinician_note": clinician_note,

        "visual_analysis": {
            "gradcam": heatmap_base64,
            "lung_segmentation": lung_base64,
            "rib_edges": rib_base64
        }
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    result = predict_image(contents)
    return JSONResponse(content=result)

@app.post("/bulk_predict")
async def bulk_predict(files: list[UploadFile] = File(...)):
    results = []

    for file in files:
        contents = await file.read()
        prediction = predict_image(contents)
        prediction["filename"] = file.filename
        results.append(prediction)

    results = sorted(results, key=lambda x: x["triage_score"], reverse=True)

    return JSONResponse(content={"results": results})

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask_medical_question(q: Question):
    answer = answer_medical_question(q.question)
    speak(answer)
    return {"answer": answer}