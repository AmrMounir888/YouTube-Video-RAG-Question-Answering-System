# 🚀 [Tips Hindawi](https://www.tipshindawi.com/) Internship (August–October) 2026

> 🎓 This project was built during the [ **Tips Hindawi** ](https://www.tipshindawi.com/) **Internship (August–October) 2026**.

## 👤 Participant

| Field            | Value                                |
| ---------------- | ------------------------------------ |
| Full Name        | Amr Mounir Esmail Ahmed                   |
| Project Name     | YouTube Video RAG Question Answering System |
| GitHub Username  | [Your GitHub username]               |
| Internship Batch | August–October 2026                  |
| Training Program | Large Language Models (LLMs) Program |
| Organization     | [**Edrak for Ai**](https://edrak4ai.com/en) |

---

# 📖 Project Overview

The **YouTube Video RAG Question Answering System** lets a user paste a YouTube link and ask questions about the video in Arabic or English. The system fetches the video's transcript, splits it into timestamped chunks, and indexes them with multilingual embeddings. For each question, it retrieves the most relevant chunks and passes them to an LLM, which answers **only from the video's content**. If the video does not cover the question, the system says so instead of guessing.

The heavy parts (LLM and embeddings) run on a **Kaggle GPU** and are exposed through a **FastAPI** server and an **ngrok** tunnel. A lightweight **Streamlit** interface runs locally and talks to that API.

---

# ✨ Features

* Ask questions about any YouTube video that has a transcript (manual or auto-generated)
* Arabic and English support, with answers in the language of the question
* Retrieval-Augmented Generation (RAG): answers are grounded in the video transcript only
* Timestamped sources: every answer shows the video segments it came from, with clickable links
* Manual transcript fallback when YouTube blocks the server
* API key protection for the public endpoint
* Automatic re-indexing when the Kaggle session restarts
* GPU inference on Kaggle with a lightweight local UI

---

# 🛠️ Technologies Used

| Area | Tools |
| --- | --- |
| Language | Python |
| LLM | Qwen2.5-7B-Instruct (Hugging Face Transformers) |
| Embeddings | multilingual-e5-small (Sentence-Transformers) |
| Retrieval | NumPy cosine similarity |
| Transcript | youtube-transcript-api |
| Backend API | FastAPI, Uvicorn |
| Tunnel | ngrok (pyngrok) |
| Frontend | Streamlit |
| Compute | Kaggle Notebooks (GPU) |

---

# ⚙️ Installation

## 1. Backend (Kaggle)

1. Create a Kaggle notebook and enable **GPU** and **Internet**.
2. Install the dependencies:
   ```bash
   pip install -q youtube-transcript-api sentence-transformers fastapi uvicorn pyngrok accelerate
   ```
3. Run the notebook cells in order: models and RAG functions, then the API and ngrok cell.
4. Set your own values in the API cell:
   ```python
   API_TOKEN = "your-secret-key"      # protects the API
   NGROK_TOKEN = "your-ngrok-token"   # from dashboard.ngrok.com
   ```
5. Copy the printed `PUBLIC URL`.

## 2. Frontend (local)

```bash
pip install streamlit requests
```

Open `app.py` and set:

```python
API_URL = "https://your-domain.ngrok-free.dev"
API_KEY = "your-secret-key"   # must match API_TOKEN on Kaggle
```

---

# 🚀 Usage

1. Keep the Kaggle notebook running.
2. Start the interface:
   ```bash
   streamlit run app.py
   ```
3. In the sidebar, click **Test connection**.
4. Paste a YouTube link and click **Process video**.
5. Ask your questions in the chat box.
6. Open **Sources** under any answer to see the transcript segments used, with timestamps.

If YouTube blocks the server and returns a transcript error, paste the transcript manually in the expander (one line per sentence) and process again.

---

# 🧩 Architecture

```
Streamlit UI (local)
      │  HTTPS
      ▼
ngrok tunnel ──► FastAPI (Kaggle)
                    ├─ /index : transcript → chunks → embeddings
                    └─ /ask   : question → top-k chunks → LLM → answer + sources
```

---

# 📸 Demo

[Add screenshots, GIFs, or a demo video here]

---

# 📈 Results

* The system answers Arabic and English questions using only the video's transcript.
* Answers include timestamped sources, which makes them easy to verify.
* Questions the video does not cover are declined instead of answered from outside knowledge.
* [Add your own observations here: videos tested, languages, response time]

---

# ⚠️ Limitations

* The Kaggle session is temporary, so the index is lost when it stops (the UI re-indexes automatically).
* The free ngrok tunnel and Kaggle GPU limits affect availability.
* Only videos with an available transcript are supported.
* Retrieval quality depends on transcript quality, especially for auto-generated Arabic.

---

# 🔮 Future Improvements

* Persistent vector database (e.g., FAISS or Chroma) so indexes survive restarts
* Speech-to-text (Whisper) for videos without transcripts
* Conversation memory for follow-up questions
* Streaming answers token by token
* Support for playlists and multiple videos in one chat
* Hybrid search (keyword + semantic) and re-ranking for better retrieval

---

# 📚 About the Internship

This project was developed as part of the [**Tips Hindawi**](https://www.tipshindawi.com/) **Internship (August–October) 2026**, and it will be showcased on the official [Tips Hindawi](https://www.tipshindawi.com/) website.

[Tips Hindawi](https://www.tipshindawi.com/) is the internships department of [**Edrak for Ai**](https://edrak4ai.com/en), and the internship encourages participants to build real-world projects, apply practical skills, and showcase their work through GitHub.

For more information about the internship, training programs, and upcoming batches, visit the official [Tips Hindawi](https://www.tipshindawi.com/) website.

---

# 📄 License

This project is shared for educational and portfolio purposes.
