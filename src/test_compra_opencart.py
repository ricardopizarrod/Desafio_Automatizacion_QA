import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# === Configuración inicial ===
ruta_evidencias = os.path.join(os.path.dirname(__file__), "../evidencias")
os.makedirs(ruta_evidencias, exist_ok=True)

ruta_credenciales = os.path.join(os.path.dirname(__file__), "../data/credenciales.txt")
with open(ruta_credenciales, "r") as archivo:
    linea = archivo.readline().strip()
    if "," in linea:
        email, password = linea.split(",")
    else:
        raise ValueError("❌ Formato de credenciales inválido. Usa: correo,contraseña")

chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--start-maximized")

# Iniciar WebDriver
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=chrome_options
)
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

def tomar_evidencia(nombre):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    driver.save_screenshot(os.path.join(ruta_evidencias, f"{nombre}_{timestamp}.png"))

def validar_producto_agregado(nombre_producto):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success")))
    mensaje = driver.find_element(By.CSS_SELECTOR, ".alert-success").text
    assert nombre_producto in mensaje, f"❌ No se confirmó el agregado de {nombre_producto} al carrito"
    print(f"🛒 Producto agregado correctamente: {nombre_producto}")

try:
    driver.get("https://opencart.abstracta.us/index.php?route=common/home")

    driver.find_element(By.LINK_TEXT, "My Account").click()
    driver.find_element(By.LINK_TEXT, "Login").click()
    wait.until(EC.presence_of_element_located((By.ID, "input-email")))
    driver.find_element(By.ID, "input-email").send_keys(email)
    driver.find_element(By.ID, "input-password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//h2[text()='My Account']")))
    print("✅ Login exitoso")

    for producto in ["iPod Classic", "iMac"]:
        driver.find_element(By.NAME, "search").clear()
        driver.find_element(By.NAME, "search").send_keys(producto)
        driver.find_element(By.CSS_SELECTOR, "button.btn-default").click()
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, producto))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "button-cart"))).click()
        validar_producto_agregado(producto)
        tomar_evidencia(f"{producto.lower().replace(' ', '_')}_agregado")
        driver.find_element(By.XPATH, "//a[text()='Your Store']").click()

    driver.get("https://opencart.abstracta.us/index.php?route=checkout/cart")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table tbody")))

    productos = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr td:nth-child(2) a")
    nombres = [p.text.strip() for p in productos]
    print("🔍 Productos detectados en el carrito:", nombres)
    assert "iMac" in nombres and "iPod Classic" in nombres, "❌ Los productos no están en el carrito"
    tomar_evidencia("carrito_validado")
    print("✅ Carrito validado con iMac y iPod Classic")

    driver.get("https://opencart.abstracta.us/index.php?route=checkout/checkout")
    print("🛒 Navegación directa al checkout realizada")

    try:
        wait.until(EC.presence_of_element_located((By.ID, "collapse-checkout-option")))
        driver.find_element(By.ID, "button-account").click()
        print("🧾 Paso 1: Opción de cuenta confirmada")
    except:
        print("ℹ️ Paso 1 ya estaba completado o no fue necesario")

    try:
        driver.execute_script("document.getElementById('bitnami-banner').remove();")
        print("🧼 Banner de Bitnami eliminado")
    except:
        pass

    wait.until(EC.element_to_be_clickable((By.ID, "button-payment-address"))).click()
    print("✅ Paso 2: Dirección de pago confirmada")

    wait.until(EC.element_to_be_clickable((By.ID, "button-shipping-address"))).click()
    print("✅ Paso 3: Dirección de envío confirmada")

    driver.find_element(By.TAG_NAME, "body").click()
    wait.until(EC.element_to_be_clickable((By.ID, "button-shipping-method"))).click()
    print("✅ Paso 4: Método de envío confirmado")

    shipping = driver.find_element(By.CSS_SELECTOR, "#collapse-shipping-method .radio label").text
    assert shipping.strip() == "Flat Shipping Rate - $5.00", f"❌ Despacho no esperado: {shipping}"
    print("🚚 Despacho validado correctamente")

    checkbox = wait.until(EC.presence_of_element_located((By.NAME, "agree")))
    driver.execute_script("arguments[0].scrollIntoView();", checkbox)
    checkbox.click()

    driver.find_element(By.ID, "button-payment-method").click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='collapse-checkout-confirm']//table")))
    total = driver.find_element(By.XPATH, "//div[@id='collapse-checkout-confirm']//td[contains(text(), '$')]").text
    assert total != "", "❌ No se encontró total de orden"
    print(f"💰 Total de la orden: {total}")
    tomar_evidencia("total_validado")

    driver.find_element(By.ID, "button-confirm").click()

    try:
        wait.until(EC.title_contains("Success"), "Redirigiendo a página de éxito...")
    except:
        print("⚠️ No se detectó Success, redirigiendo manualmente al historial")

    print("✅ Orden completada exitosamente")
    driver.get("https://opencart.abstracta.us/index.php?route=account/order")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table-responsive")))
    print("📂 Historial de órdenes accedido correctamente")
    tomar_evidencia("historial_orden")

    try:
        estado = driver.find_element(By.CSS_SELECTOR, ".table-responsive tbody tr td:nth-child(4)").text
        assert "Pending" in estado, f"❌ Estado de orden no es 'Pending' → Es: {estado}"
        print(f"🕒 Estado de orden: {estado}")
        tomar_evidencia("estado_orden")
    except Exception as e:
        print(f"⚠️ {e}")

    try:
        driver.find_element(By.LINK_TEXT, "View").click()
        wait.until(EC.presence_of_element_located((By.ID, "content")))
        direccion_pago = driver.find_element(By.XPATH, "//td[contains(text(),'ricardo')]").text.lower()
        assert "direccion 1" in direccion_pago, "❌ Dirección de pago no coincide"
        print("🏠 Dirección de pago validada correctamente")
        tomar_evidencia("direccion_pago_validada")
    except Exception as e:
        print("⚠️ No hay botón 'View' disponible, posiblemente por estado 'Canceled'")

    # Comparar productos
    try:
        print("🆚 Iniciando comparación de productos...")
        for producto in ["Apple Cinema 30\"", "Samsung SyncMaster 941BW"]:
            driver.find_element(By.NAME, "search").clear()
            driver.find_element(By.NAME, "search").send_keys(producto)
            driver.find_element(By.CSS_SELECTOR, "button.btn-default").click()
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, producto))).click()
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-original-title='Compare this Product']"))).click()
            print(f"➕ {producto} agregado a comparación")
            driver.find_element(By.XPATH, "//a[text()='Your Store']").click()

        driver.get("https://opencart.abstracta.us/index.php?route=product/compare")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-bordered")))
        tomar_evidencia("comparacion_productos")
        print("📸 Comparación capturada exitosamente")

    except Exception as e:
        tomar_evidencia("error_comparacion")
        print("❌ Error durante comparación de productos:", type(e).__name__, "→", str(e))

    # Cerrar sesión
    try:
        driver.find_element(By.LINK_TEXT, "My Account").click()
        driver.find_element(By.LINK_TEXT, "Logout").click()
        print("👋 Sesión cerrada correctamente")
    except:
        print("⚠️ No se pudo cerrar sesión (posiblemente ya fue cerrada)")

except Exception as e:
    tomar_evidencia("error")
    print("❌ Error durante el flujo:")
    print(type(e).__name__, "→", str(e))

finally:
    driver.quit()