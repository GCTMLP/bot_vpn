from database.models import Users, Keys
from database.repository import SQLAlchemyRepository
from services.service import UserService, KeyService

class UserRepository(SQLAlchemyRepository):
    model = Users

class KeyRepository(SQLAlchemyRepository):
    model = Keys

def user_service():
    return UserService(UserRepository)

def key_service():
    return KeyService(UserRepository, KeyRepository)