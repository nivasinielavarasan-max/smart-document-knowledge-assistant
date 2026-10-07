# 📚 Smart Document Knowledge Assistant

An AI-powered web application that allows students and researchers to upload documents and ask questions about their content using Retrieval-Augmented Generation (RAG).

## 📌 Problem Statement

Students and researchers often work with large PDF documents such as lecture notes, research papers, study materials, and lab manuals. Finding specific information using normal keyword searches can be time-consuming.

This project provides a document-based AI assistant that allows users to upload PDF or TXT files and ask questions in natural language. The system searches the uploaded documents for relevant information and generates answers based only on the retrieved content.

## 🎯 Objective

The main objective of this project is to build a simple and user-friendly knowledge assistant that:

- Accepts PDF and TXT documents
- Extracts and processes their content
- Finds the most relevant sections for a user's question
- Uses AI to generate answers based on those sections
- Supports follow-up questions through conversational history
- Shows the documents used as sources for the answer

## 💡 Why This Problem Was Chosen

Students frequently have to search through lengthy lecture notes and study materials to find answers to specific questions. This can take considerable time, especially when information is spread across multiple documents.

The Smart Document Knowledge Assistant simplifies this process by combining semantic search with a local AI model. It allows users to interact with their study materials through natural-language questions instead of manually searching through pages.

## 🔍 Proposed Solution

The project uses a Retrieval-Augmented Generation (RAG) approach.

The system works in three main stages:

### 1. Retrieval

Uploaded documents are divided into smaller text chunks. Each chunk is converted into a numerical embedding using the `all-MiniLM-L6-v2` sentence-transformer model.

When a user asks a question, the question is also converted into an embedding. Cosine similarity is then used to identify the most relevant document chunks.

### 2. Augmentation

The top relevant chunks are combined with the user's question and previous conversation context.

This retrieved document information is provided to the language model as context.

### 3. Generation

The local Llama 3.2 3B language model, running through Ollama, generates an answer using the retrieved document context.

The system is instructed not to use outside knowledge and to state when the answer cannot be found in the uploaded documents.

## 🏗️ System Workflow

```text
User uploads PDF / TXT
          ↓
     Text Extraction
          ↓
      Text Chunking
          ↓
   Generate Embeddings
          ↓
     User Question
          ↓
 Question Embedding
          ↓
  Cosine Similarity Search
          ↓
 Top 3 Relevant Chunks
          ↓
 Retrieved Context + Question
          ↓
     Llama 3.2 3B
          ↓
      AI-generated Answer
          ↓
   Source Documents Shown
```

## 🛠️ Technologies / Tools Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application interface |
| PyPDF | PDF text extraction |
| Sentence Transformers | Document and query embeddings |
| all-MiniLM-L6-v2 | Local embedding model |
| Scikit-learn | Cosine similarity search |
| NumPy | Numerical data processing |
| Ollama | Local AI model execution |
| Llama 3.2 3B | Local language model |
| GitHub | Source code management |

## ✨ Key Features

- 📄 Upload PDF documents
- 📝 Upload TXT documents
- 📚 Support for multiple documents
- ✂️ Automatic document chunking
- 🧠 Local semantic embeddings
- 🔎 Similarity-based document search
- 🔝 Retrieval of the top 3 relevant chunks
- 🤖 AI-generated answers using Llama 3.2 3B
- 💬 Interactive chat interface
- 🔄 Follow-up questions using conversation history
- 📑 Source document identification
- 🗑️ Clear documents and chat history
- 🔐 Local AI processing without requiring an external AI API

## 📂 Project Structure

```text
smart-document-knowledge-assistant/
│
├── new.py
├── requirements.txt
├── .gitignore
└── README.md
## 🚀 How to Run the Project
```


### 1. Clone the repository

```bash
git clone https://github.com/nivasinielavarasan-max/smart-document-knowledge-assistant.git
cd smart-document-knowledge-assistant
pip install -r requirements.txt
ollama pull llama3.2:3b
streamlit run new.py
```
💬 Example Usage
1. Upload a lecture note or study material in PDF or TXT format.
2. Click Generate Embeddings.
3. Ask a question related to the uploaded material.
4. The system searches for the most relevant document sections.
5. Llama 3.2 3B generates an answer using the retrieved context.
6. The source document is displayed with the response.
7. Users can continue asking follow-up questions.
🔐 Privacy and Security
The current version uses local embeddings and a locally running Llama 3.2 3B model through Ollama.
The application does not require sending document content to an external AI API for the current implementation.
The .env file is excluded from GitHub using .gitignore to prevent accidental exposure of sensitive information.
🔮 Future Improvements
- Support for additional document formats such as DOCX and PPTX
- Page-number references for retrieved information
- Improved document chunking strategies
- More advanced ranking and retrieval
- User authentication
- Persistent document storage
- Public cloud deployment
- Support for larger and more capable language models
- Improved citation and source highlighting
👩‍💻 Author
Nivasini Elavarasan
B.Tech CSE – Cybersecurity
VIT Chennai
Project Links
GitHub Repository:
https://github.com/nivasinielavarasan-max/smart-document-knowledge-assistant
Project Type
Academic / Student Project
This project demonstrates the practical implementation of Retrieval-Augmented Generation, semantic search, document processing, and local AI-assisted question answering
