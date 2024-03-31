from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from rest_framework import status 
from supabase_py import create_client

class TableData(APIView):
    def get(self, request, format=None):
        try:
            # Obtener los parámetros del par de divisas y las fechas
            currency_pair = request.query_params.get('divisas')
            start_date_str = request.query_params.get('period1')
            end_date_str = request.query_params.get('period2')
            frequency = request.query_params.get('frequency')

            # Convertir las fechas a objetos de fecha
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')

            # Convertir las fechas a formato Unix
            start_unix = int(start_date.timestamp())
            end_unix = int(end_date.timestamp())

            # URL base de la página con los datos históricos de la divisa
            base_url = f'https://au.finance.yahoo.com/quote/{currency_pair}/history'

            # Construir la URL con los parámetros proporcionados
            url = f'{base_url}?period1={start_unix}&period2={end_unix}&interval={frequency}&filter=history&frequency={frequency}&includeAdjustedClose=true'

            # Configuración del navegador
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")  # Maximizar la ventana del navegador
            options.add_argument("--headless") 
            driver = webdriver.Chrome(options=options)

            # Abrir la página de Yahoo Finance
            driver.get(url)
            time.sleep(3)

            # Hacer scroll hasta el final de la página
            iter = 1
            while True:
                scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
                height = 250 * iter
                driver.execute_script("window.scrollTo(0, " + str(height) + ");")
                if height > scroll_height + 700:
                    print('End of page')
                    break

                iter += 1

            # En este punto, toda la información dinámica debe haberse cargado
            # Puedes agregar aquí el código para extraer los datos que necesitas

            # Crear objeto BeautifulSoup para analizar el HTML
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Encontrar la tabla de datos históricos
            table = soup.find('table', {'class': 'W(100%) M(0)'})

            # Verificar si se encontró la tabla
            if table:
                # Encontrar todas las filas de la tabla
                rows = table.find_all('tr')

                # Lista para almacenar los datos extraídos
                data = []

                # Iterar sobre las filas para extraer los datos
                for row in rows:
                    # Encontrar todas las celdas de la fila
                    cells = row.find_all('td')
                    # Extraer el texto de las celdas y agregarlo a la lista de datos
                    row_data = [cell.get_text(strip=True) for cell in cells]
                    # Verificar si la fila contiene datos válidos (no está vacía y no es la fila no deseada)
                    if len(row_data) > 1:
                        data.append(row_data)


                # Retornar los datos extraídos como respuesta
                return Response(data)
            else:
                return Response({'error': 'No se encontró la tabla de datos históricos'}, status=500)
        except Exception as e:
            # Manejar cualquier error y retornar una respuesta de error
            return Response({'error': str(e)}, status=500)
        finally:
            # Cerrar el navegador
            driver.quit()

class DivisaAPIView(APIView):
    def get(self, request):
        try:
            # Obtener el parámetro 'divisas' de la solicitud GET
            currency_pair = request.query_params.get('divisas')

            # Normalizar el formato del par de divisas
            normalized_currency_pair = currency_pair.replace("/", "")

            # Construir la URL utilizando el nombre de la divisa normalizado
            url = f"https://au.finance.yahoo.com/quote/{normalized_currency_pair}%3DX"

            # Configuración del navegador
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")  # Maximizar la ventana del navegador
            options.add_argument("--headless") 
            driver = webdriver.Chrome(options=options)

            # Hacer la solicitud GET a la URL
            driver.get(url)
            #time.sleep(3)  

            # Obtener el HTML de la página
            html = driver.page_source

            # Crear objeto BeautifulSoup para analizar el HTML
            soup = BeautifulSoup(html, 'html.parser')

            # Encontrar el elemento que contiene el valor de la divisa
            divisa_element = soup.find('fin-streamer', {'data-symbol': f'{normalized_currency_pair}=X'})

            # Extraer el valor del atributo "value"
            if divisa_element:
                valor = divisa_element['value']
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                # Guardar el valor en la base de datos o en algún otro lugar
                # Aquí podrías guardar el valor en tu base de datos si es necesario

                return Response({"timestamp": timestamp, "valor": valor})
            else:
                return Response({"message": "No se pudo encontrar el valor de la divisa"}, status=404)
        except Exception as e:
            return Response({"message": str(e)}, status=500)
        finally:
            # Cerrar el navegador
            driver.quit()

class ForexDataView(APIView):
    def get(self, request):
        # Parámetros de la solicitud
        symbol = request.query_params.get('divisas')
        function = 'TIME_SERIES_DAILY'  # Función para obtener datos diarios
        apikey = 'V01MN0FOTVCZ17D4'  # Reemplaza 'TU_CLAVE_API' con tu clave API de Alpha Vantage
        
        # Especificar el rango de fechas para obtener solo datos del año 2024
        start_date = '2024-01-01'
        end_date = '2024-12-31'
        #outputsize = 'full'  # Esto especifica que queremos obtener todos los datos disponibles

        # Construir la URL de la solicitud con el rango de fechas
        url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={apikey}&datatype=json&startdate={start_date}&enddate={end_date}'

        # Realizar la solicitud GET
        response = requests.get(url)

        # Procesar la respuesta
        if response.status_code == 200:
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Error al obtener los datos"}, status=response.status_code)


class SupabaseAuthView(APIView):
    def get(self, request):
        # Obtener datos de la solicitud
        email = request.query_params.get('email')
        password = request.query_params.get('password')

        if not email or not password:
            return Response({'error': 'Debes proporcionar un correo electrónico y una contraseña'}, status=400)

        # Configurar el cliente Supabase
        supabase_url = 'https://dcvauwnbzpxhdgggpzsg.supabase.co'
        supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRjdmF1d25ienB4aGRnZ2dwenNnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxMTg1OTUwNCwiZXhwIjoyMDI3NDM1NTA0fQ.AMi6GxQIuajsWeL_WQLSFFsXAfOufTwIpaN4gJxb8G4'
        client = create_client(supabase_url, supabase_key)

        # Autenticar el usuario
        auth_response = client.auth.sign_up(email, password)

        # Verificar el resultado de la autenticación
        if 'status' in auth_response and auth_response['status'] == 200:
            # Autenticación exitosa
            # Aquí puedes devolver el token de acceso u otra información relevante
            return Response({'token': auth_response['access_token']})
        else:
            # Autenticación fallida
            # Devolver un mensaje de error
            return Response({'error': auth_response.get('error', 'Error desconocido')}, status=400)
