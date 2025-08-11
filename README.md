# 💬 Imara Chat Bot

**Imara** is a multilingual FAQ chatbot for **Africa Love Match**, designed to assist users with common questions about subscriptions, profiles, privacy, and more.
Built with **Streamlit**, **OpenAI**, and **Firestore**, it delivers a friendly, interactive user experience in **8 languages**: English, Arabic, German, Spanish, French, Italian, Dutch, and Portuguese.

---

## 📚 Table of Contents

1. [Features](#-features)
2. [Project Structure](#-project-structure)
3. [Installation](#-installation)
4. [Usage](#-usage)
5. [Testing](#-testing)
6. [CI/CD](#-cicd)
7. [Configuration](#-configuration)
8. [Contributing](#-contributing)
9. [License](#-license)

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
