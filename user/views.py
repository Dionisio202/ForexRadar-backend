from rest_framework.views import APIView
from rest_framework.response import Response
from supabase_py import create_client

supabase_url = 'https://dcvauwnbzpxhdgggpzsg.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRjdmF1d25ienB4aGRnZ2dwenNnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxMTg1OTUwNCwiZXhwIjoyMDI3NDM1NTA0fQ.AMi6GxQIuajsWeL_WQLSFFsXAfOufTwIpaN4gJxb8G4'
client = create_client(supabase_url, supabase_key)

class Register(APIView):
    def post(self, request):
        # Obtener datos de la solicitud
     try:
        email = request.query_params.get('email')
        password = request.query_params.get('password')
        name=request.query_params.get('name')
        lastName=request.query_params.get('lastName')
        if not email or not password:
            return Response({'error': 'Debes proporcionar un correo electrónico y una contraseña'}, status=400)

        # Autenticar el usuario
        auth_response = client.auth.sign_up(email, password)
        
        # Verificar el resultado de la autenticación
        if 'status_code' in auth_response and auth_response['status_code'] == 200:
            user_id = auth_response.get('id')
            profile_data = {
                    'user_id': user_id,
                    'name': name,
                    'last_name':lastName,
                }
            profile_table = client.table('profile')
            profile_response = profile_table.insert(profile_data).execute()
            # Autenticación exitosa
            # Aquí puedes devolver el token de acceso u otra información relevante
            return Response({'Registrado con exito'})
        elif 'status_code' in auth_response and auth_response['status_code'] == 429:
            return Response({'Limite de registros excedidos'}, status=429)
        elif 'status_code' in auth_response and auth_response['status_code'] == 409:
            return Response({'El correo ya esta registrado'}, status=409)
     except Exception as e:
        # Manejar cualquier excepción que ocurra durante la autenticación
            return Response({'error': str(e)}, status=500)

class Login(APIView):
    def post(self, request):
        try:
            # Obtener datos de la solicitud
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                return Response({'error': 'Debes proporcionar un correo electrónico y una contraseña'}, status=400)

            # Configurar el cliente Supabase
        
            # Autenticar el usuario
            auth_response = client.auth.sign_in(email, password)
          
                # Verificar el resultado de la autenticación
            if 'status_code' in auth_response and auth_response['status_code'] == 200:
                # Autenticación exitosa
                # Aquí puedes devolver el token de acceso u otra información relevante
                  return Response({'token': auth_response['user'] })
            else:
                # Autenticación fallida
                # Devolver un mensaje de error
                return Response({'error': auth_response.get('error', auth_response)}, status=400)
        except Exception as e:
            # Manejar cualquier excepción que ocurra durante la autenticación
            return Response({'error': auth_response}, status=500)

class getProfile(APIView):
    def post(self, request):
        try:
            # Obtener el ID del perfil desde la solicitud
            profile_id = request.data.get('id')

            if not profile_id:
                return Response({'error': 'Debes proporcionar un ID de perfil'}, status=400)


            # Consultar el perfil desde Supabase
            profile = client.from_('profile').select('*').eq('user_id', profile_id).execute().get('data')

            if not profile:
                return Response({'error': 'No se encontró un perfil con el ID proporcionado'}, status=404)

            # Devolver los datos del perfil en la respuesta
            return Response(profile)

        except Exception as e:
            # Manejar cualquier excepción que ocurra durante la recuperación de datos del perfil
            return Response({'error': str(e)}, status=500)
        
class UpdateProfileName(APIView):
    def put(self, request):
        try:
            # Obtener el ID del perfil y el nuevo nombre desde la solicitud
            profile_id = request.data.get('id')
            new_name = request.data.get('name')

            if not profile_id or not new_name:
                return Response({'error': 'Debes proporcionar un ID de perfil y un nuevo nombre'}, status=400)
            # Actualizar el nombre del perfil en Supabase
            updated_profile = client.table('profile').update({'name': 'Australia'}).eq('user_id','c4ab36ae-614d-49d1-952b-3dfb025cb5fc').execute()

            # Verificar si la actualización fue exitosa
            if updated_profile.get('count', 0) > 0:
                # Actualización exitosa
                return Response({'message': 'Nombre de perfil actualizado con éxito'})
            else:
                # La actualización falló
                return Response({'error': 'No se pudo actualizar el nombre del perfil'}, status=400)

        except Exception as e:
            # Manejar cualquier excepción que ocurra durante la actualización del perfil
            return Response({'error': str(e)}, status=500)

class changePassword(APIView):
    def post(self, request):
        try:
            # Obtener datos de la solicitud
            email = request.data.get('email')
            new_password = request.data.get('password')

            if not email or  not new_password:
                return Response({'error': 'Debes proporcionar un correo electrónico, contraseña actual y nueva contraseña'}, status=400)

            # Configurar el cliente Supabase
        
            # Cambiar la contraseña del usuario
            auth_response = client.auth.update({
                 'email': email,
                'password': new_password
            })

            # Verificar el resultado de la actualización de contraseña
            if 'status_code' in auth_response and auth_response['status_code'] == 200:
                # Contraseña cambiada exitosamente
                return Response({'message': 'Contraseña cambiada exitosamente'})
            else:
                # Error al cambiar la contraseña
                return Response({'error': auth_response.get('error', auth_response)}, status=400)
        except Exception as e:
            # Manejar cualquier excepción que ocurra durante el cambio de contraseña
            return Response({'error': str(e)}, status=500)
