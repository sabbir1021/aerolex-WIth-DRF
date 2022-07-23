from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User= get_user_model()
from accounts.helpers import get_tokens_for_user
from .serializers import UserSerlializer
# Create your views here.

class LoginView(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            raise ValidationError(
                detail={'message':'email and password if required'}, code=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email__exact=email)
            if not user.check_password(raw_password=password):
                raise ValidationError(detail={'message':'invalid password'}, code=status.HTTP_400_BAD_REQUEST)
            token = get_tokens_for_user(user)
            response = {
                "success": True,
                "message": "OK",
                "meta_info": None,
                "data" : {
                'access_token': token['access'],
                'refresh_token': token['refresh'],
            }}
            return Response(response, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            raise ValidationError(detail='user not found', code=status.HTTP_404_NOT_FOUND)



class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerlializer(user)
        response = {
                "success": True,
                "message": "OK permission ",
                "data" : serializer.data
            }
        return Response(response, status=status.HTTP_201_CREATED)



