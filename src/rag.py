from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from .config import load_config
from .faq_loader import load_faqs

config = load_config()
embeddings = OpenAIEmbeddings(model=config['openai_embedding_model'])

faqs = load_faqs()

def build_vectorstore():
    docs = []
    for state, data in faqs.items():
        if 'messages' in data and 'en' in data['messages']:
            text = data['messages']['en']
            docs.append(Document(page_content=text, metadata={"state": state}))
    if not docs:
        raise ValueError("No English FAQ messages found for embedding.")
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("faiss_index")
    return vectorstore

# Load or build vectorstore
try:
    vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
except Exception:
    vectorstore = build_vectorstore()

def retrieve(query, lang_code, top_k=3):
    results = vectorstore.similarity_search(query, k=top_k)
    contexts = []
    for doc in results:
        state = doc.metadata['state']
        if state in faqs and lang_code in faqs[state].get('messages', {}):
            contexts.append(faqs[state]['messages'][lang_code])
    return contexts