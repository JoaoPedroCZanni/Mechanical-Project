import os
import re
import json
import requests
import webbrowser
import pandas as pd
import oracledb

conn = None
def connect_to_database():
    username = ''
    password = ''
    cs = ""
    try:
        conn = oracledb.connect(user=username, password=password, dsn=cs)
        print("Conexão realizada com sucesso!")
        return conn
    except oracledb.DatabaseError as e:
        error, = e.args
        print("Erro ao conectar ao banco de dados:")
        print(f"Código do erro: {error.code}")
        print(f"Mensagem do erro: {error.message}")
        return None
def inserir_usuario_no_banco(conn, nome, email):
    try:
        cursor = conn.cursor()
        cursor.execute(''''
            INSERT INTO t_usuarios (nome, email) 
            VALUES (:1, :2)
        ''', (nome, email))
        conn.commit()
        print("Usuário cadastrado com sucesso!")
    except oracledb.DatabaseError as e:
        error, = e.args
        print("Erro ao inserir o usuário no banco de dados:")
        print(f"Código do erro: {error.code}")
        print(f"Mensagem do erro: {error.message}")
    finally:
        cursor.close()
def main():
    conn = connect_to_database()
    if conn is not None:
        nome = input("Digite o nome do usuário: ")
        email = input("Digite o e-mail do usuário: ")
        inserir_usuario_no_banco(conn, nome, email)
        conn.close()    
    input("Pressione Enter para entrar no Sistema...")
if __name__ == "__main__":
    main()

# MENSAGENS PADRÃO
MSG_QTDE_INVALIDA = "Quantidade inválida! Apenas números positivos são permitidos. Por favor, insira um valor válido."
MSG_VALOR_INVALIDO = "Valor inválido! Por favor, insira um número positivo."
MSG_FORMATO_PLACA_INVALIDO = "Formato de placa inválido. A placa deve seguir o formato AAA-0000 ou AAA0A00."
MSG_EMAIL_INVALIDO = "E-mail inválido."
MSG_SENHA_INVALIDA = "A senha deve conter pelo menos 8 caracteres."
MSG_CADASTRO_SUCESSO = "Cadastro realizado com sucesso!"
MSG_CADASTRO_USUARIO = "Usuário cadastrado com sucesso!"
MSG_CADASTRO_VEICULO = "Veículo cadastrado com sucesso!"
MSG_CADASTRO_REMOVIDO = "Veículo removido com sucesso!"
MSG_CADASTRO_ALTERADO = "Veículo alterado com sucesso!"
MSG_OPCAO_INVALIDA = "Opção inválida. Por favor, escolha novamente."
MSG_NENHUM_VEICULO = "Nenhum veículo cadastrado."
MSG_NENHUM_CADASTRO = "Nenhum cadastro encontrado."
MSG_PROBLEMA_RELATADO = "Problema relatado com sucesso!"
MSG_PROBLEMA_REMOVIDO = "Problema removido com sucesso!"


# VARIÁVEIS DE ARMAZENAMENTO
registro_veiculos = []
cadastro_pessoal = []
problemas_veiculos = {}


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


# GERENCIAR VEICULOS 
def adicionar_veiculo(modelo, placa):
    registro_veiculos.append({"modelo": modelo, "placa": placa})                                                                    
    print(MSG_CADASTRO_VEICULO)
    input("\nPressione Enter para voltar ao menu...")
def listar_veiculos():
    limpar_tela()
    if not registro_veiculos:
        print(MSG_NENHUM_VEICULO)
    else:
        for i, veiculo in enumerate(registro_veiculos, 1):
            print(f"{i}. Modelo: {veiculo['modelo']} - Placa: {veiculo['placa']}")
    input("\nPressione Enter para voltar ao menu...")
def buscar_veiculo_por_placa(placa):
    for veiculo in registro_veiculos:
        if veiculo["placa"] == placa:
            return veiculo
    return None
def alterar_veiculo(placa_antiga, modelo_novo, placa_nova):
    veiculo = buscar_veiculo_por_placa(placa_antiga)
    if veiculo:
        veiculo["modelo"] = modelo_novo
        veiculo["placa"] = placa_nova
        print(MSG_CADASTRO_ALTERADO)
    else:
        print("Veículo não encontrado.")
    input("\nPressione Enter para voltar ao menu...")
def remover_veiculo(placa):
    global registro_veiculos
    veiculo_a_remover = [veiculo for veiculo in registro_veiculos if veiculo["placa"] == placa]
    if veiculo_a_remover:
        registro_veiculos = [veiculo for veiculo in registro_veiculos if veiculo["placa"] != placa]
        print(MSG_CADASTRO_REMOVIDO)
    else:
        print("Veículo não encontrado.")
    input("\nPressione Enter para voltar ao menu...")

def inserir_usuario_no_banco(conn, email, senha):
    try:
        cursor = conn.cursor()
        cursor.execute('''  
            INSERT INTO t_usuarios (email, senha)  -- Removi o nome aqui
            VALUES (:1, :2)
        ''', (email, senha))
        conn.commit()
        print(MSG_CADASTRO_SUCESSO)
    except oracledb.DatabaseError as e:
        error, = e.args
        print("Erro ao inserir o usuário no banco de dados:")
        print(f"Código do erro: {error.code}")
        print(f"Mensagem do erro: {error.message}")
    finally:
        cursor.close()

# GERENCIAR CADASTRO PESSOAL
def adicionar_pessoal(email, senha):
    cadastro_pessoal.append({"email": email, "senha": senha})
    if conn is not None:
        inserir_usuario_no_banco(conn, email, senha)  
        conn.close() 
    print(MSG_CADASTRO_USUARIO)
    input("\nPressione Enter para voltar ao menu...")

def listar_pessoal():
    limpar_tela()
    if not cadastro_pessoal:
        print(MSG_NENHUM_CADASTRO)
    else:
        for i, pessoal in enumerate(cadastro_pessoal, 1):
            print(f"{i}. E-mail: {pessoal['email']}")
    input("\nPressione Enter para voltar ao menu...")
def buscar_pessoal_por_email(email):
    for pessoal in cadastro_pessoal:
        if pessoal["email"] == email:
            return pessoal
    return None
def alterar_pessoal(email_antigo, email_novo, senha_nova):
    pessoal = buscar_pessoal_por_email(email_antigo)
    if pessoal:
        pessoal["email"] = email_novo
        pessoal["senha"] = senha_nova
        print("Cadastro alterado com sucesso.")
    else:
        print("Cadastro não encontrado.")
    input("\nPressione Enter para voltar ao menu...")
def remover_pessoal(email, senha):
    global cadastro_pessoal
    try:
        pessoal_a_remover = [pessoal for pessoal in cadastro_pessoal if pessoal["email"] == email and pessoal["senha"] == senha]
        if pessoal_a_remover:
            cadastro_pessoal = [pessoal for pessoal in cadastro_pessoal if not (pessoal["email"] == email and pessoal["senha"] == senha)]
            print("Cadastro removido com sucesso.")
        else:
            print("E-mail ou senha incorretos, ou cadastro não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    input("\nPressione Enter para voltar ao menu...")


# RELATAR PROBLEMAS 
def relatar_problema_entrada():
    while True:
        placa = input("Digite a placa do veículo (formato AAA-0000 ou AAA0A00): ")
        if validar_placa(placa):
            descricao_problema = input("Descreva o problema: ").strip()
            if descricao_problema:
                relatar_problema(placa, descricao_problema)
                break
            else:
                print("A descrição do problema não pode estar em branco. Por favor, insira uma descrição válida.")
        else:
            print(MSG_FORMATO_PLACA_INVALIDO)
def relatar_problema(placa, descricao_problema):
    veiculo = buscar_veiculo_por_placa(placa)
    if veiculo:
        if placa not in problemas_veiculos:
            problemas_veiculos[placa] = []
        problemas_veiculos[placa].append(descricao_problema)
        print(MSG_PROBLEMA_RELATADO)
    else:
        print("Veículo não encontrado.")
    input("\nPressione Enter para voltar ao menu...")
def listar_problemas():
    limpar_tela()
    if not problemas_veiculos:
        print("Nenhum problema relatado.")
    else:
        for placa, problemas in problemas_veiculos.items():
            print(f"Problemas para o veículo {placa}:")
            for problema in problemas:
                print(f"- {problema}")
    input("\nPressione Enter para voltar ao menu...")
def remover_problema(placa, descricao_problema):
    if placa in problemas_veiculos and descricao_problema in problemas_veiculos[placa]:
        problemas_veiculos[placa].remove(descricao_problema)
        print(MSG_PROBLEMA_REMOVIDO)
    else:
        print("Problema não encontrado.")
    input("\nPressione Enter para voltar ao menu...")


# FUNÇÕES DE VALIDAÇÃO
def validar_placa(placa):
    return re.match(r"^[A-Z]{3}-\d{4}$|^[A-Z]{3}\d[A-Z]\d{2}$", placa) is not None
def validar_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None
def validar_senha(senha):
    return len(senha) >= 8


# FUNÇÕES DE ENTRADA
def adicionar_veiculo_entrada():
    while True:
        modelo = input("Digite o modelo do veículo: ").strip()
        if modelo:
            while True:
                placa = input("Digite a placa do veículo (formato AAA-0000 ou AAA0A00): ")
                if validar_placa(placa):
                    adicionar_veiculo(modelo, placa)
                    break
                else:
                    print(MSG_FORMATO_PLACA_INVALIDO)
            break
        else:
            print("O modelo do veículo não pode estar em branco. Por favor, insira um modelo válido.")
def adicionar_pessoal_entrada():
    while True:
        email = input("Digite seu e-mail: ")
        if validar_email(email):
            while True:
                senha = input("Digite sua senha (pelo menos 8 caracteres): ")
                if validar_senha(senha):
                    adicionar_pessoal(email, senha)
                    break
                else:
                    print(MSG_SENHA_INVALIDA)
            break
        else:
            print(MSG_EMAIL_INVALIDO)
def alterar_pessoal_entrada():
    if not cadastro_pessoal:
        print(MSG_NENHUM_CADASTRO)
        input("\nPressione Enter para voltar ao menu...")
        return
    email_antigo = input("Digite o e-mail do cadastro que deseja alterar: ")
    pessoal = buscar_pessoal_por_email(email_antigo)
    if pessoal:
        while True:
            email_novo = input("Digite o novo e-mail: ")
            if validar_email(email_novo):
                while True:
                    senha_nova = input("Digite a nova senha: ")
                    if validar_senha(senha_nova):
                        alterar_pessoal(email_antigo, email_novo, senha_nova)
                        break
                    else:
                        print(MSG_SENHA_INVALIDA)
                break
            else:
                print(MSG_EMAIL_INVALIDO)
    else:
        print("Cadastro não encontrado.")
    input("\nPressione Enter para voltar ao menu...")


# MOSTRAR MAPAS (consumo de API externa)
def mostrar_mapa(placa):
    endereco = "Bela vista, 1060, São Paulo, SP" # aqui será adicionado as localizações das oficinas 
    url_mapa = f"https://www.google.com/maps/search/?api=1&query={endereco.replace(' ','%20')}"
    webbrowser.open(url_mapa)  
    print(f"A localização das oficinas mais próximas foi aberta no navegador.")
    input("\nPressione Enter para voltar ao menu...")
def mostrar_mapa_entrada():
    placa = input("Digite a placa do veículo: ")
    if buscar_veiculo_por_placa(placa):
        mostrar_mapa(placa)
    else:
        print("Veículo não encontrado.")
        input("\nPressione Enter para voltar ao menu...")


# RELATAR PROBLEMAS MENU
def menu_problemas():
    while True:
        limpar_tela()
        print("=== RELATAR PROBLEMAS ===")
        print("1. Relatar Problema")
        print("2. Listar Problemas")
        print("3. Remover Problema")
        print("0. Voltar ao Menu Principal")
        opcao_problema = input("Escolha uma opção: ")
        if opcao_problema == "1":
            relatar_problema_entrada()
        elif opcao_problema == "2":
            listar_problemas()
        elif opcao_problema == "3":
            while True:
                placa = input("Digite a placa do veículo (formato AAA-0000 ou AAA0A00): ")
                if validar_placa(placa):
                    descricao_problema = input("Digite a descrição do problema a ser removido: ")
                    remover_problema(placa, descricao_problema)
                    break
                else:
                    print(MSG_FORMATO_PLACA_INVALIDO)
        elif opcao_problema == "0":
            break
        else:
            print(MSG_OPCAO_INVALIDA)


# EXPORTAR DADOS PARA O JSON  
def exportar_dados_json():
    dados = {
        "veiculos": registro_veiculos,
        "cadastro_pessoal": cadastro_pessoal,
        "problemas": problemas_veiculos
    }
    with open("dados.json", "w") as arquivo_json:
        json.dump(dados, arquivo_json, indent=4)
    print("Dados exportados para dados.json com sucesso!")
    input("\nPressione Enter para voltar ao menu...")


# MENU PRINCIPAL
def menu_principal():
    while True:
        limpar_tela()
        print("=== MENU PRINCIPAL ===")
        print("1. Gerenciar Veículos")
        print("2. Gerenciar Cadastro Pessoal")
        print("3. Relatar Problemas")
        print("4. Mostrar Mapa")
        print("5. Exportar dados para JSON")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            while True:
                limpar_tela()
                print("1. Adicionar Veículo")
                print("2. Listar Veículos")
                print("3. Alterar Veículo")
                print("4. Remover Veículo")
                print("0. Voltar ao Menu Principal")
                opcao_veiculo = input("Escolha uma opção: ")
                if opcao_veiculo == "1":
                    adicionar_veiculo_entrada()
                elif opcao_veiculo == "2":
                    listar_veiculos()
                elif opcao_veiculo == "3":
                    if not registro_veiculos:
                        print(MSG_NENHUM_VEICULO)
                        input("\nPressione Enter para voltar ao menu...")
                        continue
                    placa_antiga = input("Digite a placa do veículo a ser alterado: ")
                    veiculo = buscar_veiculo_por_placa(placa_antiga)
                    if veiculo:
                        modelo_novo = input("Digite o novo modelo: ")
                        placa_nova = input("Digite a nova placa (formato AAA-0000 ou AAA0A00): ")
                        if validar_placa(placa_nova):
                            alterar_veiculo(placa_antiga, modelo_novo, placa_nova)
                        else:
                            print(MSG_FORMATO_PLACA_INVALIDO)
                    else:
                        print("Veículo não encontrado.")
                    input("\nPressione Enter para voltar ao menu...")
                elif opcao_veiculo == "4":
                    if not registro_veiculos:
                        print(MSG_NENHUM_VEICULO)
                        input("\nPressione Enter para voltar ao menu...")
                        continue
                    placa = input("Digite a placa do veículo a ser removido: ")
                    remover_veiculo(placa)
                elif opcao_veiculo == "0":
                    break
                else:
                    print(MSG_OPCAO_INVALIDA)
        elif opcao == "2":
            while True:
                limpar_tela()
                print("1. Adicionar Cadastro Pessoal")
                print("2. Listar Cadastros Pessoais")
                print("3. Alterar Cadastro Pessoal")
                print("4. Remover Cadastro Pessoal")
                print("0. Voltar ao Menu Principal")
                opcao_cadastro = input("Escolha uma opção: ")
                if opcao_cadastro == "1":
                    adicionar_pessoal_entrada()
                elif opcao_cadastro == "2":
                    listar_pessoal()
                elif opcao_cadastro == "3":
                    alterar_pessoal_entrada()
                elif opcao_cadastro == "4":
                    if not cadastro_pessoal:
                        print(MSG_NENHUM_CADASTRO)
                        input("\nPressione Enter para voltar ao menu...")
                        continue
                    email = input("Digite o e-mail do cadastro que deseja remover: ")
                    if buscar_pessoal_por_email(email):
                        senha = input("Digite a senha do cadastro: ")
                        remover_pessoal(email, senha)
                    else:
                        print("E-mail não encontrado. Verifique e tente novamente.")
                elif opcao_cadastro == "0":
                    break
                else:
                    print(MSG_OPCAO_INVALIDA)
        elif opcao == "3":
            menu_problemas()
        elif opcao == "4":
            mostrar_mapa_entrada()
        elif opcao == "5":
            exportar_dados_json()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print(MSG_OPCAO_INVALIDA)


# INÍCIO DO PROGRAMA
if __name__ == "__main__":
    menu_principal()
