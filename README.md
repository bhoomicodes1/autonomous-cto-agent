# 🚀 Autonomous Startup CTO Agent

An AI-powered GitHub Repository Analysis Platform that helps engineers, founders, and CTOs understand any codebase using Retrieval-Augmented Generation (RAG), Large Language Models, and intelligent repository analysis.

🌐 **Live Demo:** https://autonomous-cto-agent.vercel.app/

---

## ✨ Features

- 🤖 AI-powered GitHub repository analysis
- 📂 Automatic repository ingestion
- 🧠 Retrieval-Augmented Generation (RAG)
- 🔍 Semantic code search using Qdrant
- 💬 AI chat with repository context
- 🏗 Architecture analysis
- 📊 Repository Health Score
- 🌳 Interactive Architecture Graph
- 🔗 Dependency Graph
- ⚡ FastAPI backend
- 🎨 React + Vite frontend
- 🐳 Docker support
- ☁️ Production deployment on Render & Vercel

---

## 🏗 System Architecture

```text
GitHub Repository
        │
        ▼
Repository Ingestion
        │
        ▼
Chunking
        │
        ▼
Gemini Embeddings
        │
        ▼
Qdrant Vector Database
        │
        ▼
Retriever
        │
        ▼
LangGraph Workflow
        │
        ▼
Gemini 2.5 Flash
        │
        ▼
Repository Analysis & AI Chat
```

---

## 🛠 Tech Stack

### Backend

- FastAPI
- LangGraph
- Google Gemini API
- Qdrant
- PostgreSQL
- Docker
- Async Python

### Frontend

- React
- Vite
- React Flow
- React Markdown
- Axios

### AI / GenAI

- Gemini 2.5 Flash
- Gemini Embeddings
- RAG
- Semantic Search

---

## 🚀 Key Capabilities

### Repository Analysis

- Executive Summary
- Architecture Review
- Tech Stack Detection
- Folder Structure Analysis
- Code Flow Explanation
- Technical Debt Detection
- Scalability Review
- Security Review
- CTO Recommendations

---

### AI Repository Chat

Ask questions like:

- Explain the architecture
- How does authentication work?
- Which file starts the application?
- Explain the RAG pipeline
- Describe the dependency graph

---

## 📊 Repository Health Metrics

The platform evaluates repositories based on:

- Code Quality
- Documentation
- Test Coverage
- Maintainability
- Project Structure

---

## 📁 Project Structure

```text
backend/
    app/
        api/
        core/
        graph/
        services/
        db/

frontend/
    src/
        components/
        pages/
```

---

## ⚙️ Local Setup

### Clone

```bash
git clone https://github.com/bhoomicodes1/autonomous-cto-agent.git
```

### Backend

```bash
cd backend
uv sync
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🌐 Deployment

### Frontend

- Vercel

### Backend

- Render

### Vector Database

- Qdrant Cloud

### Database

- PostgreSQL

---

## 📸 Screenshots

> Add screenshots of:

- Home Page
- Repository Analysis
- AI Chat
- Architecture Graph
- Repository Health

---

## 🔮 Future Improvements

- Streaming Responses
- Multi Repository Support
- Authentication
- Private Repository Analysis
- MCP Integration
- Code Review Agent
- PR Review Agent

---

## 👩‍💻 Author

**Bhoomi Gaur**

B.Tech CSE (AI & ML)

GitHub: https://github.com/bhoomicodes1

---

⭐ If you found this project useful, consider giving it a star.
