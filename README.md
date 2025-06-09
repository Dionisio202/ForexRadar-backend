# 📈 ForexRadar Backend

<div align="center">

![Django](https://img.shields.io/badge/Django-4.2.22-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.14-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.0-43B02A?style=for-the-badge&logo=selenium&logoColor=white)

**API REST robusta para análisis de mercados Forex con scraping dinámico y datos históricos**

[🚀 Demo](#-vista-previa) • [📖 Documentación](#-funcionalidades-principales) • [⚡ Instalación](#️-instalación-rápida) • [🔗 Frontend](https://github.com/Dionisio202/ForexRadar-frontEnd)

</div>

---

## 🎯 ¿Qué es ForexRadar?

**ForexRadar** es una potente aplicación backend desarrollada con **Django REST Framework** que combina scraping inteligente y APIs para proporcionar datos completos del mercado Forex. Diseñada para alimentar dashboards analíticos y aplicaciones de trading con información precisa y actualizada.

### ✨ Características destacadas

- 🔄 **Datos en tiempo real** con precios actuales y variaciones
- 📊 **Scraping inteligente** de Yahoo Finance con Selenium
- 💾 **Base de datos histórica** desde 2005 hasta la actualidad
- 🎛️ **Panel de administración** completo y personalizable
- 👥 **Gestión de usuarios** con divisas favoritas
- 📈 **Múltiples frecuencias** (diario, semanal, mensual)

---

## 🖼️ Vista previa

<table>
<tr>
<td width="50%">

### 🎛️ Panel de Administración
![Dashboard general](./docs/images/track6.png)

</td>
<td width="50%">

### 🔍 Filtros Avanzados
![Filtros de frecuencia y símbolo](./docs/images/track7.png)

</td>
</tr>
<tr>
<td width="50%">

### 📋 Resultados de Scraping
![Scraping de Yahoo Finance](./docs/images/4767cf8d-c2b7-4e6e-a8eb-79b86c709e6c.png)

</td>
<td width="50%">

### 🌐 Yahoo Finance Base
![Yahoo Finance ejemplo](./docs/images/51151a87-3543-4693-8f2a-d7f13dd8cc84.png)

</td>
</tr>
</table>

---

## 🚀 Funcionalidades principales

<table>
<tr>
<td width="50%">

### 📊 **Datos del Mercado**
- ✅ Precios en tiempo real
- ✅ Datos históricos completos
- ✅ Múltiples pares de divisas
- ✅ Frecuencias personalizables

</td>
<td width="50%">

### 🛠️ **Gestión y Admin**
- ✅ Panel de administración Django
- ✅ Filtros avanzados por símbolo/fecha
- ✅ Gestión de usuarios autenticados
- ✅ Configuración de divisas favoritas

</td>
</tr>
</table>

---

## ⚙️ Stack Tecnológico

### 🔧 Backend Core
```
Django 4.2.22          # Framework web robusto
Django REST Framework  # API REST potente
SQLite3               # Base de datos (desarrollo)
```

### 🕷️ Scraping & APIs
```
Selenium              # Automatización web
BeautifulSoup         # Parsing HTML
Alphavantage API      # Datos alternativos
```

### 🎨 Frontend (Repositorio separado)
```
React                 # Interface de usuario
ApexCharts           # Gráficos candlestick
```

> 🔗 **Frontend Repository:** [ForexRadar-frontEnd](https://github.com/Dionisio202/ForexRadar-frontEnd)

---

## 🗄️ Estructura de Datos

### 📈 Modelo `ForexData`
```python
class ForexData(models.Model):
    symbol      # Par de divisas (EURUSD, AUDUSD, etc.)
    date        # Fecha del registro
    open_price  # Precio de apertura
    high_price  # Precio máximo
    low_price   # Precio mínimo
    close_price # Precio de cierre
    volume      # Volumen negociado
    frequency   # Frecuencia (D, W, M)
```

### 💱 Modelo `Divisa`
```python
class Divisa(models.Model):
    nombre      # Nombre descriptivo
    simbolo     # Código de la divisa
    imagen1     # URL imagen principal
    imagen2     # URL imagen secundaria
```

### 👤 Modelo `UserDivisa`
```python
# Relación Usuario ↔ Divisas Favoritas
class UserDivisa(models.Model):
    user        # Usuario autenticado
    divisa      # Divisa favorita
```

---

## 🎯 Cobertura de Datos

<div align="center">

| 📊 **Métrica** | 📈 **Valor** |
|:---:|:---:|
| **Símbolos Disponibles** | `AUDCAD, AUDUSD, CHFUSD, EURGBP, EURUSD, GBPUSD, NZDJPY, USDCAD, USDJPY` |
| **Rango Temporal** | `2005-02-21` hasta `2024-04-26` |
| **Frecuencias** | `Diario (D)` • `Semanal (W)` • `Mensual (M)` |
| **Total de Registros** | `190,000+` datos históricos |

</div>

---

## 🔍 Sistema de Scraping

### 🎯 Endpoint Principal: `/divisa/tableData/`

```http
GET /divisa/tableData/?divisas=EURUSD%3DX&period1=2024-01-01&period2=2024-06-01&frequency=1d
```

### 🔄 Proceso de Scraping

1. **🏗️ Construcción de URL** → Parámetros de fecha y frecuencia
2. **🚀 Selenium Headless** → Navegación automatizada
3. **📜 Scroll Dinámico** → Carga completa de datos
4. **🧹 BeautifulSoup** → Parsing y extracción de HTML
5. **📤 JSON Response** → Datos estructurados

> ⚠️ **Nota:** El scraping depende de la estructura actual de Yahoo Finance

---

## 📡 API Endpoints

### 🔴 Datos en Tiempo Real
```http
GET /divisa/currentData/?divisas=EURUSD
```

### 📊 Datos Históricos (Scraping)
```http
GET /divisa/tableData/?divisas=EURUSD%3DX&period1=2024-01-01&period2=2024-06-01&frequency=1d
```

### 💾 Datos Almacenados
```http
GET /divisa/dataprueba/?divisas=EURUSD&start_date=2023-01-01&end_date=2023-06-01&frequency=W
```

### 👤 Gestión de Usuarios
```http
POST /user/register/         # Registro
POST /user/login/           # Autenticación
GET  /user/getProfile/      # Perfil de usuario
PUT  /user/updateProfileName/  # Actualizar nombre
PUT  /user/changePassword/  # Cambiar contraseña
```

### 💱 Divisas de Usuario
```http
GET  /divisa/obtenerDivisas/?user=2        # Obtener favoritas
POST /divisa/insertarDivisaInformation/    # Agregar favorita
DELETE /divisa/eliminarDivisas/            # Eliminar favorita
```

---

## 🛠️ Instalación Rápida

### 📋 Prerrequisitos
- **Python** ≥ 3.9 (recomendado 3.11+)
- **Google Chrome** instalado
- **Git** para clonado

### 🚀 Setup en 5 pasos

```bash
# 1️⃣ Clonar repositorio
git clone https://github.com/Dionisio202/ForexRadar-backend.git
cd ForexRadar-backend

# 2️⃣ Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3️⃣ Instalar dependencias
pip install -r requirements.txt

# 4️⃣ Configurar base de datos
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 5️⃣ Ejecutar servidor
python manage.py runserver
```

### 🎯 Acceso Rápido
- **API Base:** `http://127.0.0.1:8000/`
- **Admin Panel:** `http://127.0.0.1:8000/admin/`
- **API Docs:** `http://127.0.0.1:8000/api/docs/`

---

## 🚧 Consideraciones Importantes

### ⚠️ Limitaciones Técnicas
- **Dependencia de Yahoo Finance:** Cambios en su estructura pueden afectar el scraping
- **Rate Limiting:** Se recomienda uso controlado del scraping
- **Chrome Driver:** Debe estar correctamente instalado

### 🔒 Seguridad
- Autenticación JWT implementada
- Validación de entrada en todos los endpoints
- Protección CSRF activada

---

## 🛣️ Roadmap Futuro

### 🎯 Próximas Características

- [ ] **🤖 Automatización con Celery** → Scraping periódico
- [ ] **📊 Dashboard React Completo** → Gráficos candlestick interactivos
- [ ] **🔔 Sistema de Alertas** → Notificaciones de precio
- [ ] **🗃️ Data Warehouse** → Escalabilidad para producción
- [ ] **📈 Más Fuentes de Datos** → Investing.com, APIs premium
- [ ] **🐳 Docker Support** → Containerización completa

---

## 🤝 Contribución

¿Quieres contribuir? ¡Genial! 

1. **Fork** el repositorio
2. **Crea** una branch para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la branch (`git push origin feature/AmazingFeature`)
5. **Abre** un Pull Request

---



## 🔗 Enlaces Relacionados

- 🎨 **Frontend Repository:** [ForexRadar-frontEnd](https://github.com/Dionisio202/ForexRadar-frontEnd)
- 📚 **Django Documentation:** [docs.djangoproject.com](https://docs.djangoproject.com/)
- 🕷️ **Selenium Docs:** [selenium-python.readthedocs.io](https://selenium-python.readthedocs.io/)

---

<div align="center">

**⭐ Si te gusta este proyecto, considera darle una estrella en GitHub ⭐**

*Desarrollado con ❤️ por [Dionisio202](https://github.com/Dionisio202)*

</div>