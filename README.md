# Desafío Automatización QA - Previred

## Autor
- **Nombre completo:** Ricardo Pizarro
- **Correo electrónico:** ricardopizarro.d@gmail.com

## Descripción del proyecto
Este proyecto automatiza el proceso de compra en el sitio de pruebas de OpenCart (https://opencart.abstracta.us), cumpliendo con todos los requisitos y validaciones solicitadas por Previred. La solución está desarrollada en Python utilizando Selenium WebDriver.

---

## Pre-requisitos
- Python 3.9 o superior
- Google Chrome instalado
- pip instalado

---

## Instalación y configuración
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/ricardopizarro1990/Desafio_Automatizacion_QA.git
   cd Desafio_Automatizacion_QA
   ```

2. Crear entorno virtual:
   ```bash
   python -m venv env
   source env/bin/activate  # En Windows: env\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Crear archivo de credenciales:
   Dentro de la carpeta `data/` crear un archivo llamado `credenciales.txt` con el siguiente formato:
   ```txt
   correo@ejemplo.com,contraseña123
   ```

---

## Ejecución
```bash
python src/test_compra_opencart.py
```

Las capturas de pantalla generadas se guardarán en la carpeta `/evidencias`.

---

## Flujo automatizado
- Login con credenciales externas
- Búsqueda y agregado de productos al carrito:
  - iPod Classic
  - iMac
- Validación del contenido del carrito
- Proceso completo de checkout:
  - Dirección de pago
  - Método de envío
  - Validación de despacho y total
- Confirmación de orden
- Acceso a historial de órdenes y validación de estado ("Pending")
- Validación de dirección de pago
- Cierre de sesión

### Validaciones solicitadas
- ✅ Evidencia de productos agregados
- ✅ Validación del carrito
- ✅ Captura paso a paso del checkout
- ✅ Validación de despacho: `Flat Shipping Rate - $5.00`
- ✅ Evidencia de orden completada y total
- ✅ Historial de órdenes con estado `Pending` (cuando aplica)
- ✅ Validación de dirección de pago
- ✅ Cierre de sesión

---

## Extra: Comparación de productos
- Se realiza la comparación entre:
  - Apple Cinema 30"
  - Samsung SyncMaster 941BW
- Se toma evidencia del cuadro comparativo

---

## Estructura del proyecto
```bash
Desafio_Automatizacion_QA/
├── data/
│   └── credenciales.txt
├── evidencias/
│   └── *.png
├── src/
│   └── test_compra_opencart.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Observaciones
- El sitio de pruebas de OpenCart a veces muestra fallas inesperadas como órdenes "Canceled" o ausencia de botón `View`. Se manejan estas situaciones para evitar fallos críticos.
- Se incluye manejo de errores y captura de evidencias para seguimiento.

---

© Ricardo Pizarro - 2025


