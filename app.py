# app.py
import streamlit as st
from speech_utils import transcribe_audio
from image_utils import generate_image_from_text
from memory_brain import build_index, search_memory
from contextual_memory import find_related_memories
from doc_utils import extract_text_from_file
from supabase_utils import upload_file, save_memory_to_db, fetch_memories

st.set_page_config(page_title="Memory Preserver AI", page_icon="🧠")
st.title("🧠 AI Memory Preserver")

menu = st.sidebar.selectbox(
    "Menu",
    ["Add Memory", "View Memories", "Search Memories", "Memory Brain AI"]
)

# =========================
# ADD MEMORY
# =========================
if menu == "Add Memory":
    st.subheader("Write a Memory")
    text_memory = st.text_area("Type your memory here")

    st.subheader("Upload Files (Optional)")
    audio_file = st.file_uploader("Upload Audio", type=["wav","mp3"])
    doc_file = st.file_uploader("Upload Document", type=["pdf","txt","docx"])
    user_image = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])
    image_description = st.text_area("Image Description (Optional)")

    if st.button("Save Memory"):
        # Construct memory text
        memory_text = text_memory or ""

        # Handle audio
        audio_url = None
        if audio_file:
            transcription = transcribe_audio(audio_file)
            memory_text += "\n" + transcription
            audio_url = upload_file(audio_file)

        # Handle document
        doc_url = None
        if doc_file:
            doc_text = extract_text_from_file(doc_file)
            memory_text += "\n" + doc_text
            doc_url = upload_file(doc_file)

        # Handle image
        image_url = None
        if user_image:
            if image_description:
                memory_text += "\n" + image_description
            image_url = upload_file(user_image)
        elif memory_text:
            image_url = generate_image_from_text(memory_text)

        # Save memory
        save_memory_to_db(memory_text, audio_url, image_url, doc_url)
        st.success("Memory saved successfully!")
        if image_url:
            st.image(image_url, caption="Memory Image", use_column_width=True)

# =========================
# VIEW MEMORIES
# =========================
elif menu == "View Memories":
    st.subheader("All Memories")
    memories = fetch_memories()
    for mem in memories:
        st.markdown("---")
        st.write(mem["memory_text"])
        if mem["image_path"]:
            st.image(mem["image_path"], caption="Memory Image", use_column_width=True)
        if mem["audio_path"]:
            st.audio(mem["audio_path"])
        if mem["doc_path"]:
            st.markdown(f"[Download Document]({mem['doc_path']})")

# =========================
# SEARCH MEMORIES
# =========================
elif menu == "Search Memories":
    keyword = st.text_input("Enter keyword to search memories")
    if keyword:
        memories = fetch_memories()
        results = [m for m in memories if keyword.lower() in m["memory_text"].lower()]
        for mem in results:
            st.markdown("---")
            st.write(mem["memory_text"])
            if mem["image_path"]:
                st.image(mem["image_path"], caption="Memory Image", use_column_width=True)
            if mem["audio_path"]:
                st.audio(mem["audio_path"])
            if mem["doc_path"]:
                st.markdown(f"[Download Document]({mem['doc_path']})")

# =========================
# MEMORY BRAIN AI
# =========================
elif menu == "Memory Brain AI":
    st.subheader("Talk with your memories")
    if st.button("Rebuild Memory Brain"):
        build_index()
        st.success("Memory brain updated!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask about your memories...")
    if user_input:
        st.session_state.messages.append({"role":"user","content":user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Fetch memories for AI
        memories = fetch_memories()
        all_memory_texts = [m["memory_text"] for m in memories]

        semantic_results = search_memory(user_input)
        contextual_results = find_related_memories(user_input)

        response = ""
        if contextual_results:
            response += "💭 This reminds me of something you shared before:\n\n"
            for mem in contextual_results:
                response += f"• {mem}\n"
        response += "\n🧠 Based on your memories:\n\n"
        for mem in semantic_results:
            response += f"• {mem}\n"

        st.session_state.messages.append({"role":"assistant","content":response})
        with st.chat_message("assistant"):
            st.write(response)