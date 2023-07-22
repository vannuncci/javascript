
import logging
import os
import sys

import shutil
import configparser
import psutil
import pyzipper
import requests
import win32serviceutil
import tempfile
from contextlib import suppress

from datetime import datetime
from playwright.sync_api import sync_playwright 

# Função para verificar status do contrato
def verificar_status_contrato(status_contrato,tipo_dominio):
    if status_contrato == 'A' and tipo_dominio == 'Web':    # Contrato ativo e tipo de domínio Web
        print("Contrato Ativo e tipo de domínio Web")
    else:
        print("Contrato Não está Ativo e/ou tipo de Domínio não é Domínio WEB") 
        sys.exit()  # Encerra a execução do programa

caminho_arquivo_token = 'token_e-robo.ini' #caminho do arquivo token

config = configparser.ConfigParser()# Crie uma instância do objeto ConfigParser
config.read(caminho_arquivo_token)# Carregue o arquivo INI
key_token_ini = config.get('secao', 'token')# Acesse o valor no arquivo INI

# Consulta do WEBSERVICE
url = "http://ws.e-kontroll.com.br/ws/erobo_chave"
data_token_api = {"token": key_token_ini}
response = requests.post(url, data=data_token_api)
response_data = response.json()  # Converte a resposta em formato JSON para um dicionário

# status consulta
tipo_dominio = response_data["tipo_dominio"]
status_contrato = response_data["status_contrato"]
dia_semana_completo = response_data["dia_semana_completo"]
hora_completo = response_data["hora_completo"]
hora_modificacao = 'null'

#diretorios
pasta_download = response_data["pasta_download"]
pasta_banco_dados = response_data["pasta_banco_dados"]

# senhas
hash_senha_dominio = response_data["senha_onvio"]
usuario_onvio = response_data["usuario_onvio"]
key_zip_backup = 'dominioweb' #senha padrão para descompactar backup

# Nome do serviço do BD dominio
nome_servico = 'SQLANYs_Servidor_Dominio16'

# Nome do serviço do e-robo
nome_servico_erobo = 'prunsrv.exe'

verificar_status_contrato(status_contrato,tipo_dominio) #Contrato continua ativo?

def run() -> str:
    with sync_playwright() as playwright:
        try:
            # Inicializa o navegador Chromium
            browser = playwright.chromium.launch(headless=False)

            # Cria um novo contexto
            context = browser.new_context()

            # Cria uma nova página
            page = context.new_page()

            # Abre uma nova página
            page.goto("https://suporte.dominioatendimento.com/login.html")

            # Preenche os campos de login
            page.fill('xpath=//*[@id="j_username"]', usuario_onvio)
            page.fill('xpath=//*[@id="j_password"]', hash_senha_dominio)

            # Clica no botão de login
            page.locator('xpath=//*[@id="loginForm"]/div[3]/div/input').click()
            page.wait_for_timeout(8)
            # Realiza uma sequência de cliques em diferentes elementos na página
            page.goto("https://suporte.dominioatendimento.com/backup/faces/bkp-realizado.html?backupTipo=2")

            # Aguarda um tempo de espera de 5 segundos
            page.wait_for_timeout(8)

            # Inicia o download de um arquivo e aguarda até que o download seja concluído
            with page.expect_download() as download_info:
                page.locator('xpath=//*[@id="DataTables_Table_0"]/tbody/tr/td[2]/a/i').click()
            download = download_info.value
            file_name = download.suggested_filename

            # Salva o arquivo baixado na pasta de destino especificada
            download.save_as(os.path.join(pasta_download, file_name))

            # New file name with .zip extension
            new_file_name = os.path.splitext(file_name)[0] + ".zip"

            # Rename the downloaded file to .zip
            os.rename(os.path.join(pasta_download, file_name), os.path.join(pasta_download, new_file_name))

            # Fecha o contexto e o navegador
            context.close()
            browser.close()
            return new_file_name

        except Exception as e:
            # Registra o erro no log com a hora atual
            logging.error(f"Erro durante a execução: {e}, Hora: {datetime.now()}")
            return None


# Chama a função "run"
new_file_name = run()


if not os.path.exists(pasta_banco_dados):
    os.makedirs(pasta_banco_dados)

# Verifica se as variáveis pasta_download e new_file_name não são None
if pasta_download is not None and new_file_name is not None:
    try:
        # Para pausar o serviço do BD dominio e realizar a extração do arquivo .zip
        # pausar servico
        def pausar_servico(nome_servico):
            # Verifica se o serviço está em execução
            if is_servico_em_execucao(nome_servico):
                win32serviceutil.StopService(nome_servico)

        # Para iniciar o serviço do BD dominio
        def iniciar_servico(nome_servico):
            # Verifica se o serviço está pausado
            if not is_servico_em_execucao(nome_servico):
                win32serviceutil.StartService(nome_servico)

        # Função auxiliar para verificar se o serviço está em execução
        def is_servico_em_execucao(nome_servico):
            try:
                service = psutil.win_service_get(nome_servico)
                return service.status() == psutil.STATUS_RUNNING
            except psutil.NoSuchProcess:
                return False

        pausar_servico(nome_servico) # pausar servico
        pausar_servico(nome_servico_erobo) # pausar servico e-robo


        def listar_arquivos_e_pastas(diretorio):
            # Lista com todos os arquivos e pastas no diretório
            lista_todos = os.listdir(diretorio)

            # Lista com tudo na pasta, exceto arquivos que começam com a palavra "backup"
            lista_sem_backup = [item for item in lista_todos if not item.startswith("backup")]

            # Lista apenas com os itens que iniciam com o nome "backup"
            lista_apenas_backup = [item for item in lista_todos if item.startswith("backup")]

            return lista_todos, lista_sem_backup, lista_apenas_backup

        def criar_zip_e_limpar(diretorio_alvo, lista_sem_backup, lista_apenas_backup):
            data_atual = datetime.now().strftime("%d-%m-%Y")
            valor = f"backup_{data_atual}.zip"

            if valor not in todos:
                # Criar um diretório temporário para armazenar os arquivos a serem compactados
                diretorio_temporario = tempfile.mkdtemp()

                # Copiar os arquivos de lista_sem_backup para o diretório temporário
                for item in lista_sem_backup:
                    origem = os.path.join(diretorio_alvo, item)
                    destino = os.path.join(diretorio_temporario, item)
                    if os.path.isfile(origem):
                        shutil.copy(origem, destino)
                    elif os.path.isdir(origem):
                        shutil.copytree(origem, destino)

                # Deletar todo o conteúdo de diretorio_alvo
                for item in todos:
                    item_caminho = os.path.join(diretorio_alvo, item)
                    if os.path.isfile(item_caminho):
                        os.chmod(item_caminho, 0o777)
                        os.remove(item_caminho)
                    elif os.path.isdir(item_caminho):
                        shutil.rmtree(item_caminho)

                # Criar o arquivo zip
                shutil.make_archive(os.path.join(diretorio_alvo, valor.split(".")[0]), 'zip', diretorio_temporario)

                # Remover o diretório temporário e seu conteúdo, ignorando caso o diretório já tenha sido deletado
                with suppress(FileNotFoundError):
                    shutil.rmtree(diretorio_temporario)

                print(f"Arquivo de backup '{valor}' criado com sucesso!")

            else:
                if len(lista_apenas_backup) > 1:
                    # Deletar tudo que não seja o "backup_{data_atual}.zip"
                    for item in lista_apenas_backup:
                        if item != valor:
                            item_caminho = os.path.join(diretorio_alvo, item)
                            if os.path.isfile(item_caminho):
                                os.remove(item_caminho)
                            elif os.path.isdir(item_caminho):
                                shutil.rmtree(item_caminho)

                    print("Apenas o arquivo de backup atual foi mantido.")
                else:
                    print("A pasta já existe e contém apenas o arquivo de backup atual.")

        todos, sem_backup, apenas_backup = listar_arquivos_e_pastas(pasta_banco_dados)
        criar_zip_e_limpar(pasta_banco_dados, sem_backup, apenas_backup)

        caminho_arquivo_zip = os.path.join(pasta_download, new_file_name)
        with open(caminho_arquivo_zip, 'rb') as zip_file:
            with pyzipper.AESZipFile(zip_file) as z:
                z.pwd = bytes(key_zip_backup, 'utf-8')  # Define a senha para o arquivo .zip
                z.extractall(pasta_banco_dados)  # Extrai os arquivos para a pasta do backup

        # Exclui o arquivo .zip após a extração
        if hora_modificacao == 'null':
            os.remove(caminho_arquivo_zip)

        # despausar servico
        iniciar_servico(nome_servico)

    except Exception as e:
        # Registra o erro no log com a hora atual
        logging.error(f"Erro durante a extração do arquivo .zip: {e}, Hora: {datetime.now()}")