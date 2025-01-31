from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import re  # Para extrair o número da string a onde tem o segundo preço se necessário

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://www.amazon.com.br/ref=nav_logo")
time.sleep(2)

search_box = driver.find_element(By.ID, "twotabsearchtextbox")
search_box.send_keys("livros sobre automacao")
search_box.send_keys(Keys.RETURN)
time.sleep(3)

produtos = []

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-component-type='s-search-result']"))
    )
except:
    print("Resultados da pesquisa não carregados.")
    driver.quit()
    exit()

resultados = driver.find_elements(By.CSS_SELECTOR, "div[data-component-type='s-search-result']")

for resultado in resultados[:10]: 
    try:
        titulo = resultado.find_element(By.CSS_SELECTOR, "h2.a-size-base-plus span").text
        
        try:
            autor = resultado.find_element(By.CSS_SELECTOR, "div.a-row.a-size-base.a-color-secondary span.a-size-base + span.a-size-base").text
        except:
            autor = "N/A"
        
        # Verifica o preço principal (Kindle ou físico)
        try:
            preco = resultado.find_element(By.CSS_SELECTOR, "span.a-price span.a-offscreen").get_attribute("innerHTML").replace("&nbsp;", " ").strip()
            preco = "Gratuito" if float(preco.replace('R$', '').replace(',', '.')) == 0 else preco
        except:
            preco = "N/A"
        
        # Verifica se há um preço secundário (versão física)
        if preco == "Gratuito":
            try:
                # Captura o texto do preço secundário
                preco_secundario = resultado.find_element(By.CSS_SELECTOR, "div[data-cy='secondary-offer-recipe'] span.a-color-secondary").text
                preco_match = re.search(r"R\$\s*(\d+,\d+)", preco_secundario)
                if preco_match:
                    preco = f"R$ {preco_match.group(1)}"  
                else:
                    preco = "N/A"  
            except:
                pass  
        
        try:
            nota = resultado.find_element(By.CSS_SELECTOR, "span.a-icon-alt").get_attribute("innerHTML").split()[0]
        except:
            nota = "Nenhuma nota"
        
        try:
            avaliacoes = resultado.find_element(By.CSS_SELECTOR, "span.a-size-base.s-underline-text").text.replace(",", "")
        except:
            avaliacoes = "N/A"
        
        produtos.append({
            "Titulo": titulo,
            "Autor": autor,
            "Preço": preco,
            "Nota": nota,
            "Avaliações": avaliacoes
        })

    except Exception as e:
        print(f"Erro ao coletar dados de um produto: {e}")

driver.quit()

if produtos:  # Verifica se há dados coletados
    df = pd.DataFrame(produtos)
    
    # Ordenar primeiro por título e garantir IDs sequenciais
    df = df.sort_values(by="Titulo", ascending=True).reset_index(drop=True)
    df.insert(0, 'ID', range(1, len(df) + 1))

    df.to_excel("livros_automacao.xlsx", index=False)
    print("Dados coletados e salvos com sucesso!")
else:
    print("Nenhum dado foi coletado. Verifique os seletores CSS.")