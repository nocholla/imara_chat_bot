# 💬 Imara Chat Bot

**Imara** is a multilingual FAQ chatbot for **Africa Love Match**, designed to assist users with common questions about subscriptions, profiles, privacy, and more.
Built with **Streamlit**, **OpenAI**, and **Firestore**, it delivers a friendly, interactive user experience in **8 languages**: English, Arabic, German, Spanish, French, Italian, Dutch, and Portuguese.

---

## 📚 Table of Contents

1. [Features](#-features)
2. [Tech Stack](#-tech-stack)
3. [Project Structure](#-project-structure)
4. [Installation](#-installation)
5. [Usage](#-usage)
6. [Testing](#-testing)
7. [CI/CD](#-cicd)
8. [Configuration](#-configuration)
9. [Contributing](#-contributing)
10. [License](#-license)
11. [Screenshots](#-screenshots)

---

## ✨ Features

* **Multilingual Support** – Responds in 8 supported languages.
* **Personalized Interaction** – Collects user details for tailored responses.
* **Soccer Enthusiast Detection** – Adds themed messaging for football fans.
* **Chat History Tracking** – Saves conversations to `data/chat_history.csv` for analytics.
* **Feedback System** – Requests engagement feedback after 5 messages.
* **Firestore Integration** – Retrieves FAQs from Firestore.
* **Streamlit UI** – Clean and interactive interface.
* **OpenAI Integration** – Uses GPT-4o for dynamic responses.
* **Docker Support** – Easy deployment via Docker.

---

## 🖥 Tech Stack

**Frameworks & Libraries**

* [Streamlit](https://streamlit.io/) – Frontend UI for chatbot interaction
* [FastAPI](https://fastapi.tiangolo.com/) – Backend API for chatbot and feedback handling
* [LangChain](https://www.langchain.com/) – Retrieval-Augmented Generation (RAG) pipeline
* [FAISS](https://faiss.ai/) – Vector similarity search
* [PyYAML](https://pyyaml.org/) – Configuration file parsing
* [Pytest](https://pytest.org/) – Unit & integration testing

**AI & NLP**

* [OpenAI GPT-4o](https://openai.com/) – Natural language understanding & generation
* [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings) – Semantic search
* [Transformers](https://huggingface.co/transformers/) – Model utilities
* [Datasets](https://huggingface.co/docs/datasets) – Data handling for model development

**Database & Cloud**

* [Firebase Firestore](https://firebase.google.com/docs/firestore) – FAQ and data storage
* [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup) – Admin access to Firestore

**Data Processing**

* Pandas – Data storage and analysis
* NumPy – Numerical computations
* SciPy – Scientific computing
* Scikit-learn – Machine learning utilities
* Joblib – Model persistence

**Deployment**

* Docker – Containerized deployment
* GitHub Actions – CI/CD pipeline

---

## 📂 Project Structure

```
imara_chat_bot/
├── streamlit/secrets.toml    # Streamlit secrets (e.g., OPENAI_API_KEY)
├── config.yaml               # Configuration file
├── Dockerfile                # Docker configuration
├── requirements.txt          # Python dependencies
├── .gitignore                # Ignores secrets, data, models, etc.
├── secrets/                  # Sensitive files
│   └── serviceAccountKey.json # Firestore credentials
├── data/                     # Data storage
│   └── chat_history.csv      # Chatbot conversation history
├── models/                   # Model storage (unused for now)
├── src/                      # Source code
│   ├── __init__.py
│   ├── config.py             # Config loader (renamed from data_loader)
│   ├── faq_loader.py         # Load FAQs from Firestore
│   ├── rag.py                # RAG setup with LangChain and FAISS
│   └── llm_pipeline.py       # FastAPI backend for generation and feedback
├── ui/                       # Streamlit UI
│   └── streamlit_chatbot.py  # Chatbot UI
├── tests/                    # Tests
│   ├── __init__.py
│   ├── test_config.py        # Test config loading
│   ├── test_llm_pipeline.py  # Test FastAPI endpoints
│   └── test_chatbot.py       # Test chatbot functionality
├── .github/                  # CI/CD
│   └── workflows/
│       └── ci.yml            # GitHub Actions
└── README.md                 # Documentation
```

---

## 🛠 Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-repo/imara_chat_bot.git
cd imara_chat_bot
```

**2. Set up a virtual environment**

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure secrets**

* Create `streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "your-openai-api-key"
```

* Add Firestore credentials to `secrets/serviceAccountKey.json`.
* Update `config.yaml`:

```yaml
data_dir: "data"
firestore_credentials: "secrets/serviceAccountKey.json"
openai_api_key: "your-openai-api-key"  # Optional if using secrets.toml
```

**5. Run locally**

```bash
streamlit run ui/streamlit_chatbot.py
```

**6. Run with Docker (optional)**

```bash
docker build -t imara-chat-bot .
docker run -p 8501:8501 -p 8000:8000 imara-chat-bot
```

---

## 🚀 Usage

1. Open the Streamlit app at **[http://localhost:8501](http://localhost:8501)**.
2. Enter your profile details (name, language, interests).
3. Choose FAQ options or ask free-form questions.
4. Receive feedback after 5 messages.
5. Conversations are logged to `data/chat_history.csv`.

**Example:**

* Selecting **Profile Edit** → Imara guides profile updates.
* Mentioning “soccer” → Adds Africa Soccer Kings-themed message.

---

## 🧪 Testing

Run all tests:

```bash
pytest tests/
```

**Key tests:**

* `test_chatbot_initialization` – UI loads successfully.
* `test_chat_history_saving` – Confirms chat history persistence.
* `test_data_loader` – Checks configuration loading.
* `test_llm_pipeline` – Tests API endpoints.

---

## 🔄 CI/CD

Configured in `.github/workflows/ci.yml` to:

* Run tests on pushes/PRs.
* Build & deploy Docker image (if enabled).

---

## ⚙️ Configuration

* **`config.yaml`** – Data paths & credentials.
* **`secrets.toml`** – Stores sensitive API keys.
* **`requirements.txt`** – Dependencies such as:

  * `streamlit>=1.38.0`
  * `openai>=1.45.0`
  * `firebase-admin>=6.5.0`
  * `pandas>=2.2.2`

---

## 🤝 Contributing

1. Fork this repository.
2. Create a branch:

   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit changes:

   ```bash
   git commit -m "Add your feature"
   ```
4. Push & open a pull request.

Please ensure all tests pass before submitting.

---

## 📜 License

Licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 📜 Screenshots

ENGLISH

<img width="1717" height="848" alt="1 Imara Chat Bot EN" src="https://github.com/user-attachments/assets/f506a392-1bd7-4f79-9c2e-6f669ebcf14b" />

<img width="1717" height="844" alt="2 Imara Chat Bot EN" src="https://github.com/user-attachments/assets/36fa9f76-e023-4094-9b1d-4fab20b738b7" />

<img width="1717" height="844" alt="3 Imara Chat Bot EN" src="https://github.com/user-attachments/assets/1621d475-7994-4c47-ae77-18716b9cfb94" />

<img width="1717" height="844" alt="4 Imara Chat Bot EN" src="https://github.com/user-attachments/assets/e03b66d8-8b8d-4d92-89fa-862a366c1e1b" />

<img width="1717" height="844" alt="5 Imara Chat Bot EN" src="https://github.com/user-attachments/assets/03f3a17e-a3a0-472f-b2f6-50857da12917" />

<img width="1717" height="844" alt="6 Imara Chat Bot EN" src="https://github.com/user-attachments/assets/ae227b33-7388-42dc-b77d-81a7b8a1d553" />

<img width="1717" height="844" alt="7 Imara Chat Bot EN" src="https://github.com/user-attachments/assets/4a05de84-ad9d-4b2c-9310-18b06f63ef69" />

<img width="1717" height="844" alt="8 Imara Chat Bot EN" src="https://github.com/user-attachments/assets/78c12a85-8921-4796-b86e-66d0a2aabf17" />

<img width="1717" height="844" alt="9 Imara Chat Bot EN" src="https://github.com/user-attachments/assets/004fa841-eb2c-43f6-b7d7-fc125fd0b7d4" />

<img width="1717" height="844" alt="10 Imara Chat Bot EN" src="https://github.com/user-attachments/assets/2e34b654-4f6a-4c7a-90b2-294130501dff" />

<img width="1717" height="844" alt="11 Imara Chat Bot EN" src="https://github.com/user-attachments/assets/d368bf0f-9ce6-4451-be06-2b8d11af9e48" />

<img width="1717" height="844" alt="12 Imara Chat Bot EN" src="https://github.com/user-attachments/assets/b5c2c2c9-90e2-4854-90aa-a063c6502952" />

<img width="1717" height="844" alt="13 Imara Chat Bot EN" src="https://github.com/user-attachments/assets/ebbf3d52-9343-44d8-b8ac-d8d38be5353f" />

<img width="1717" height="844" alt="14 Imara Chat Bot EN" src="https://github.com/user-attachments/assets/8bdf983a-32d6-4777-be61-cfe946acfd8e" />

<img width="1717" height="844" alt="15 Imara Chat Bot EN" src="https://github.com/user-attachments/assets/5314be3b-7b03-4a97-9b6b-3b3e9b4dc93c" />

---

FRENCH

---

SPANISH

---

PORTUGUESE

---

GERMAN

---

ITALIAN

---

DUTCH

---

ARABIC

---
