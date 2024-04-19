from rest_framework.views import APIView
from rest_framework.response import Response
from supabase_py import create_client

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

        # Configurar el cliente Supabase
        supabase_url = 'https://dcvauwnbzpxhdgggpzsg.supabase.co'
        supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRjdmF1d25ienB4aGRnZ2dwenNnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxMTg1OTUwNCwiZXhwIjoyMDI3NDM1NTA0fQ.AMi6GxQIuajsWeL_WQLSFFsXAfOufTwIpaN4gJxb8G4'
        client = create_client(supabase_url, supabase_key)

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
            return Response({'Registrado con exito':auth_response})
        elif 'status_code' in auth_response and auth_response['status_code'] == 429:
            return Response({'Limite de registros excedidos'}, status=429)
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
            supabase_url = 'https://dcvauwnbzpxhdgggpzsg.supabase.co'
            supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRjdmF1d25ienB4aGRnZ2dwenNnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxMTg1OTUwNCwiZXhwIjoyMDI3NDM1NTA0fQ.AMi6GxQIuajsWeL_WQLSFFsXAfOufTwIpaN4gJxb8G4'
            client = create_client(supabase_url, supabase_key)

            # Autenticar el usuario
            auth_response = client.auth.sign_in(email, password)
          
                # Verificar el resultado de la autenticación
            if 'status_code' in auth_response and auth_response['status_code'] == 200:
                # Autenticación exitosa
                # Aquí puedes devolver el token de acceso u otra información relevante
                  return Response({'token': auth_response['user']['id'] })
            else:
                # Autenticación fallida
                # Devolver un mensaje de error
                return Response({'error': auth_response.get('error', auth_response)}, status=400)
        except Exception as e:
            # Manejar cualquier excepción que ocurra durante la autenticación
            return Response({'error': auth_response}, status=500)

