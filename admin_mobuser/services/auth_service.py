
from fastapi import HTTPException
from admin_mobuser.utils.jwt_auth import JWTManager
from admin_mobuser.utils.password_manager import PasswordManager
from admin_mobuser.firebase_handler import FirestoreHandler
from admin_mobuser.models.user_model import UserSignup
from admin_mobuser.config.logging import LoggerConfig

logger = LoggerConfig('auth_service.py').get_logger()


class AuthService:
    def __init__(self):
        self.handler = FirestoreHandler()
        self.password_manager = PasswordManager()
        self.jwt_manager = JWTManager()

    def retrieve_user(self, email, password) -> dict:
        try:
            user = self.handler.fetch_data('tabUserss', email)
            if not user:
                return False
            if isinstance(user, list):
                user = user[0]
            if not self.password_manager.verify_password(password,
                                                         user.get('password')):
                return False
            access_token = self.jwt_manager.create_access_token(user)
            return {
                'access_token': access_token.get('access_token'),
                "user_id": user.get('id')
            }
        except Exception as e:
            logger.error(f"Error retrieving user {email}: {str(e)}")
            raise e

    def signup(self, user: UserSignup):
        try:
            hashed_password = self.password_manager.hash_password(
                user.password)
            data = {
                "email": user.email,
                "password": hashed_password,
                "phone_number": user.phone_number
            }
            user = self.handler.add_data('tabUserss', data)
            access_token = self.jwt_manager.create_access_token(data)

            return {
                "message": "User created Successfully",
                "email": data.get('email'),
                'access_token': access_token.get('access_token')
            }
        except Exception as e:
            logger.error(f"Exception creating user -> {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
