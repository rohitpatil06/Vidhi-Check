# VidhiCheck — AI-Based Packaged Commodity Compliance Checker

> **“Scan. Verify. Comply.”**  
> *A presentation-ready prototype designed for Legal Metrology officers for Smart India Hackathon (SIH 2026).*

---

## 🏛️ Project Overview

**VidhiCheck** is an AI-assisted web application built to empower **Legal Metrology officers** to inspect packaged commodities quickly and accurately. Officers can upload a product label image, automatically extract mandatory declarations, check them against statutory rules, flag infractions, record human verification remarks, and generate official compliance inspection reports in PDF format.

### Key Highlights
- **Human-in-the-Loop Architecture**: Strictly adheres to the statutory workflow:  
  $$\text{AI Analysis} \longrightarrow \text{Officer Verification} \longrightarrow \text{Final Enforcement Decision}$$
- **Fail-Safe SIH Demo Engine**: Operates seamlessly whether the Python backend & OCR are online or running in standalone client-side demo mode. The live presentation **never fails or crashes**.
- **Configurable Rules Engine**: Dynamic JSON rules modeling Rule 6 & Rule 9 of the *Legal Metrology (Packaged Commodities) Rules, 2011*.
- **Official PDF Reports**: Downloadable and printable dossiers with tamper-evident metadata, declaration audit logs, and digital officer sign-off.

---

## 💻 Technology Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, React Router DOM, Lucide React, Recharts
- **Backend**: Python 3.10+, FastAPI, Uvicorn, SQLite
- **Computer Vision & AI**: OpenCV, Pytesseract / Intelligent Semantic Fallback Parser
- **Reports**: ReportLab (Python PDF generation) & Browser Print Fallback
- **Database**: SQLite (`backend/vidhicheck.db`)

---

## 🚀 Quick Start Guide

### Prerequisites
- **Node.js** (v18 or higher) & **npm**
- **Python** (3.10 or higher) & **pip**

---

### 1. Start the Backend API (FastAPI)

```bash
# Navigate to the backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
python -m uvicorn main:app --reload --port 8000
```
- **API Server**: `http://127.0.0.1:8000`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`

---

### 2. Start the Frontend (React + Vite)

Open a second terminal window:

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the Vite development server
npm run dev
```
- **Web App**: `http://localhost:5173`

---

## 🔑 Demo Credentials

| Role | Officer ID | Password |
| :--- | :--- | :--- |
| **Legal Metrology Inspector** | `officer001` | `vidhicheck123` |

*(A 1-click **Auto-fill** button is also available on the login page for quick presentation).*

---

## 🎯 10-Step SIH Demo Presentation Script

1. **Sign In**: Navigate to `http://localhost:5173`. Click **Auto-fill** and log in with `officer001`.
2. **Dashboard Overview**: Show the 4 stat cards (*Total Inspections: 128, Compliant: 82, Non-Compliant: 31, Needs Verification: 15*) and the Recharts *Inspection Compliance Overview* chart.
3. **Start Inspection**: Click **Scan Product** in the sidebar or top header.
4. **Choose a Test Product**: Under **One-Click SIH Demo Sample Products**, select:
   - 🌾 **Sample 1: Premium Basmati Rice** $\rightarrow$ High-compliance scenario (Score: 94/100).
   - 🍪 **Sample 2: Packaged Biscuits** $\rightarrow$ Violation scenario (Missing Consumer Care helpline under Rule 6(1)(n)).
   - 🛢️ **Sample 3: Cooking Oil** $\rightarrow$ Low contrast / unclear address requiring physical inspection (Rule 9(1)).
5. **Or Upload Custom Image**: Drag and drop any food package photograph to preview dimensions and file information.
6. **Analyze**: Click **Analyze Product**. Observe the realistic 6-step verification animation:
   1. Image Processing ✓
   2. Detecting Label ✓
   3. Extracting Text ✓
   4. Identifying Declarations ✓
   5. Checking Legal Metrology Rules ✓
   6. Generating Compliance Result ✓
7. **Inspect Analysis Results**:
   - **Status Banner & Score**: Review the weighted score breakdown (*Mandatory Declarations, Format Checks, Readability*).
   - **Annotated Label Preview**: View interactive colored bounding boxes (*Green = Valid, Red = Violation, Yellow = Review*). Toggle layers on/off.
   - **Extracted Declarations**: View parsed values alongside OCR confidence percentages.
   - **Compliance Checklist**: Review checks against Rule 6 criteria.
   - **Detected Violations**: Highlight legal rule citations (e.g. *Rule 6(1)(n)*).
8. **Officer Verification**:
   - Select an enforcement action: **Confirm Violation**, **Reject Violation**, or **Needs Manual Review**.
   - Input Officer Remarks (e.g., *"Helpline missing on package. Notice issued."*).
   - Click **Submit Verification** to record the statutory decision.
9. **Generate PDF Report**:
   - Click **Download PDF Report** to trigger ReportLab server-side generation.
   - Or click **View Full Report** to preview the printable Government Inspection Dossier.
10. **Audit History**: Navigate to **Inspections** to search, filter by compliance status, and open past audits.

---

## ⚖️ Legal Metrology Compliance Rules

The rules engine checks mandatory declarations under **The Legal Metrology (Packaged Commodities) Rules, 2011**:

- **Rule 6(1)(a)**: Name and complete address of the manufacturer, packer, or importer.
- **Rule 6(1)(b)**: Generic or common name of the commodity.
- **Rule 6(1)(c)**: Net quantity in terms of standard unit of weight or measure (g, kg, ml, L).
- **Rule 6(1)(d)**: Month and year of manufacture or pre-packing.
- **Rule 6(1)(e)**: Maximum Retail Price (MRP inclusive of all taxes).
- **Rule 6(1)(n)**: Name, address, telephone number, and email of consumer care grievance cell.
- **Rule 9(1)**: Minimum font height, optical contrast, and conspicuity standards.

Rules can be configured directly in [`backend/rules/rules.json`](backend/rules/rules.json).

---

## 📁 Repository Structure

```text
VidhiCheck-Compliance-Checker/
│
├── frontend/                     # React + TypeScript + Tailwind + Vite
│   ├── src/
│   │   ├── components/           # Navbar, Sidebar, AnalysisModal, AnnotatedImage
│   │   ├── pages/                # Login, Dashboard, Scan, Result, History, Reports, About
│   │   ├── services/             # API client with auto offline fallback
│   │   ├── data/                 # Demo test fixtures & sample products
│   │   ├── App.tsx               # React Router DOM routes
│   │   ├── main.tsx              # React DOM entrypoint
│   │   └── index.css             # Tailwind CSS tokens
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── backend/                      # Python FastAPI Backend
│   ├── routes/
│   │   └── inspections.py        # /api/analyze, /api/verify, /api/report, /api/dashboard
│   ├── services/
│   │   ├── ocr_service.py        # Image processing & OCR extraction
│   │   ├── compliance_service.py # Statutory rules evaluation & scoring
│   │   └── report_service.py     # ReportLab PDF report generation
│   ├── rules/
│   │   └── rules.json            # Configurable Legal Metrology rules
│   ├── database.py               # SQLite schema & seeded demo inspections
│   ├── models.py                 # Pydantic data schemas
│   ├── main.py                   # FastAPI server entrypoint & CORS
│   └── requirements.txt
│
└── README.md
```

---

## 🛡️ License

Developed for academic and demonstration purposes for **Smart India Hackathon (SIH 2026)**.
