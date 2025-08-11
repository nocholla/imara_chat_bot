import logging
from firebase_admin import credentials, firestore, initialize_app

from .config import load_config

logger = logging.getLogger(__name__)

config = load_config()

cred = credentials.Certificate(config['firestore_credentials'])
initialize_app(cred)
db = firestore.client()

def load_faqs():
    faqs = {}
    try:
        for doc in db.collection('ImaraChatBot').stream():
            faqs[doc.id] = doc.to_dict()
        if not faqs:
            logger.warning("No FAQs found in Firestore. Using default or empty.")
        logger.info("FAQs loaded from Firestore")
        return faqs
    except Exception as e:
        logger.error(f"Error loading FAQs from Firestore: {e}")
        raise