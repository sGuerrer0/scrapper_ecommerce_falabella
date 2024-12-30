from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

option = webdriver.ChromeOptions()
option.add_argument('--disable-extensions')
option.add_argument("--start-maximized")
option.add_experimental_option("detach", True)

driver = webdriver.Chrome(options = option)

driver.get('https://www.falabella.com/falabella-cl')

def get_productos(elementos_hijos):
    time.sleep(2)
    for elem in elementos_hijos:

        marca_producto = elem.find_element(By.XPATH, f'.//div[2]/div[1]/div/b').text
        nombre_producto = elem.find_element(By.XPATH, f'.//div[2]/div[1]/b').text

        # Cuando un producto no tiene descuento cambia el path del elemento, por ende parchamos utilizando try except
        precio_dcto = "Sin dcto."
        dcto = "Sin dcto."

        try: 
            precio_dcto = elem.find_element(By.XPATH, f'.//div[3]/div[1]/ol/li[1]/div/span').text
            dcto = elem.find_element(By.XPATH, f'.//div[3]/div[1]/ol/li[1]/div/div/span').text
            precio_original = elem.find_element(By.XPATH, f'.//div[3]/div[1]/ol/li[2]/div/span').text
        except NoSuchElementException:
            precio_original = elem.find_element(By.XPATH, f'.//div[3]/div[1]/ol/li/div/span').text #Precio original sin dcto asociado

        #print(f"Marca: {marca_producto} , Producto: {nombre_producto} , Precio original: {precio_original},  Dcto: {dcto}, Precio_dcto: {precio_dcto}")

        productos.append({
            "Marca" : marca_producto,
            "Producto" : nombre_producto,
            "Precio_Original" : precio_original, 
            "Descuento" : dcto, 
            "Precio_Dcto" : precio_dcto
        })

    return productos


productos = []

# Ingresamos nombre del producto que deseamos buscar
product = "Televisor"

time.sleep(3)
try:
    # Cerramos modal en caso de que aparezca
    print("Cerramos modal")
    driver.find_element(By.XPATH,'//*[@id="cmr-modal"]/div/div[1]').click()
except:
    pass

time.sleep(3)

try:
    # Ingresamos nombre del producto y buscamos
    search_bar = driver.find_element(By.ID, 'testId-SearchBar-Input').send_keys(product)
    btn_search = driver.find_element(By.CLASS_NAME, 'SearchBar-module_searchBtnIcon__2L2s0').click()

    time.sleep(3)
    # Verificamos que el botón o flecha de "Siguiente página" se encuentre habilitado.
    boton_siguiente = driver.find_element(By.ID, 'testId-pagination-top-arrow-right')
    pagina = 1

    # Dejamos en un loop hasta que el botón siguiente no se encuentre en "None", esto quiere decir hasta que este habilitado
    while boton_siguiente.get_attribute('disabled') is None:
        try:
            # Accedemos a todos los resultados encontramos del producto buscado
            resultado_producto = driver.find_element(By.ID, 'testId-searchResults-products')
            elementos_hijos = resultado_producto.find_elements(By.XPATH, './/div//a') # selecciona todos los elementos hijos
            obtain_products = get_productos(elementos_hijos)
            boton_siguiente.click()
            print(f"Esperando numeración página: {pagina}")
            pagina +=1
            time.sleep(3)
        except:
            pass
        
    df = pd.DataFrame(obtain_products)
    print(df)
    df.to_csv("productos.csv", encoding = 'utf-8-sig', index=False)

except:
    pass
