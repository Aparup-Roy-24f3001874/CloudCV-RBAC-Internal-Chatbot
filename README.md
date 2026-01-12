---
title: CloudCV Internal Operations Chatbot
emoji: 🏢
colorFrom: green
colorTo: blue
sdk: docker
app_file: Dockerfile
pinned: false
license: mit
short_description: Secure RAG chatbot for CloudCV internal operations.
---

# 🏢 CloudCV Internal Operations Chatbot

A secure, role-based AI assistant built for **CloudCV internal operations**.  
It allows users to query internal documents safely using Retrieval-Augmented Generation (RAG) while enforcing strict Role-Based Access Control (RBAC).

---

## 👥 User Roles

| Role | Access |
|------|--------|
| **Admin** | Full access to all internal data |
| **Host** | Access to hosted projects and internal policies |
| **Participant** | Access to assigned project documents only |
| **Public** | Access to explicitly public documents only |

Unauthorized data is never retrieved or shown.

---

## ⚙️ How It Works

1. Users authenticate and receive a role.
2. Queries are filtered by role permissions.
3. Only authorized documents are retrieved from the vector store.
4. The LLM generates grounded answers from approved content.

---

## 🧠 Tech Stack

- LLM: Llama 3.1 (via Groq)
- Backend: FastAPI
- UI: Streamlit
- Vector Store: FAISS
- Embeddings: all-MiniLM-L6-v2
- Auth: JWT + SQLite
- Deployment: Docker on Hugging Face Spaces

---