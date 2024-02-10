from ninja import Schema
from .models import Category, Order


class UserRegistrationSchema(Schema):
    username: str
    email: str
    password: str
    category: str


class CategorySchema(Schema):
    name: str


class OrderSchema(Schema):
    category: CategorySchema
    name: str
    description: str


class RelevantOrderSchema(OrderSchema):
    user: str
