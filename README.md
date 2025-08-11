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

## 📷 Screenshots

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

<img width="1717" height="848" alt="1 Imara Chat Bot FR" src="https://github.com/user-attachments/assets/ec7f6937-d551-4ca9-b6c7-ac32048f4700" />

<img width="1717" height="844" alt="2 Imara Chat Bot FR" src="https://github.com/user-attachments/assets/8086e3a7-38b7-4846-b219-58027f25f6b6" />

<img width="1717" height="844" alt="3 Imara Chat Bot FR" src="https://github.com/user-attachments/assets/108a7c95-d1fd-4396-9099-765a300c1349" />

<img width="1717" height="844" alt="4 Imara Chat Bot FR" src="https://github.com/user-attachments/assets/5047fe49-cdb5-4fd1-8591-c4dbfa69cfd9" />

<img width="1717" height="844" alt="5 Imara Chat Bot FR" src="https://github.com/user-attachments/assets/8acb2c96-a09c-4dc4-a1c1-1e41d2a1bf2e" />

<img width="1717" height="844" alt="6 Imara Chat Bot FR" src="https://github.com/user-attachments/assets/3882e0ca-a83e-4c28-bdd3-f3a5ddd9ecd8" />

<img width="1717" height="844" alt="7 Imara Chat Bot FR" src="https://github.com/user-attachments/assets/517495c8-8a50-4619-8884-656b9b71549a" />

<img width="1717" height="844" alt="8 Imara Chat Bot FR" src="https://github.com/user-attachments/assets/79abc6a9-af36-410a-83a7-33870ee801f4" />

<img width="1717" height="844" alt="9 Imara Chat Bot FR" src="https://github.com/user-attachments/assets/0ea31fd1-e851-4bd6-aa50-392a172c3997" />

<img width="1717" height="844" alt="10 Imara Chat Bot FR" src="https://github.com/user-attachments/assets/97ae1833-e9b1-405e-b00c-33db1a248dc3" />

---

SPANISH

<img width="1717" height="848" alt="1 Imara Chat Bot ES" src="https://github.com/user-attachments/assets/9d5baf96-e63c-45da-9cd3-7d588aacdce7" />

<img width="1717" height="848" alt="2 Imara Chat Bot ES" src="https://github.com/user-attachments/assets/aeb93079-0b0e-4901-89c3-57341568fe4d" />

<img width="1717" height="848" alt="3 Imara Chat Bot ES" src="https://github.com/user-attachments/assets/19aa4e84-0532-4422-8ab7-8207d75aa92d" />

<img width="1717" height="848" alt="4 Imara Chat Bot ES" src="https://github.com/user-attachments/assets/60488b7a-cc96-486b-9d8e-39629067bc71" />

<img width="1717" height="848" alt="5 Imara Chat Bot ES" src="https://github.com/user-attachments/assets/6aba5a76-a6d7-472f-ac75-cc23a7d028fa" />

<img width="1717" height="848" alt="6 Imara Chat Bot ES" src="https://github.com/user-attachments/assets/2ffcef1d-a365-4736-b503-5c7a85bd3e54" />

<img width="1717" height="848" alt="7 Imara Chat Bot ES" src="https://github.com/user-attachments/assets/bbd1d3b0-dcde-464e-9f31-0568bf1ee448" />

<img width="1717" height="848" alt="8 Imara Chat Bot ES" src="https://github.com/user-attachments/assets/30e66350-7096-49f0-865b-a389ce56000e" />

---

PORTUGUESE

<img width="1717" height="848" alt="1 Imara Chat Bot PR" src="https://github.com/user-attachments/assets/0c4d74a2-1f65-4bf1-98cc-6e1f0e2bc7dd" />

<img width="1717" height="848" alt="2 Imara Chat Bot PR" src="https://github.com/user-attachments/assets/9d006bd2-c32d-4a72-90bc-91963b7ee199" />

<img width="1717" height="848" alt="3 Imara Chat Bot PR" src="https://github.com/user-attachments/assets/25f6a898-5564-4600-aca0-ce4c23b6c37a" />

<img width="1717" height="848" alt="4 Imara Chat Bot PR" src="https://github.com/user-attachments/assets/8280ca43-12b1-4e7c-afda-9fdce3150f2e" />

<img width="1717" height="848" alt="5 Imara Chat Bot PR" src="https://github.com/user-attachments/assets/a7947321-e483-4ebc-8be9-f5af12426ce3" />

<img width="1717" height="848" alt="6 Imara Chat Bot PR" src="https://github.com/user-attachments/assets/776a9401-ae84-49c2-83af-1c89e558c81f" />

<img width="1717" height="848" alt="7 Imara Chat Bot PR" src="https://github.com/user-attachments/assets/8f942aef-dd9c-4a68-92a5-a5f599523173" />

<img width="1717" height="848" alt="8 Imara Chat Bot PR" src="https://github.com/user-attachments/assets/5e9622f4-5d8f-4d01-a6b5-fbe5eb0a1af4" />

<img width="1717" height="848" alt="9 Imara Chat Bot PR" src="https://github.com/user-attachments/assets/07d5faa1-3d1d-4057-aa9f-240f37633cad" />

---

GERMAN

<img width="1717" height="848" alt="1 Imara Chat Bot DE" src="https://github.com/user-attachments/assets/d8709cc4-bec8-49b8-b5d0-1585e70d1662" />

<img width="1717" height="844" alt="2 Imara Chat Bot DE" src="https://github.com/user-attachments/assets/1ef58dd6-3e44-4688-b2ba-0c3593302f9d" />

<img width="1717" height="844" alt="3 Imara Chat Bot DE" src="https://github.com/user-attachments/assets/e6c905bc-d228-4927-9aa9-8d329403f986" />

<img width="1717" height="848" alt="4 Imara Chat Bot DE" src="https://github.com/user-attachments/assets/0588e6ba-9562-4e92-b326-a786934a9a19" />

<img width="1717" height="848" alt="5 Imara Chat Bot DE" src="https://github.com/user-attachments/assets/d0a5b7d7-7748-4f79-900e-e81459387cfd" />

<img width="1717" height="848" alt="6 Imara Chat Bot DE" src="https://github.com/user-attachments/assets/fda5b67f-03c1-422b-bcdb-f5b0e9284d39" />

<img width="1717" height="848" alt="7 Imara Chat Bot DE" src="https://github.com/user-attachments/assets/9c03ebee-63e1-4efc-839c-ef9961f9c996" />

<img width="1717" height="848" alt="8 Imara Chat Bot DE" src="https://github.com/user-attachments/assets/f3f7c8aa-2e4f-48c7-8693-3fa32c9f6059" />

<img width="1717" height="848" alt="9 Imara Chat Bot DE" src="https://github.com/user-attachments/assets/a61da5f0-55b7-4c81-ba35-f7313f9fc0ee" />

---

ITALIAN

<img width="1717" height="848" alt="1 Imara Chat Bot IT" src="https://github.com/user-attachments/assets/040f8229-00c0-496b-a25e-065bdcaaa683" />

<img width="1717" height="848" alt="2 Imara Chat Bot IT" src="https://github.com/user-attachments/assets/1ad3961e-6c9e-456f-89c0-81c943b51a28" />

<img width="1717" height="848" alt="3 Imara Chat Bot IT" src="https://github.com/user-attachments/assets/607999cc-9459-4f88-9c70-5911e870f851" />

<img width="1717" height="848" alt="4 Imara Chat Bot IT" src="https://github.com/user-attachments/assets/eefc23f7-42a3-4349-bb8d-b276be74aebf" />

<img width="1717" height="848" alt="5 Imara Chat Bot IT" src="https://github.com/user-attachments/assets/2dc5852b-cec5-44d8-ae76-504dc354dba6" />

<img width="1717" height="848" alt="6 Imara Chat Bot IT" src="https://github.com/user-attachments/assets/69229201-c660-4141-a9da-386778166151" />

<img width="1717" height="848" alt="7 Imara Chat Bot IT" src="https://github.com/user-attachments/assets/da6c1458-fb86-46d2-874c-367d37b30a46" />

<img width="1717" height="848" alt="8 Imara Chat Bot IT" src="https://github.com/user-attachments/assets/6f87af6d-840b-499b-afdc-d0139a378dd3" />

<img width="1717" height="848" alt="9 Imara Chat Bot IT" src="https://github.com/user-attachments/assets/64395cbd-c5ae-4919-b181-faf334049962" />

<img width="1717" height="848" alt="10 Imara Chat Bot IT" src="https://github.com/user-attachments/assets/2c36120d-8860-476a-b35b-729e0ae7b1a6" />

---

DUTCH

<img width="1717" height="848" alt="1 Imara Chat Bot NL" src="https://github.com/user-attachments/assets/644ebab3-3844-4624-a833-da0a40b8f353" />

<img width="1717" height="848" alt="2 Imara Chat Bot NL" src="https://github.com/user-attachments/assets/99ba58c3-de11-4171-8560-658096dd75df" />

<img width="1717" height="848" alt="3 Imara Chat Bot NL" src="https://github.com/user-attachments/assets/a03635e4-306f-4cff-b01c-2b20b304c822" />

<img width="1717" height="848" alt="4 Imara Chat Bot NL" src="https://github.com/user-attachments/assets/341c7f59-4a4c-41ea-9809-2500691c79fb" />

<img width="1717" height="848" alt="5 Imara Chat Bot NL" src="https://github.com/user-attachments/assets/c02442b4-07ba-412f-8a2c-b1db42b5b02f" />

<img width="1717" height="848" alt="6 Imara Chat Bot NL" src="https://github.com/user-attachments/assets/bb7d9ff7-5202-477e-b976-b3077e634742" />

<img width="1717" height="848" alt="7 Imara Chat Bot NL" src="https://github.com/user-attachments/assets/cbea78f6-d5a4-4b25-881a-772ddbfb1d0f" />

<img width="1717" height="848" alt="8 Imara Chat Bot NL" src="https://github.com/user-attachments/assets/a5132049-2e3d-41d4-a41d-6dfe106eb7aa" />

---

ARABIC

<img width="1717" height="848" alt="1 Imara Chat Bot AR" src="https://github.com/user-attachments/assets/9527906a-1f85-4eb1-adf4-65bdca262c59" />

<img width="1717" height="848" alt="2 Imara Chat Bot AR" src="https://github.com/user-attachments/assets/bb493037-b781-4e1e-854e-0177bbc04b19" />

<img width="1717" height="848" alt="3 Imara Chat Bot AR" src="https://github.com/user-attachments/assets/2c873f54-b30a-4ae3-bd61-a832d95a781a" />

<img width="1717" height="848" alt="4 Imara Chat Bot AR" src="https://github.com/user-attachments/assets/306efd42-5c08-426f-ad7b-722703d2ea34" />

<img width="1717" height="848" alt="5 Imara Chat Bot AR" src="https://github.com/user-attachments/assets/be0ef91f-a087-408f-816b-8784ab5676d6" />

<img width="1717" height="848" alt="6 Imara Chat Bot AR" src="https://github.com/user-attachments/assets/93280ce7-a372-469c-ba8c-deb692d42b96" />

<img width="1717" height="848" alt="7 Imara Chat Bot AR" src="https://github.com/user-attachments/assets/2587bb8c-e1bf-4301-97e4-9f64fa23ccec" />

<img width="1717" height="848" alt="8 Imara Chat Bot AR" src="https://github.com/user-attachments/assets/74eec1df-69fe-4075-9d45-bbbe30454d0d" />

<img width="1717" height="848" alt="9 Imara Chat Bot AR" src="https://github.com/user-attachments/assets/615ba585-acfc-4dd4-a1c9-64fcf9acb22c" />

<img width="1717" height="848" alt="10 Imara Chat Bot AR" src="https://github.com/user-attachments/assets/4169fab6-42e7-4b96-b8c4-44d52ac4cd54" />

---
