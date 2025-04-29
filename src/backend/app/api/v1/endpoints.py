# File: src/backend/app/api/v1/endpoints.py

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserCreate, UserProfile, UserUpdate
from app.models.auth import Token
from app.models.assistant import AssistantRequest, AssistantResponse
from app.services import auth_service, user_service
from app.services.assistant_service import AssistantService
from app.dependencies import get_current_user
from fastapi import Body
from app.services.telegram_service import telegram_service

assistant_service = AssistantService()




router = APIRouter()


@router.post("/auth/register", response_model=Token)
def register_user(user: UserCreate):
    return auth_service.register(user)


@router.post("/auth/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    return auth_service.login(form_data.username, form_data.password)


@router.get("/user/profile", response_model=UserProfile)
def get_user_profile(current_user=Depends(get_current_user)):
    return user_service.get_profile(current_user)


@router.put("/user/profile", response_model=UserProfile)
def update_user_profile(data: UserUpdate, current_user=Depends(get_current_user)):
    return user_service.update_profile(current_user, data)


@router.post("/assistant/message", response_model=AssistantResponse)
def send_message_to_assistant(
    request: AssistantRequest, current_user=Depends(get_current_user)
):
    response = assistant_service.send_message(
        user=current_user,
        message=request.message,
        source="web"
    )
    return AssistantResponse(response=response)


@router.post("/webhook/telegram")
async def telegram_webhook(update: dict = Body(...)):
    return telegram_service.handle_update(update)
