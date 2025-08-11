from fastapi import FastAPI, Body, HTTPException
import logging

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from .config import load_config
from .rag import retrieve

logger = logging.getLogger(__name__)
config = load_config()
llm = ChatOpenAI(model="gpt-4o")

app = FastAPI()

rag_prompt = ChatPromptTemplate.from_template(
    "You are IMARA, a friendly assistant for Africa Love Match, helping {name} "
    "with FAQs in their preferred language. Use the following retrieved contexts to answer the question accurately and conversationally. "
    "If the user mentions soccer or football, add a friendly nod to Africa Soccer Kings. "
    "Keep responses concise, friendly, and professional, using emojis like 😊 and 💖. "
    "If you don't know the answer, say so.\n\nContexts: {context}\n\nQuestion: {query}"
)

@app.post("/generate")
def generate(body: dict = Body(...)):
    try:
        query = body['query']
        lang_code = body['lang_code']
        is_soccer_enthusiast = body.get('is_soccer_enthusiast', False)
        name = body['name']

        contexts = retrieve(query, lang_code)
        context_str = "\n\n".join(contexts) if contexts else "No relevant context found."

        prompt = rag_prompt.format_prompt(name=name, context=context_str, query=query)
        response = llm.invoke(prompt)

        answer = response.content

        if is_soccer_enthusiast and any(kw in query.lower() for kw in ["soccer", "football"]):
            answer += f" Loving the soccer spirit, {name}! ⚽ Connect with more Africa Soccer Kings fans!"

        return {"response": answer}
    except Exception as e:
        logger.error(f"Error in generate: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/feedback")
def feedback(body: dict = Body(...)):
    try:
        conversation_history = body['conversation_history']

        feedback_prompt = (
            "You are a helpful tool providing feedback on a user's interaction with IMARA, the Africa Love Match FAQ chatbot. "
            "Give a score from 1 to 10 based on how well the user engaged with the chatbot (e.g., clarity of questions, relevance to FAQs). "
            "Follow this format:\n"
            "Overall Score: //Your score\n"
            "Feedback: //Your feedback\n"
            "Do not ask questions or engage further."
        )

        response = llm.invoke([("system", feedback_prompt), ("user", f"Conversation history:\n{conversation_history}")])

        return {"feedback": response.content}
    except Exception as e:
        logger.error(f"Error in feedback: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")