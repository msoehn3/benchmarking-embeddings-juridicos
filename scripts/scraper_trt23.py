from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from urllib.parse import urlparse


# === CONFIGURAÇÕES ===
output_dir = "data/ementas"
os.makedirs(output_dir, exist_ok=True)

reiniciar_cada_n_ementas = 500  # Reinicia o navegador a cada 500 ementas


# === Função para configurar o navegador ===
def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1560,901")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)
    return driver, wait


# === Função para acessar e configurar a busca ===
def configurar_busca(driver, wait):
    driver.get("https://pje.trt23.jus.br/jurisprudencia/")
    time.sleep(5)

    # Fecha popup inicial
    try:
        btn_fechar = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="FECHAR"]')))
        btn_fechar.click()
        print("✅ Popup fechado.")
    except:
        print("⚠️ Popup 'Fechar' não encontrado.")

    # Campo "Palavras na ementa"
    campo_ementa = driver.find_element(By.ID, "filtrosEEmenta")
    campo_ementa.clear()
    campo_ementa.send_keys("ementa")

     # Campo "Palavras no dispositivo"
    campo_ementa = driver.find_element(By.ID, "filtrosEDispositivo")
    campo_ementa.clear()
    campo_ementa.send_keys("acórdão")   

    # Campo "Data de Assinatura - Início"
    campo_data_inicio = driver.find_element(By.XPATH, "//input[@aria-label='Filtro data inicial de assinatura do documento']")
    driver.execute_script("""
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """, campo_data_inicio, "01/01/2022")

    # Campo "Data de Assinatura - Final"
    campo_data_final = driver.find_element(By.XPATH, "//input[@aria-label='Filtro data final de assinatura do documento']")
    driver.execute_script("""
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """, campo_data_final, "31/12/2024")

    # Clicar no botão "Pesquisar"
    btn_pesquisar = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"Pesquisar")]')))
    btn_pesquisar.click()
    print("🔍 Pesquisa iniciada...")
    time.sleep(5)

# === Carrega lista de arquivos já baixados ===
arquivos_existentes = os.listdir(output_dir)
ids_existentes = set()

for arquivo in arquivos_existentes:
    if arquivo.endswith(".txt"):
        caminho = os.path.join(output_dir, arquivo)
        if os.path.getsize(caminho) > 0:  # considera só os não vazios
            id_doc = arquivo.replace(".txt", "")
            ids_existentes.add(id_doc)

print(f"📂 Total de arquivos já existentes e não vazios: {len(ids_existentes)}")


# === Função que verifica se há próxima página ===
def ha_proxima_pagina(driver):
    try:
        botao = driver.find_element(By.XPATH, '//button[@aria-label="Próxima página" and not(@disabled)]')
        return botao
    except:
        return None


# === Loop principal ===
pagina = 1
ementas_processadas = 0

driver, wait = iniciar_driver()
configurar_busca(driver, wait)

# === Aumentar quantidade de resultados por página ===
try:
    dropdown_paginacao = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "mat-select-15"))
    )
    dropdown_paginacao.click()

    opcao_100 = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//mat-option//span[normalize-space(text())="100"]'))
    )
    opcao_100.click()

    print("✅ Resultados por página ajustado para 100.")
    time.sleep(5)

except Exception as e:
    print(f"⚠️ Falha ao ajustar resultados por página: {e}")

def processar_pagina(pagina):
    print(f"\n📄 Processando página {pagina}...")

    while True:
        try:
            # Captura o primeiro botão "Ementa" visível
            botao = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[.//span[contains(., 'Ementa') and normalize-space() != '']]")
                )
            )

            link = driver.find_element(By.XPATH, "//a[contains(@aria-label, 'Inteiro teor')]")

            href = link.get_attribute("href")
            if not href:
                print("⚠️ Link vazio. Pulando.")
                remover_elemento_dom(botao)
                remover_elemento_dom(link)
                continue

            path = urlparse(href).path
            id_doc = path.strip("/").split("/")[-1]

            if id_doc in ids_existentes:
                #print(f"⏭️ Ementa {id_doc} já existe. Pulando.")
                remover_elemento_dom(botao)
                remover_elemento_dom(link)
                continue

            driver.execute_script("arguments[0].scrollIntoView(true);", botao)
            time.sleep(0.2)
            driver.execute_script("arguments[0].click();", botao)

            # Espera abrir o popup da ementa
            wait.until(EC.visibility_of_element_located((By.XPATH, "//mat-dialog-container")))

            texto_bruto = wait.until(
                EC.presence_of_element_located((By.XPATH, "//mat-dialog-container"))
            ).text.strip()

            linhas = texto_bruto.splitlines()

            if linhas and linhas[0].strip().lower() == "fechar":
                linhas = linhas[1:]

            if linhas and linhas[-1].strip().lower() == "copiar tudo":
                linhas = linhas[:-1]

            conteudo_ementa = "\n".join(linhas).strip()

            filename = os.path.join(output_dir, f"{id_doc}.txt")
            with open(filename, "w", encoding="utf-8") as f_out:
                f_out.write(conteudo_ementa)

            ids_existentes.add(id_doc)

            # Fecha popup
            btn_fechar_popup = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[@aria-label='Fechar a visualização']"))
            )
            driver.execute_script("arguments[0].click();", btn_fechar_popup)

            remover_elemento_dom(botao)
            remover_elemento_dom(link)

            time.sleep(0.5)

        except Exception:
            # Se não há mais botões de ementa, sai do loop
            try:
                driver.find_element(By.XPATH, "//button[.//span[contains(., 'Ementa')]]")
                continue
            except:
                print("🚩 Nenhuma ementa restante na página atual.")
                break


def remover_elemento_dom(el):
    try:
        driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", el)
    except:
        pass


# === Loop principal ===
pagina = 1
while True:
    processar_pagina(pagina)

    botao_proximo = ha_proxima_pagina(driver)
    if botao_proximo:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", botao_proximo)
            driver.execute_script("arguments[0].click();", botao_proximo)
            time.sleep(3)
            pagina += 1
        except Exception as e:
            print(f"⚠️ Erro ao clicar em próxima página: {e}")
            break
    else:
        print("🚩 Última página alcançada.")
        break

# === Finaliza ===
driver.quit()
print("\n🏁 Fim do processo.")
