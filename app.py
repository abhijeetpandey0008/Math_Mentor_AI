import streamlit as st
import tempfile
from pydub import AudioSegment
import shutil

# Force pydub to find ffmpeg in Streamlit Cloud
AudioSegment.converter = shutil.which("ffmpeg")
AudioSegment.ffmpeg = shutil.which("ffmpeg")
AudioSegment.ffprobe = shutil.which("ffprobe")

# ─── IMPORTS ───
# IMPORTANT: load audio tool first (sets ffmpeg path)
from tools.audio_tool import transcribe_audio
from audiorecorder import audiorecorder
from graph.agent_graph import build_graph
from utils.input_processor import process_input
from memory.memory_db import save_memory, retrieve_similar

# ─── 1. PAGE CONFIGURATION & CSS ───
st.set_page_config(page_title="AI Math Mentor", page_icon="✨", layout="centered")

# Custom CSS for a professional, clean chat interface
st.markdown("""
    <style>
    /* Clean up the top padding to make it look like a native app */
    .block-container { padding-top: 2rem; padding-bottom: 5rem; }
    
    /* User message bubble (Soft Blue) */
    .stChatMessage:has([data-testid="stIconUser"]) { 
        background-color: #f0f4f9; 
        border-radius: 15px; 
        padding: 10px; 
    }
    
    /* AI Assistant message bubble (Clean White with border) */
    .stChatMessage:has([data-testid="stIconAssistant"]) { 
        background-color: #ffffff; 
        border-radius: 15px; 
        padding: 10px; 
        border: 1px solid #e0e0e0; 
    }
    
    /* Hide default file uploader text to make it compact */
    .stFileUploader > div > div > div > div > small { display: none; }
    </style>
""", unsafe_allow_html=True)

# ─── 2. INITIALIZE GRAPH ───
@st.cache_resource
def get_graph():
    return build_graph()

graph = get_graph()

# ─── 3. SESSION STATE MANAGEMENT ───
if "messages" not in st.session_state:
    st.session_state.messages = []

# Dynamic keys: These allow us to clear the uploaders AFTER the message is sent
if "file_key" not in st.session_state:
    st.session_state.file_key = 0
if "audio_key" not in st.session_state:
    st.session_state.audio_key = 100

# ─── 4. SIDEBAR & HEADER ───
with st.sidebar:
    st.title("✨ Math Mentor")
    st.caption("Your intelligent exam prep assistant.")
    st.divider()
    
    # New Chat Button
    if st.button("➕ New Conversation", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.session_state.file_key += 1  # Resets the uploaders
        st.session_state.audio_key += 1
        st.rerun()

st.title("What can I help you solve today?")

# ─── 5. DISPLAY CHAT HISTORY ───
for msg in st.session_state.messages:
    avatar = "🧑‍🎓" if msg["role"] == "user" else "✨"
    with st.chat_message(msg["role"], avatar=avatar):
        if msg.get("file_preview"):
            st.image(msg["file_preview"], width=250)
        elif msg.get("is_pdf"):
            st.caption("📄 PDF Attached")
        st.markdown(msg["content"])

# ─── 6. INPUT ATTACHMENTS (Grouped in an Expander) ───
st.write("") # Quick spacer
with st.expander("📎 Attach Image, PDF, or Voice Note"):
    c1, c2, c3 = st.columns(3)
    
    with c1:
        # Dynamic key applied here
        uploaded_file = st.file_uploader("Image / PDF", type=["png","jpg","jpeg","pdf"], key=f"file_{st.session_state.file_key}", label_visibility="collapsed")
    with c2:
        audio_file = st.file_uploader("Audio File", type=["wav","mp3","m4a"], key=f"audio_{st.session_state.audio_key}", label_visibility="collapsed")
    with c3:
        st.caption("Record Voice")
        recorded_audio = audiorecorder("🎤 Record", "🛑 Recording...", key=f"mic_{st.session_state.audio_key}")

# Smooth UX: Let the user know the file is ready and waiting for their text prompt
if uploaded_file:
    st.success("📎 File attached! Type what you want me to do with it and press Enter.")

# ─── 7. THE MAIN TRIGGER ───
prompt = st.chat_input("Ask a math question...")

# We trigger the generation if they hit Enter OR if they just finished a voice note
if prompt or (recorded_audio and len(recorded_audio) > 0) or audio_file:
    
    base_text = prompt if prompt else ""
    user_display = base_text

    # Handle Audio Transcriptions
    if recorded_audio and len(recorded_audio) > 0:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            recorded_audio.export(tmp.name, format="wav")
            transcript = transcribe_audio(tmp.name)
            base_text = (base_text + " " + transcript).strip()
            if not user_display: 
                user_display = f"🎤 *Voice Note:* {transcript}"
                
    elif audio_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_file.read())
            tmp.flush()
            transcript = transcribe_audio(tmp.name)
            base_text = (base_text + " " + transcript).strip()
            if not user_display: 
                user_display = f"🎧 *Audio File:* {transcript}"

    if not user_display and uploaded_file:
        user_display = "Please solve the attached problem."

    # ─── 8. RENDER USER MESSAGE IMMEDIATELY ───
    # We display it instantly so the user knows the app is working
    with st.chat_message("user", avatar="🧑‍🎓"):
        is_pdf = uploaded_file and "pdf" in uploaded_file.type
        has_image = uploaded_file and "image" in uploaded_file.type
        
        if has_image:
            st.image(uploaded_file, width=250)
        elif is_pdf:
            st.caption("📄 PDF Attached")
            
        st.markdown(user_display)

    # Process the text and file together
    final_question = process_input(base_text, uploaded_file)

    # Handle Memory Commands (history, previous)
    q = final_question.lower()
    if any(phrase in q for phrase in ["previous question", "what did i ask", "history"]):
        with st.chat_message("assistant", avatar="✨"):
            st.markdown("### Previous Questions")
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.write("• " + msg["content"].replace("🎤 *Voice Note:* ", "").replace("🎧 *Audio File:* ", ""))
        st.stop()

    # ─── 9. ASSISTANT GENERATION ───
    with st.chat_message("assistant", avatar="✨"):
        with st.spinner("Analyzing and solving..."):
            
            past_solution = retrieve_similar(final_question)
            memory_entry = None

            if past_solution:
                # Memory Hit
                st.info("⚡ Retrieved similar problem from memory")
                st.markdown(f"### **Solution:**\n{past_solution['solution']}")
                with st.expander("📚 View Details"):
                    st.write("**Explanation:** Retrieved from memory.")
                    st.caption(f"**Confidence:** {past_solution.get('confidence', 'N/A')}")
                
                response_content = f"**Solution:** {past_solution['solution']}\n\n*Retrieved from memory.*"
            else:
                # Graph Invocation
                result = graph.invoke({"question": final_question})
                
                st.markdown(f"### **Solution:**\n{result.get('solution', 'No solution found.')}")
                with st.expander("📚 View Step-by-Step Explanation"):
                    st.write(result.get("explanation", "No explanation provided."))
                    st.divider()
                    st.caption(f"**Topic Detected:** {result.get('topic', 'N/A').title().replace('_', ' ')}")
                    st.caption(f"**AI Confidence Score:** {result.get('confidence', 'N/A')}")

                response_content = f"### **Solution:**\n{result.get('solution')}\n\n**Explanation:**\n{result.get('explanation')}"
                
                memory_entry = {
                    "question": final_question,
                    "solution": result.get("solution"),
                    "confidence": result.get("confidence"),
                    "feedback": None
                }

    # ─── 10. SAVE STATES & RERUN ───
    # Append the completed messages to session state
    st.session_state.messages.append({
        "role": "user",
        "content": user_display,
        "file_preview": uploaded_file if has_image else None,
        "is_pdf": is_pdf
    })
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_content
    })
    
    if memory_entry:
        save_memory(memory_entry)

    # Magic Reset: Incrementing these keys completely clears the uploaders for the next question
    st.session_state.file_key += 1
    st.session_state.audio_key += 1
    
    # Rerun to refresh the UI cleanly

    st.rerun()
