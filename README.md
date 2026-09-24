# 🛡️ CampusGuard AI

An AI-powered safety monitoring system that analyzes images/video for potential security concerns — unattended bags and possible falls — using computer vision, custom reasoning logic, and an LLM-powered agent that writes human-readable incident reports.

🔗 **Live Demo:** [campusguard-ai-dk5d.onrender.com/docs](https://campusguard-ai-dk5d.onrender.com/docs)

> Note: hosted on a free tier — the first request may take 30-50s to wake up.

## What it does

1. **Detects objects** in an uploaded image using YOLOv8 (people, bags, etc.)
2. **Flags suspicious bags** — bags with no person detected nearby, using proximity-based reasoning
3. **Flags possible falls** — using body aspect-ratio analysis (a fallen person's bounding box is wider than it is tall)
4. **Investigates concerning findings** with a LangGraph agent that assesses severity and writes a natural-language incident report via an LLM (Groq)
5. **Returns results** as structured JSON via a REST API, or as an annotated image with bounding boxes and labels

## Tech Stack

| Layer | Tools |
|---|---|
| Computer Vision | YOLOv8 (Ultralytics), OpenCV |
| Backend / API | FastAPI, Uvicorn |
| Agentic AI | LangGraph, LangChain-Groq |
| LLM | Groq (`openai/gpt-oss-20b`) |
| Deployment | Render |

## Architecture

Image upload → YOLO detection → Rule-based flagging (proximity / aspect ratio)
→ [if concerning] → LangGraph agent → severity assessment → LLM incident report
→ JSON response (or annotated image)


## API Endpoints

### `POST /analyze`
Upload an image, get back structured JSON with detection counts, findings, severity, and AI-generated incident reports for anything flagged.

### `POST /analyze-image`
Upload an image, get back the same image with bounding boxes and labels drawn on it (green = safe/standing, red = suspicious/possible fall).

## Running locally

```bash
git clone https://github.com/Bindukeshav/campusguard-ai.git
cd campusguard-ai
pip install -r requirements.txt
```

Create a `.env` file:


Run the server:
```bash
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` to test interactively.

## Project Structure

├── main.py # FastAPI app and endpoints
├── analyzer.py # YOLO detection + safety logic (bag proximity, fall detection)
├── agent.py # LangGraph agent for severity assessment + report generation
├── requirements.txt
└── Dockerfile


## Why this project

Built as an end-to-end demonstration of combining classical computer vision, rule-based reasoning, and agentic LLM workflows into a single deployable system — the kind of pipeline used in real-world security and safety monitoring platforms.

## Author

**Bindu K** — [GitHub](https://github.com/Bindukeshav) · [LinkedIn](https://linkedin.com/in/bindu-keshav-380b34425)
