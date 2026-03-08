# RAYZO — AI Powered Lung X-Ray Analysis with Blockchain Audit Layer

## Overview

RAYZO is an AI-powered medical imaging platform that analyzes lung X-ray images to detect potential diseases and generates automated clinical reports.
To ensure **data integrity and transparency**, every generated report is cryptographically hashed and recorded on the **Solana blockchain**, creating a **tamper-proof medical audit trail**.

This system helps hospitals and clinicians verify the authenticity of medical reports and maintain an immutable history of patient diagnostics.

---

## Problem

Many hospitals and diagnostic centers still rely on manual report verification and centralized storage. This creates several risks:

* Medical reports can be **tampered with or altered**
* Lack of **transparent medical audit trails**
* Difficulty verifying **authenticity of diagnostic results**
* Limited access to **AI-assisted early detection tools**

---

## Solution

RAYZO combines **Artificial Intelligence + Blockchain** to build a secure diagnostic pipeline.

1. AI analyzes chest X-ray images.
2. The system generates a diagnostic report.
3. A cryptographic **hash of the report** is created.
4. The hash is stored on the **Solana blockchain** via a smart contract.
5. Doctors and hospitals can verify the report integrity anytime.

---

## System Architecture

X-Ray Image
↓
AI Detection Model
↓
Report Generation
↓
Report Hash (SHA-256)
↓
Solana Smart Contract
↓
Immutable Medical Audit Trail

---

## Key Features

### AI-Powered X-Ray Analysis

* Automated lung disease detection
* Confidence scoring for predictions
* Explainable AI using **Grad-CAM heatmaps**

### Secure Blockchain Audit Layer

* Smart contract built using **Solana + Anchor**
* Stores report hashes for verification
* Prevents tampering of diagnostic results

### Medical Report Integrity

* Each report has a unique hash
* Doctors can verify reports against blockchain records
* Ensures long-term auditability

### Scalable Architecture

* AI microservice for model inference
* Blockchain layer for trust and verification
* Modular design for integration with hospital systems

---

## Tech Stack

### Artificial Intelligence

* Python
* PyTorch
* OpenCV
* Grad-CAM (Explainability)
* NUMPY
* SKLEARN
* PANDAS

### Backend / API

* FastAPI
* Python
* SPRING BOOT
* JAVA

### Blockchain

* Solana
* Anchor Framework
* Rust Smart Contracts

### Development Tools

* Git & GitHub
* Docker (optional)
* VS Code



## Repository Structure

```
RAYZO
├── ai-service
│   ├── app.py
│   ├── model.py
│   ├── gradcam.py
│   ├── segmentation.py
│   └── requirements.txt
│
├── solana-audit-layer
│   ├── programs
│   │   └── rayzo_auditlayer
│   ├── tests
│   └── Anchor.toml
│
│
└── README.md
```

---

## How It Works

1. Upload a lung X-ray image.
2. The AI model analyzes the image and predicts abnormalities.
3. The system generates a structured diagnostic report.
4. A SHA-256 hash of the report is computed.
5. The hash is stored on the Solana blockchain.
6. Anyone can verify report authenticity using the stored hash.

---

## Future Improvements

* Multi-disease lung detection models
* Integration with hospital EHR systems
* Real-time blockchain verification dashboard
* Patient medical history tracking
* Decentralized medical data registry

---

## Impact

RAYZO improves healthcare systems by:

* Enhancing **trust in medical diagnostics**
* Preventing **report tampering**
* Providing **AI-assisted disease detection**
* Creating **transparent medical audit trails**

---

## License

This project is released under the MIT License.

