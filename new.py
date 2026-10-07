import streamlit as st
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import ollama


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="Smart Document Knowledge Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Smart Document Knowledge Assistant")

st.write(
    "Upload your PDF or TXT documents and ask questions "
    "using an AI-powered document assistant."
)


# --------------------------------------------------
# LOAD EMBEDDING MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():

    model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


model = load_model()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "embeddings" not in st.session_state:
    st.session_state.embeddings = []

if "sources" not in st.session_state:
    st.session_state.sources = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("📚 Document Manager")

    uploaded_files = st.file_uploader(
        "Upload PDF or TXT files",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    st.divider()

    st.subheader("📊 Project Status")

    st.write(
        "Documents:",
        len(set(st.session_state.sources))
    )

    st.write(
        "Chunks:",
        len(st.session_state.chunks)
    )

    st.write(
        "Chat messages:",
        len(st.session_state.chat_history)
    )

    st.divider()

    if st.button(
        "🗑️ Clear Everything",
        use_container_width=True
    ):

        st.session_state.chunks = []
        st.session_state.embeddings = []
        st.session_state.sources = []
        st.session_state.chat_history = []

        st.rerun()


# --------------------------------------------------
# TEXT EXTRACTION
# --------------------------------------------------

def extract_text(uploaded_file):

    text = ""

    if uploaded_file.name.lower().endswith(".pdf"):

        reader = PdfReader(uploaded_file)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text = text + page_text + "\n"

    else:

        text = uploaded_file.read().decode("utf-8")

    return text


# --------------------------------------------------
# CREATE CHUNKS
# --------------------------------------------------

def create_chunks(
    text,
    chunk_size=1000,
    overlap=150
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk)

        start = end - overlap

    return chunks


# --------------------------------------------------
# CREATE EMBEDDING
# --------------------------------------------------

def get_embedding(text):

    embedding = model.encode(text)

    return embedding


# --------------------------------------------------
# SEARCH RELEVANT CHUNKS
# --------------------------------------------------

def search_chunks(
    question,
    chunks,
    embeddings,
    sources
):

    question_embedding = get_embedding(question)

    scores = cosine_similarity(
        [question_embedding],
        embeddings
    )[0]

    top_indexes = scores.argsort()[-3:][::-1]

    results = []

    for index in top_indexes:

        results.append(
            (
                chunks[index],
                scores[index],
                sources[index]
            )
        )

    return results


# --------------------------------------------------
# GENERATE ANSWER
# --------------------------------------------------

def generate_answer(
    question,
    results
):

    context = ""

    for i, (
        chunk,
        score,
        source
    ) in enumerate(results):

        context = context + "\n\n"

        context = context + (
            "SOURCE "
            + str(i + 1)
            + ": "
            + source
            + "\n"
        )

        context = context + chunk


    conversation = ""

    for message in st.session_state.chat_history:

        conversation = conversation + "\n"

        conversation = conversation + (
            message["role"]
            + ": "
            + message["content"]
        )


    prompt = """
You are a document knowledge assistant.

Answer the user's question using ONLY the information
provided in the document context.

Do not use outside knowledge.

Use the conversation history to understand
follow-up questions.

If the answer cannot be found in the documents,
say:

"I could not find the answer in the uploaded documents."

Give a clear and simple answer.

CONVERSATION HISTORY:
""" + conversation + """

DOCUMENT CONTEXT:
""" + context + """

CURRENT QUESTION:
""" + question


    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# --------------------------------------------------
# PROCESS DOCUMENTS
# --------------------------------------------------

if uploaded_files:

    st.subheader("📄 Uploaded Documents")

    all_chunks = []
    all_sources = []

    for uploaded_file in uploaded_files:

        text = extract_text(uploaded_file)

        chunks = create_chunks(text)

        all_chunks.extend(chunks)

        for chunk in chunks:

            all_sources.append(
                uploaded_file.name
            )

        with st.expander(
            "📄 " + uploaded_file.name
        ):

            st.write(
                "Characters extracted:",
                len(text)
            )

            st.write(
                "Number of chunks:",
                len(chunks)
            )

    st.session_state.chunks = all_chunks
    st.session_state.sources = all_sources


    # --------------------------------------------------
    # GENERATE EMBEDDINGS
    # --------------------------------------------------

    if st.button(
        "🧠 Generate Embeddings",
        use_container_width=True
    ):

        embeddings = []

        with st.spinner(
            "Generating document embeddings..."
        ):

            for chunk in all_chunks:

                embedding = get_embedding(chunk)

                embeddings.append(embedding)

        st.session_state.embeddings = embeddings

        st.success(
            "Embeddings generated successfully!"
        )


# --------------------------------------------------
# CHAT
# --------------------------------------------------

if len(st.session_state.embeddings) > 0:

    st.divider()

    st.subheader("💬 Chat with Your Documents")

    # Display previous messages

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.write(message["content"])

            if message["role"] == "assistant":

                st.caption(
                    "📚 Sources: "
                    + ", ".join(message["sources"])
                )


    question = st.chat_input(
        "Ask a question about your documents..."
    )


    if question:

        search_query = question

        previous_questions = []

        for message in st.session_state.chat_history:

            if message["role"] == "user":

                previous_questions.append(
                    message["content"]
                )

        if previous_questions:

            search_query = (
                previous_questions[-1]
                + " "
                + question
            )


        # Retrieve relevant chunks

        with st.spinner(
            "🔎 Searching your documents..."
        ):

            results = search_chunks(
                search_query,
                st.session_state.chunks,
                st.session_state.embeddings,
                st.session_state.sources
            )


        # Save user message

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )


        # Generate answer

        with st.spinner(
            "🤖 Generating answer..."
        ):

            answer = generate_answer(
                question,
                results
            )


        # Get source names

        source_names = []

        for chunk, score, source in results:

            if source not in source_names:

                source_names.append(source)


        # Save assistant response

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": source_names
            }
        )

        st.rerun()


# --------------------------------------------------
# CLEAR CHAT
# --------------------------------------------------

if len(st.session_state.chat_history) > 0:

    if st.button("🗑️ Clear Chat"):

        st.session_state.chat_history = []

        st.rerun()


# --------------------------------------------------
# START MESSAGE
# --------------------------------------------------

if len(st.session_state.embeddings) == 0:

    st.info(
        "👈 Upload a PDF or TXT document from the sidebar "
        "to get started."
    )
