from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AIConversation
from app.schemas import (
    AIRequest,
    AIResponse,
    AIConversationResponse,
)
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant"],
)


# ======================================
# Ask AI
# ======================================

@router.post(
    "/ask",
    response_model=AIResponse,
)
def ask_ai(
    request: AIRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Replace this with OpenAI or another AI service later
    answer = (
        f"You asked: '{request.question}'. "
        "AI integration will be connected here."
    )

    conversation = AIConversation(
        question=request.question,
        answer=answer,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return AIResponse(answer=answer)


# ======================================
# Conversation History
# ======================================

@router.get(
    "/history",
    response_model=list[AIConversationResponse],
)
def conversation_history(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(AIConversation)
        .order_by(AIConversation.created_at.desc())
        .all()
    )


# ======================================
# Clear History
# ======================================

@router.delete("/history")
def clear_history(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db.query(AIConversation).delete()
    db.commit()

    return {
        "message": "Conversation history cleared successfully."
    }