# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# REGISTER
class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            username = email  # usamos el email como username
            first_name = request.data.get('name')
            last_name = request.data.get('lastName')

            if not email or not password:
                return Response({'error': 'Debes proporcionar un correo electrónico y una contraseña'}, status=400)

            if User.objects.filter(email=email).exists():
                return Response({'error': 'El correo ya está registrado'}, status=409)

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            return Response({'message': 'Registrado con éxito'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)

# LOGIN
class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            username = email  # si usamos el email como username

            if not email or not password:
                return Response({'error': 'Debes proporcionar un correo electrónico y una contraseña'}, status=400)

            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'email': user.email
                })
            else:
                return Response({'error': 'Credenciales inválidas'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

# GET PROFILE
class getProfile(APIView):
    def post(self, request):
        try:
            user_id = request.data.get('id')
            if not user_id:
                return Response({'error': 'Debes proporcionar un ID de usuario'}, status=400)

            user = User.objects.filter(id=user_id).first()

            if not user:
                return Response({'error': 'No se encontró un usuario con el ID proporcionado'}, status=404)

            return Response({
                'user_id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

# UPDATE PROFILE NAME
class UpdateProfileName(APIView):
    def put(self, request):
        try:
            user_id = request.data.get('id')
            new_name = request.data.get('name')

            if not user_id or not new_name:
                return Response({'error': 'Debes proporcionar un ID de usuario y un nuevo nombre'}, status=400)

            user = User.objects.filter(id=user_id).first()
            if not user:
                return Response({'error': 'Usuario no encontrado'}, status=404)

            user.first_name = new_name
            user.save()

            return Response({'message': 'Nombre actualizado con éxito'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)

# CHANGE PASSWORD
class changePassword(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            new_password = request.data.get('password')

            if not email or not new_password:
                return Response({'error': 'Debes proporcionar un correo electrónico y nueva contraseña'}, status=400)

            user = User.objects.filter(email=email).first()
            if not user:
                return Response({'error': 'Usuario no encontrado'}, status=404)

            user.set_password(new_password)
            user.save()

            return Response({'message': 'Contraseña actualizada con éxito'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
