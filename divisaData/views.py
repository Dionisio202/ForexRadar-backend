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
class DivisaAPIView(APIView):
    def get(self, request, format=None):
        url = 'https://es.investing.com/currencies/eur-usd-historical-data'
        response = requests.get(url)
        time.sleep(random.uniform(2, 3))
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            div_valor = soup.find('div', {'class': 'text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]', 'data-test': 'instrument-price-last'})
            if div_valor:
                valor = div_valor.text.strip()
                return Response({'valor_divisa': valor})
            else:
                return Response({'error': 'No se encontró el valor de la divisa'}, status=500)
        else:
            return Response({'error': 'No se pudo obtener la página'}, status=response.status_code)

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