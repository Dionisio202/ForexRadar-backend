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
            # URL de la página con los datos históricos de la divisa
            url = 'https://au.finance.yahoo.com/quote/EURUSD%3DX/history'

            # Encabezados con el agente de usuario
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }

            # Realizar la solicitud GET a la URL con los encabezados
            response = requests.get(url, headers=headers)

            # Verificar si la solicitud fue exitosa (código de estado 200)
            if response.status_code == 200:
                # Crear objeto BeautifulSoup para analizar el HTML
                soup = BeautifulSoup(response.text, 'html.parser')

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
                        data.append(row_data)

                    # Retornar los datos extraídos como respuesta
                    return Response(data)
                else:
                    return Response({'error': 'No se encontró la tabla de datos históricos'}, status=500)
            else:
                return Response({'error': 'No se pudo obtener la página'}, status=response.status_code)
        except Exception as e:
            # Manejar cualquier error y retornar una respuesta de error
            return Response({'error': str(e)}, status=500)