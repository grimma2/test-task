from ninja import Router, Form, NinjaAPI
from .models import Order, CustomUser
from django.contrib.auth import get_user_model
from .serializers import OrderSchema, UserRegistrationSchema, RelevantOrderSchema
from ninja.security import APIKeyQuery
from rest_framework.authtoken.models import Token


router = NinjaAPI()


class ApiKey(APIKeyQuery):
    param_name = "api_key"

    def authenticate(self, request, key):
        try:
            return CustomUser.objects.get(key=key)
        except CustomUser.DoesNotExist:
            pass


api_key = ApiKey()


@router.post("/register/", response=dict)
def register_user(request, user: UserRegistrationSchema):
    User = get_user_model()
    new_user = User.objects.create_user(
        username=user.username,
        email=user.email,
        password=user.password,
        category=user.category
    )

    # Generate a token for the new user
    token, created = Token.objects.get_or_create(user=new_user)

    return {"token": token.key}


@router.post("/orders/", auth=api_key)
def create_order(request, order: OrderSchema):
    return Order.objects.create(category=order.category, name=order.name, description=order.description, user=request.user)


@router.get("/relevant-orders/", response=list[RelevantOrderSchema], auth=api_key)
def relevant_orders(request):
    user_category = request.user.category
    relevant_orders = Order.objects.filter(category=user_category)

    return relevant_orders.values()
