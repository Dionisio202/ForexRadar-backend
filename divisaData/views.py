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
from .models import ForexData

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
            if(currency_pair==""):
                return Response({"message": "No se ha proporcionado un par de divisas"}, status=200)
            time.sleep(random.randint(4, 6))
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
            divisa_element2=soup.find('fin-streamer', class_='Fw(500) Pstart(8px) Fz(24px)')
            divisa_element3=soup.find('fin-streamer', {
                'class': 'Fw(500) Pstart(8px) Fz(24px)',
                'data-symbol': f'{normalized_currency_pair}=X',
                'data-field': 'regularMarketChangePercent'
            })
            if divisa_element:
                valor = divisa_element['value']
                valor = float(valor)
                valor_formatted = round(valor, 4)
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            if divisa_element2:
                valor2=divisa_element2['value']
                valor2=float(valor2)
                valor2=round(valor2,4)
            if divisa_element3:
                valor3=divisa_element3['value']
                valor3=float(valor3)*100
                valor3=round(valor3,4)
                if valor2<0:
                    color='red'
                else:
                    color='green'
                return Response({"timestamp": timestamp, "valor": valor_formatted,"cambio":valor2, "cambioPorcentaje":valor3 ,"color":color , "divisa": currency_pair})
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
        outputsize = 'full'  # Esto especifica que queremos obtener todos los datos disponibles

        # Construir la URL de la solicitud con el rango de fechas
        url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={apikey}&datatype=json&startdate={start_date}&enddate={end_date}&outputsize={outputsize}'

        # Realizar la solicitud GET
        response = requests.get(url)

        # Procesar la respuesta
        if response.status_code == 200:
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Error al obtener los datos"}, status=response.status_code)


class ForexGETDataView(APIView):
    def get(self, request):
        symbol = request.query_params.get('divisas')

        # Realizar la solicitud GET
        function = 'TIME_SERIES_WEEKLY'
        apikey = 'V01MN0FOTVCZ17D4'
        start_date = '2024-01-01'
        end_date = '2024-12-31'
        url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={apikey}&datatype=json&startdate={start_date}&enddate={end_date}'
        response = requests.get(url)

        # Procesar la respuesta
        if response.status_code == 200:
            data = response.json()
            
            
            # Determinar la frecuencia según la función utilizada
            if function == 'TIME_SERIES_DAILY':
                frequency = 'D'
                time_series_key = 'Time Series (Daily)'
            elif function == 'TIME_SERIES_WEEKLY':
                frequency = 'W'
                time_series_key = 'Weekly Time Series'
            elif function == 'TIME_SERIES_MONTHLY':
                frequency = 'M'
                time_series_key = 'Monthly Time Series'
            else:
                frequency = 'D'  # Frecuencia predeterminada
            time_series = data.get(time_series_key, {})
            # Guardar los datos en la base de datos
            for date_str, daily_data in time_series.items():
                ForexData.objects.update_or_create(
                    symbol=symbol,
                    date=date_str,
                    defaults={
                        'open_price': float(daily_data['1. open']),
                        'high_price': float(daily_data['2. high']),
                        'low_price': float(daily_data['3. low']),
                        'close_price': float(daily_data['4. close']),
                        'volume': int(daily_data['5. volume']),
                        'frequency': frequency,  # Asignar la frecuencia determinada
                    }
                )

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Error al obtener los datos"}, status=response.status_code)


class ForexSendDataView(APIView):
    def get(self, request):
        symbol = request.query_params.get('divisas')
        frequency = request.query_params.get('frequency', 'D')  # Obtener frecuencia de los query parameters

        # Validar la frecuencia permitida
        allowed_frequencies = ['D', 'W', 'M']
        if frequency not in allowed_frequencies:
            return Response({"error": "Frecuencia no válida"}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener datos de la base de datos filtrados por símbolo y frecuencia, ordenados por fecha
        data = ForexData.objects.filter(symbol=symbol, frequency=frequency).order_by('date')

        if not data.exists():
            return Response({"error": "No se encontraron datos para el símbolo y frecuencia proporcionados"}, status=status.HTTP_404_NOT_FOUND)

        # Crear la estructura del JSON de salida
        output_data = {
            "Meta Data": {
                "1. Information": f"{frequency.capitalize()} Prices (open, high, low, close) and Volumes",
                "2. Symbol": symbol,
                "3. Last Refreshed": data.last().date.strftime('%Y-%m-%d %H:%M:%S'),  # Última fecha de actualización
                "4. Output Size": "Compact",
                "5. Time Zone": "US/Eastern"
            },
            f"Time Series ({frequency.capitalize()})": {}
        }

        # Llenar los datos de series temporales en el JSON de salida
        for entry in data:
            output_data[f"Time Series ({frequency.capitalize()})"][entry.date.strftime('%Y-%m-%d')] = {
                "1. open": str(entry.open_price),
                "2. high": str(entry.high_price),
                "3. low": str(entry.low_price),
                "4. close": str(entry.close_price),
                "5. volume": str(entry.volume)
            }

        return Response(output_data, status=status.HTTP_200_OK)
    
class DivisasInformation(APIView):
    def get(self, request):
        try:
            # Configurar el cliente Supabase
            supabase_url = 'https://dcvauwnbzpxhdgggpzsg.supabase.co'
            supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRjdmF1d25ienB4aGRnZ2dwenNnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxMTg1OTUwNCwiZXhwIjoyMDI3NDM1NTA0fQ.AMi6GxQIuajsWeL_WQLSFFsXAfOufTwIpaN4gJxb8G4'
            client = create_client(supabase_url, supabase_key)

            # Realizar consulta a la tabla "divisas"
            table_name = 'divisas'
            response = client.from_(table_name).select('*').execute()

            # Verificar si la consulta fue exitosa
            if response['status_code'] == 200:
                # Obtener los datos de la respuesta
                data = response['data']
                return Response(data)
            else:
                # La consulta falló
                return Response({'error': 'No se pudo obtener datos de la tabla "divisas"'}, status=500)

        except Exception as e:
            # Manejar cualquier excepción que ocurra durante la consulta
            return Response({'error': str(e)}, status=500)
        
class InsertarDivisasUser(APIView):
    def post(self, request):
        try:
            # Obtener datos de la solicitud POST
            divisa_id = request.data.get('divisa_id')
            user_profile_id = request.data.get('user_profile_id')

            if not divisa_id or not user_profile_id:
                return Response({'error': 'Se requiere divisa_id y user_profile_id para la inserción'}, status=400)

            # Configurar el cliente Supabase
            supabase_url = 'https://dcvauwnbzpxhdgggpzsg.supabase.co'
            supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRjdmF1d25ienB4aGRnZ2dwenNnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxMTg1OTUwNCwiZXhwIjoyMDI3NDM1NTA0fQ.AMi6GxQIuajsWeL_WQLSFFsXAfOufTwIpaN4gJxb8G4'
            client = create_client(supabase_url, supabase_key)

            # Realizar inserción en la tabla "user_divisas"
            table_name = 'user_divisas'
            response = client.from_(table_name).insert([{
                'divisa_id': divisa_id,
                'user_profile_id': user_profile_id
            }]).execute()

            # Verificar si la inserción fue exitosa
            if response['status_code'] == 201:
                # Obtener el ID de la nueva entrada insertada
                inserted_id = response['data'][0]['id']

                # Consultar los detalles de la divisa asociada al divisa_id
                table_divisas = 'divisas'
                divisa_response = client.from_(table_divisas).select('*').eq('id', divisa_id).single().execute()

                if divisa_response['status_code'] == 200:
                    # Obtener los datos de la divisa asociada
                    divisa_data = divisa_response['data']
                    return Response(divisa_data)
                else:
                    return Response({'error': response}, status=500)
            else:
                # La inserción falló
                return Response({'error': response}, status=500)

        except Exception as e:
            # Manejar cualquier excepción que ocurra durante la inserción o consulta
            return Response({'error': str(e)}, status=500)

class DivisasOwn(APIView):
    def get(self, request):
        try:
            # Configurar el cliente Supabase
            supabase_url = 'https://dcvauwnbzpxhdgggpzsg.supabase.co'
            supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRjdmF1d25ienB4aGRnZ2dwenNnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxMTg1OTUwNCwiZXhwIjoyMDI3NDM1NTA0fQ.AMi6GxQIuajsWeL_WQLSFFsXAfOufTwIpaN4gJxb8G4'
            client = create_client(supabase_url, supabase_key)
            
            user_id = request.query_params.get('user')
            
            # Realizar consulta a la tabla "user_divisas" filtrando por user_id
            table_name = 'user_divisas'
            response = client.from_(table_name).select('*').eq('user_profile_id', user_id).execute()

            # Verificar si la consulta fue exitosa
            if response['status_code'] == 200:
                # Obtener los datos de la respuesta
                data = response['data']
                
                # Extraer solo los valores de divisa_id como cadenas (strings)
                divisa_ids = [str(item['divisa_id']) for item in data]
                
                # Inicializar una lista para almacenar todos los datos de las divisas
                all_divisas_data = []
                
                # Iterar sobre cada divisa_id y obtener sus datos completos
                for divisa_id in divisa_ids:
                    # Realizar consulta para obtener los datos de la divisa con este divisa_id
                    table_divisas = 'divisas'
                    divisa_response = client.from_(table_divisas).select('*').eq('id', divisa_id).execute()
                    
                    # Verificar si la consulta fue exitosa y agregar los datos a la lista
                    if divisa_response['status_code'] == 200:
                        all_divisas_data.append(divisa_response['data'][0])  # Asumiendo que solo se espera un resultado
                    else:
                        # Manejar el error si la consulta de la divisa falló
                        return Response({'error': f'No se pudo obtener datos de la divisa con ID {divisa_id}'}, status=500)
                
                # Devolver la lista de todos los datos de las divisas encontradas
                return Response(all_divisas_data)
            
            else:
                # La consulta inicial falló
                return Response({'error': f'No se pudo obtener datos de la tabla "user_divisas" para el usuario {user_id}'}, status=500)

        except Exception as e:
            # Manejar cualquier excepción que ocurra durante la consulta
            return Response({'error': str(e)}, status=500)


class divisasDeleteInformation(APIView):
    def delete_divisa(self, user_profile_id, divisa_id):
        try:
            # Configurar el cliente Supabase
            supabase_url = 'https://dcvauwnbzpxhdgggpzsg.supabase.co'
            supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRjdmF1d25ienB4aGRnZ2dwenNnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxMTg1OTUwNCwiZXhwIjoyMDI3NDM1NTA0fQ.AMi6GxQIuajsWeL_WQLSFFsXAfOufTwIpaN4gJxb8G4'
            client = create_client(supabase_url, supabase_key)

            # Realizar la eliminación en la tabla "user_divisas"
            table_name = 'user_divisas'
            response = client.from_(table_name).delete().eq('user_profile_id', user_profile_id).eq('divisa_id', divisa_id).execute()

            # Verificar si la eliminación fue exitosa
            if 'status_code' in response and response['status_code'] == 200:
                return True  # Indica que la eliminación fue exitosa
            else:
                return False  # Indica que la eliminación falló

        except Exception as e:
            # Manejar cualquier excepción que ocurra durante la eliminación
            print(f'Error al eliminar divisa: {str(e)}')
            return False

    def get(self, request):
        try:
            user_profile_id = request.query_params.get('user')
            divisa_id = request.query_params.get('divisa')

            if not user_profile_id or not divisa_id:
                return Response({'error': 'Se requiere user_profile_id y divisa_id para eliminar la divisa'}, status=400)

            # Intentar eliminar la divisa
            if self.delete_divisa(user_profile_id, divisa_id):
                return Response({'message': 'Divisa eliminada exitosamente'}, status=200)
            else:
                return Response({'message': 'Divisa eliminada exitosamente'}, status=200)

        except Exception as e:
            # Manejar cualquier excepción que ocurra durante la solicitud
            return Response({'error': str(e)}, status=500)

##Test 
class ForexGETDataSelectView(APIView):
    def get(self, request):
        symbol = request.query_params.get('divisas')
        frequency = request.query_params.get('frequency', 'D')  # Obtener frecuencia de los query parameters
        start_date = request.query_params.get('start_date', '2020-01-01')
        end_date = request.query_params.get('end_date', '2024-04-19')
        # Validar la frecuencia permitida
        allowed_frequencies = ['D', 'W', 'M']
        if frequency not in allowed_frequencies:
            return Response({"error": "Frecuencia no válida"}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener datos de la base de datos filtrados por símbolo y frecuencia, ordenados por fecha
        data = ForexData.objects.filter(symbol=symbol, frequency=frequency).order_by('date')

        if not data.exists():
            # Si no se encuentran datos en la base de datos, obtener datos de la API y almacenarlos
            if frequency == 'D':
                    time_series_Api = 'Daily'
            elif frequency == 'W':
                    time_series_Api = 'Weekly'
            elif frequency == 'M':
                    time_series_Api = 'Monthly'
            else:
                    time_series_Api = None
            function = f'TIME_SERIES_{time_series_Api.upper()}'
            apikey = 'V01MN0FOTVCZ17D4'
            outputsize = 'full'
            url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={apikey}&datatype=json&outputsize={outputsize}'
            response = requests.get(url)

            # Procesar la respuesta de la API
            if response.status_code == 200:
                api_data = response.json()

                # Determinar la clave de la serie temporal según la frecuencia utilizada
                if frequency == 'D':
                    time_series_key = 'Time Series (Daily)'
                elif frequency == 'W':
                    time_series_key = 'Weekly Time Series'
                elif frequency == 'M':
                    time_series_key = 'Monthly Time Series'
                else:
                    time_series_key = None

                if time_series_key:
                    time_series = api_data.get(time_series_key, {})

                    # Guardar los datos en la base de datos
                    for date_str, daily_data in time_series.items():
                        ForexData.objects.update_or_create(
                            symbol=symbol,
                            date=date_str,
                            defaults={
                                'open_price': float(daily_data['1. open']),
                                'high_price': float(daily_data['2. high']),
                                'low_price': float(daily_data['3. low']),
                                'close_price': float(daily_data['4. close']),
                                'volume': int(daily_data['5. volume']),
                                'frequency': frequency,  # Asignar la frecuencia determinada
                            }
                        )

                    # Después de almacenar los datos, volver a recuperarlos de la base de datos
        data = ForexData.objects.filter(symbol=symbol, frequency=frequency,date__range=(start_date, end_date)).order_by('date')
        if not data.exists():
            return Response({"error": "No se encontraron datos para el símbolo y frecuencia proporcionados"}, status=status.HTTP_404_NOT_FOUND)
        # Crear la estructura del JSON de salida
        output_data = {
            "Meta Data": {
                "1. Information": f"{frequency.capitalize()} Prices (open, high, low, close) and Volumes",
                "2. Symbol": symbol,
                "3. Last Refreshed": data.last().date.strftime('%Y-%m-%d %H:%M:%S'),  # Última fecha de actualización
                "4. Output Size": "Compact",
                "5. Time Zone": "US/Eastern"
            },
            "Time Series": {}
        }

        # Llenar los datos de series temporales en el JSON de salida
        for entry in data:
            output_data["Time Series"][entry.date.strftime('%Y-%m-%d')] = {
                "1. open": str(entry.open_price),
                "2. high": str(entry.high_price),
                "3. low": str(entry.low_price),
                "4. close": str(entry.close_price),
                "5. volume": str(entry.volume)
            }

        return Response(output_data, status=status.HTTP_200_OK)