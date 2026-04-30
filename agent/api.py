from typing import Optional, List, Dict, Any

from fastapi import FastAPI
from pydantic import BaseModel

from agent.seo_agent import load_model, seo_agent
from agent.rag_retriever import retrieve_context


app = FastAPI(
    title="Gemma SEO Agent API",
    description="API wrapper for the Gemma SEO LoRA agent with optional RAG.",
    version="0.1.0",
)

_model = None
_tokenizer = None


class AnswerRequest(BaseModel):
    prompt: str
    use_rag: bool = True
    show_sources: bool = False


class AnswerResponse(BaseModel):
    answer: str
    sources: Optional[List[Dict[str, Any]]] = None


@app.on_event("startup")
def startup_event():
    global _model, _tokenizer
    _model, _tokenizer = load_model()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": _model is not None,
        "adapter": "RajeevSK25/gemma4-e2b-seo-lora-v4-400",
    }


@app.post("/answer", response_model=AnswerResponse)
def answer(request: AnswerRequest):
    response = seo_agent(
        _model,
        _tokenizer,
        request.prompt,
        use_rag=request.use_rag,
        show_sources=False,
    )

    sources = None

    if request.show_sources and request.use_rag:
        sources = retrieve_context(request.prompt, top_k=2)

        # Remove full content from API response to keep it clean
        sources = [
            {
                "path": item["path"],
                "title": item["title"],
                "score": item["score"],
            }
            for item in sources
        ]

    return AnswerResponse(
        answer=response,
        sources=sources,
    )