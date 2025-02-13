from database.models import Users, Keys, Payments
from database.repository import SQLAlchemyRepository
from services.service import UserService, KeyService

class UserRepository(SQLAlchemyRepository):
    model = Users

class KeyRepository(SQLAlchemyRepository):
    model = Keys

class PaymentRepository(SQLAlchemyRepository):
    model = Payments

def user_service():
    return UserService(UserRepository)

def key_service():
    return KeyService(UserRepository, KeyRepository)

def payment_service():
    return KeyService(PaymentRepository, UserRepository)