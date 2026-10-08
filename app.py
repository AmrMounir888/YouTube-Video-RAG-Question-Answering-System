import os

import requests
import streamlit as st


API_URL = "https://photo-willpower-crayfish.ngrok-free.dev"
API_KEY = "change-me-to-a-long-random-string"  # <--- لازم يساوي API_TOKEN في Kaggle بالظبط

API_URL = os.getenv("RAG_API_URL", API_URL)
API_KEY = os.getenv("RAG_API_KEY", API_KEY)

st.set_page_config(page_title="YouTube RAG", page_icon="🎬", layout="wide")

st.markdown(
    """
    <style>
    .stChatMessage p, .stChatMessage li { unicode-bidi: plaintext; text-align: start; }
    textarea, input { unicode-bidi: plaintext; }
    </style>
    """,
    unsafe_allow_html=True,
)

ss = st.session_state
ss.setdefault("api_url", API_URL)
ss.setdefault("api_key", API_KEY)
ss.setdefault("video", None)   
ss.setdefault("chats", {})     


def call_api(method: str, path: str, timeout: int = 60, **kwargs):
    base = ss.api_url.strip().rstrip("/")
    if not base.startswith("http"):
        raise RuntimeError("API URL is missing or invalid.")
    try:
        r = requests.request(
            method,
            base + path,
            headers={
                "x-api-key": ss.api_key,
                "ngrok-skip-browser-warning": "1",
            },
            timeout=timeout,
            **kwargs,
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            f"Cannot reach the server ({type(e).__name__}). "
            "Is the Kaggle notebook still running, and is the URL up to date?"
        )
    if r.status_code != 200:
        try:
            detail = r.json().get("detail", r.text)
        except ValueError:
            detail = r.text[:200]
        raise RuntimeError(f"{r.status_code}: {detail}")
    return r.json()


def ask_with_reindex(vid: str, question: str):
 
    payload = {"video_id": vid, "question": question}
    try:
        return call_api("POST", "/ask", timeout=300, json=payload)
    except RuntimeError as e:
        if not str(e).startswith("404"):
            raise
        call_api(
            "POST", "/index", timeout=900,
            json={
                "url": ss.video["url"],
                "manual_transcript": ss.video.get("transcript", ""),
            },
        )
        return call_api("POST", "/ask", timeout=300, json=payload)


with st.sidebar:
    st.header("⚙️ Server")
    ss.api_url = st.text_input("API URL", ss.api_url)
    ss.api_key = st.text_input("API Key", ss.api_key, type="password")
    if st.button("Test connection", use_container_width=True):
        try:
            info = call_api("GET", "/health", timeout=15)
            st.success(f"Connected. Indexed videos: {len(info['videos'])}")
        except RuntimeError as e:
            st.error(str(e))

    if ss.video:
        st.divider()
        st.subheader("🎬 Current video")
        st.video(ss.video["url"])
        if st.button("Clear chat", use_container_width=True):
            ss.chats[ss.video["video_id"]] = []
            st.rerun()

st.title("🎬 YouTube Video Q&A")
st.caption("Ask questions about a YouTube video. Answers come only from its transcript.")

with st.form("index_form"):
    url = st.text_input("YouTube link", placeholder="https://www.youtube.com/watch?v=...")
    with st.expander("YouTube blocked the server? Paste the transcript manually"):
        manual = st.text_area("Transcript (one line per sentence)", height=150)
    submitted = st.form_submit_button("Process video", type="primary")

if submitted:
    if not url.strip():
        st.warning("Enter a video link.")
    else:
        try:
            with st.spinner("Fetching transcript and building the index..."):
                res = call_api(
                    "POST", "/index", timeout=900,
                    json={"url": url.strip(), "manual_transcript": manual},
                )
            ss.video = {
                "video_id": res["video_id"],
                "url": url.strip(),
                "manual": res.get("manual", False),
                "transcript": manual,
            }
            ss.chats.setdefault(res["video_id"], [])
            if res.get("cached"):
                st.success("Video was already indexed. Ready.")
            else:
                st.success(
                    f"Ready: {res['chunks']} chunks from {res['segments']} segments."
                )
            st.rerun()
        except RuntimeError as e:
            st.error(str(e))

if ss.video:
    vid = ss.video["video_id"]
    history = ss.chats[vid]

    def render_sources(sources):
        with st.expander(f"Sources ({len(sources)})"):
            for s in sources:
                if ss.video.get("manual"):
                    st.markdown(f"**{s['time']}**")
                else:
                    link = f"https://youtu.be/{vid}?t={s['seconds']}"
                    st.markdown(f"[**{s['time']}**]({link})")
                st.caption(s["text"] + "...")

    for m in history:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if m.get("sources"):
                render_sources(m["sources"])

    question = st.chat_input("Ask about the video...")
    if question:
        history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            try:
                with st.spinner("Thinking..."):
                    res = ask_with_reindex(vid, question)
                st.markdown(res["answer"])
                render_sources(res["sources"])
                history.append(
                    {"role": "assistant", "content": res["answer"], "sources": res["sources"]}
                )
            except RuntimeError as e:
                st.error(str(e))
                history.pop()
else:
    st.info("Process a video to start chatting.")