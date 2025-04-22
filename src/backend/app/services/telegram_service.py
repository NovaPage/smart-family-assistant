import requests
from app.repositories.user_repository import (
    get_user_by_telegram_token,
    update_user_telegram_chat_id,
    get_user_by_chat_id
)
from app.services.assistant_service import AssistantService
from app.models.user import UserInDB
from app.core.config import settings
from app.models.assistant import AssistantRequest

assistant_service = AssistantService()

class TelegramService:
    def __init__(self, assistant_service_instance):
        self.assistant_service = assistant_service_instance
        self.telegram_api_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    def handle_update(self, update: dict) -> dict:
        message = update.get("message")
        if not message:
            return {"status": "no_message"}

        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if text.startswith("/start "):
            token = text.split("/start ")[1].strip()
            return self._handle_start_command(chat_id, token)

        user = get_user_by_chat_id(chat_id)
        if not user:
            self._send_message(chat_id, "❌ No estás autorizado para usar este bot.")
            return {"status": "unauthorized"}

        return self._handle_user_message(chat_id, text, user)

    def _handle_start_command(self, chat_id: int, token: str) -> dict:
        user = get_user_by_telegram_token(token)
        if not user:
            self._send_message(chat_id, "❌ Token inválido o expirado.")
            return {"status": "invalid_token"}

        update_user_telegram_chat_id(user.id, chat_id)
        self._send_message(chat_id, f"✅ ¡Hola {user.name}! Tu cuenta fue vinculada exitosamente.")
        return {"status": "linked"}

    from app.models.assistant import AssistantRequest  # Asegúrate de tener esto al inicio del archivo

    def _handle_user_message(self, chat_id: int, text: str, user: UserInDB) -> dict:
        try:
            assistant_response = self.assistant_service.process_message(
                current_user=user,
                request=AssistantRequest(message=text, source="telegram")
            )
            response_text = assistant_response.response
        except Exception as e:
            response_text = "❌ Hubo un error al procesar tu mensaje."
            print(f"Error procesando mensaje para usuario {user.id}: {e}")

        self._send_message(chat_id, response_text)
        return {"status": "replied", "reply": response_text}


    def _send_message(self, chat_id: int, text: str):
        payload = {
            "chat_id": chat_id,
            "text": text
        }
        try:
            requests.post(self.telegram_api_url, json=payload, timeout=10)
        except Exception as e:
            print(f"Error al enviar mensaje a Telegram: {e}")
