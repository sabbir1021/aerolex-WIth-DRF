from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User= get_user_model()
from accounts.helpers import get_tokens_for_user
from .serializers import UserSerializer, ProfileSerializer
from django.http import Http404
from base.decorator import userGuard

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
        serializer = ProfileSerializer(user)
        response = {
                "success": True,
                "message": "OK",
                "data" : serializer.data
            }
        return Response(response, status=status.HTTP_201_CREATED)


class ProfileUpdate(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, format=None):
        user = request.user
        serializer = ProfileSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        old_password = request.data['current_password']
        new_password =  request.data['new_password']
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            response = {
                    "success": True,
                    "message": "your password successfuly changes"
                }
        else:
            response = {
                    "success": False,
                    "message": "Your current password is not right."
                }
        return Response(response, status=status.HTTP_201_CREATED)

class UserCreate(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = User.objects.filter(agent__country = request.user.agent.country, user_type = request.user.user_type)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data['agent'] = request.user.agent.id
        request.data['user_type'] = request.user.user_type
        request.data['status'] = "active"
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSingle(APIView):
    permission_classes = [IsAuthenticated] 
    @userGuard
    def get(self, request, pk, format=None):
        snippet = User.objects.get(pk=pk)
        serializer = UserSerializer(snippet)
        return Response(serializer.data)

    @userGuard
    def patch(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = UserSerializer(snippet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)