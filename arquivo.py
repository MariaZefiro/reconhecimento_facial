import sqlite3
import re
import datetime
import cv2
import time
 
# Estabelece a conexão com o banco de dados (se não existir, será criado)
def initialize_database():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
 
    cursor.execute('''CREATE TABLE IF NOT EXISTS colaboradores
                (ID INTEGER PRIMARY KEY,
                NOME VARCHAR(255),
                TEL VARCHAR(20),
                EMAIL VARCHAR(50),
                ENDERECO VARCHAR(255),
                SEXO VARCHAR(20),
                PIX VARCHAR(50),
                HI VARCHAR(20),
                HO VARCHAR(20),
                STATUS INTEGER,
                FOTO VARCHAR(255),
                CPF VARCHAR(20),
                DN VARCHAR(20),
                CARTAO VARCHAR(20),
                CARGO VARCHAR(50))''')
    return conn, cursor
    
def initialize_database2():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS registros
                (ID INTEGER PRIMARY KEY,
                NOME VARCHAR(255),  
                CPF VARCHAR(20),             
                HI VARCHAR(20),
                HO VARCHAR(20)''')
    return conn, cursor
    
# Validações
def validate_nome(nome):
    return nome.replace(" ", "").isalpha()
 
def validate_telefone(telefone):
    return telefone.isdigit()
 
def validate_email(email):
    return '@' in email
 
def validate_cpf(cpf):
    return re.match(r'^\d{11}$', cpf)
 
def validate_data_nascimento(dn):
    return re.match(r'^\d{2}/\d{2}/\d{4}$', dn)

# Registro de Colaborador
def incluir_colaborador(conn, cursor):
    nome = input("Insira o nome:")
    while not validate_nome(nome):
        print("Nome inválido")
        nome = input("Insira o nome novamente:")
   
    telefone = input("Insira o telefone:")
    while not validate_telefone(telefone):
        print("Telefone inválido")
        telefone = input("Insira o telefone novamente:")
 
    email = input("Insira o e-mail:")
    while not validate_email(email):
        print("E-mail inválido")
        email = input("Insira o e-mail novamente:")
 
    endereco = input("Insira o endereco:")
    sexo = input("Insira o sexo:")
    pix = input("Insira o pix:")
    hi = '0'
    ho = '0'
    status = 0
 
    cpf = input("Insira o CPF:")
    while not validate_cpf(cpf):
        print("CPF inválido")
        cpf = input("Insira o CPF novamente:")

    salvar_imagem(nome,cpf)
    foto = f"C:\\Users\\maria.couto\\Desktop\\python\\{nome}_{cpf}.png"
 
    dn = input("Insira a data de nascimento (DD/MM/AAAA):")
    while not validate_data_nascimento(dn):
        print("Data de nascimento inválida")
        dn = input("Insira a data de nascimento (DD/MM/AAAA) novamente:")
 
    cartao = input("Insira o cartão:")
    cargo = input("Insira o cargo:")
 
    # Inserir dados
    cursor.execute("INSERT INTO colaboradores (NOME, TEL, EMAIL, ENDERECO, SEXO, PIX, HI, HO, STATUS, FOTO, CPF, DN, CARTAO, CARGO) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (nome, telefone, email, endereco, sexo, pix, hi, ho, status, foto, cpf, dn, cartao, cargo))
    conn.commit()
    print(f'Colaborador {nome} registrado com sucesso no sistema.')

# Excluir colaborador do banco de dados
def excluir_colaborador(conn, cursor):
    lista_de_colaboradores = cursor.execute("SELECT ID, NOME, CPF FROM colaboradores").fetchall()
    id_colaborador = input("Insira o ID do colaborador que deseja excluir:")
    for colaborador in lista_de_colaboradores:
        if id_colaborador == str(colaborador[0]):
            cursor.execute(f"DELETE FROM colaboradores WHERE ID = {id_colaborador};")
            conn.commit()
            print("Colaborador excluído com sucesso da base de dados.")
            return
    print('ID não encontrado')
 
# Atualizar o cartão do colaborador
def atualizar_colaborador(conn, cursor):
    listar_colaboradores(cursor)
    lista_de_colaboradores = cursor.execute("SELECT ID, NOME, CARTAO FROM colaboradores").fetchall()
    id_colaborador = input("Insira o ID do colaborador que deseja atualizar:")
    for colaborador in lista_de_colaboradores:
        while True:
            print("1. Nome")
            print("2. Telefone")
            print("3. E-mail")
            print("4. Endereço")
            print("5. Sexo")
            print("6. Pix")
            print("7. Foto")
            print("8. CPF")
            print("9. Cartão")
            print("10. Cargo")
            escolha = input("Escolha a opção que deseja atualizar:")
            if escolha == "1":
                if id_colaborador == str(colaborador[0]):
                    novo_nome = input("Insira o novo nome:")
                    cursor.execute(f"UPDATE colaboradores SET NOME = ? WHERE ID = ?;", (novo_nome, id_colaborador))
                    conn.commit()
                    print(f"Nome: {novo_nome} associado com sucesso a {colaborador[1]}.")
                    return
            elif escolha == "2":
                if id_colaborador == str(colaborador[0]):
                    novo_telefone = input("Insira o novo telefone:")
                    cursor.execute(f"UPDATE colaboradores SET TEL = ? WHERE ID = ?;", (novo_telefone, id_colaborador))
                    conn.commit()
                    print(f"Telefone: {novo_telefone} associado com sucesso a {colaborador[1]}.")
                    return
            elif escolha == "3":
                if id_colaborador == str(colaborador[0]):
                    novo_email = input("Insira o novo e-mail:")
                    cursor.execute(f"UPDATE colaboradores SET EMAIL = ? WHERE ID = ?;", (novo_email, id_colaborador))
                    conn.commit()
                    print(f"E-mail: {novo_email} associado com sucesso a {colaborador[1]}.")
                    return
            elif escolha == "4":
                if id_colaborador == str(colaborador[0]):
                    novo_endereco = input("Insira o novo endereço:")
                    cursor.execute(f"UPDATE colaboradores SET ENDERECO = ? WHERE ID = ?;", (novo_endereco, id_colaborador))
                    conn.commit()
                    print(f"Endereço: {novo_endereco} associado com sucesso a {colaborador[1]}.")
                    return
            elif escolha == "5":
                if id_colaborador == str(colaborador[0]):
                    novo_sexo = input("Insira o novo sexo:")
                    cursor.execute(f"UPDATE colaboradores SET SEXO = ? WHERE ID = ?;", (novo_sexo, id_colaborador))
                    conn.commit()
                    print(f"Sexo: {novo_sexo} associado com sucesso a {colaborador[1]}.")
                    return
            elif escolha == "6":
                if id_colaborador == str(colaborador[0]):
                    novo_pix = input("Insira o novo pix:")
                    cursor.execute(f"UPDATE colaboradores SET PIX = ? WHERE ID = ?;", (novo_pix, id_colaborador))
                    conn.commit()
                    print(f"Pix: {novo_pix} associado com sucesso a {colaborador[1]}.")
                    return
            elif escolha == "7":
                #if id_colaborador == str(colaborador[0]):
                    #novo_foto = input("Insira o novo cartão:")
                    #cursor.execute(f"UPDATE colaboradores SET FOTO = ? WHERE ID = ?;", (novo_cartao, id_colaborador))
                    #conn.commit()
                    #print(f"Cartão: {novo_cartao} associado com sucesso a {colaborador[1]}.")
                print("Foto manutenção")
                return
            elif escolha == "8":
                if id_colaborador == str(colaborador[0]):
                    novo_cpf = input("Insira o novo CPF:")
                    cursor.execute(f"UPDATE colaboradores SET CPF = ? WHERE ID = ?;", (novo_cpf, id_colaborador))
                    conn.commit()
                    print(f"CPF: {novo_cpf} associado com sucesso a {colaborador[1]}.")
                    return
            elif escolha == "9":
                if id_colaborador == str(colaborador[0]):
                    novo_cartao = input("Insira o novo cartão:")
                    cursor.execute(f"UPDATE colaboradores SET CARTAO = ? WHERE ID = ?;", (novo_cartao, id_colaborador))
                    conn.commit()
                    print(f"Cartão: {novo_cartao} associado com sucesso a {colaborador[1]}.")
                    return
            elif escolha == "10":
                if id_colaborador == str(colaborador[0]):
                    novo_cargo = input("Insira o novo cargo:")
                    cursor.execute(f"UPDATE colaboradores SET CARGO = ? WHERE ID = ?;", (novo_cargo, id_colaborador))
                    conn.commit()
                    print(f"Cargo: {novo_cargo} associado com sucesso a {colaborador[1]}.")
                    return
    print('ID não encontrado')

# Listagem dos Colaboradores
def listar_colaboradores(cursor):
    print("Lista de Colaboradores:")
    colaboradores = cursor.execute("SELECT * FROM colaboradores").fetchall()
    for colaborador in colaboradores:
        print(colaborador)

# Acesso do colaborador

 
def salvar_imagem(nome,cpf):

    cap=cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao abrir câmera.")
        exit()

    while True:
        ret, frame=cap.read()

        if not ret:
            print("Erro ao capturar o frame.")
            break

        cv2.imshow("Captura de imagem",frame)

        key = cv2.waitKey(1)

        if key == ord('q'):
            break

    cv2.imwrite(f'{nome}_{cpf}.png',frame)
    print(f"Imagem captura e salva como '{nome}_{cpf}.png'.")

    cap.release()
    cv2.destroyAllWindows()

# Acesso do colaborador
def registrar_colaborador(conn, cursor, cartao):
    card_solicitando = cartao
    colaborador = cursor.execute("SELECT ID, NOME, HI, HO, STATUS, CARTAO FROM colaboradores WHERE CARTAO = ?", (card_solicitando,)).fetchone()
    if colaborador:
        status = colaborador[4]
        if status == 0:
            data_hora_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            cursor.execute("UPDATE colaboradores SET STATUS = ?, HI = ? WHERE ID = ?;", (1, data_hora_atual, colaborador[0]))
            conn.commit()
            print(f"Acesso realizado!\nBem vindo, {colaborador[1]}!")
        elif status == 1:
            data_hora_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            cursor.execute("UPDATE colaboradores SET STATUS = ?, HO = ? WHERE ID = ?;", (0, data_hora_atual, colaborador[0]))
            conn.commit()
            print(f"Acesso realizado!\nAté logo, {colaborador[1]}!")

def main():
    conn, cursor = initialize_database()
    while True:
        print("*** SISTEMA DE PONTO ***")
        print("1. Incluir")
        print("2. Listar")
        print("3. Excluir")
        print("4. Atualizar")
        print("5. Sair")
        escolha = input("Escolha a opção:")
        if escolha == "1":
            incluir_colaborador(conn, cursor)
        elif escolha == "2":
            listar_colaboradores(cursor)
        elif escolha == "3":
            excluir_colaborador(conn, cursor)
        elif escolha == "4":
            atualizar_colaborador(conn, cursor)            
        elif escolha == "5":
            break
        else:
            colaborador = cursor.execute("SELECT * FROM colaboradores WHERE CARTAO = ?", (escolha,)).fetchone()
            if colaborador:
                print("Nome:", colaborador[1])
                print("Telefone:", colaborador[2])
                print("E-mail:", colaborador[3])
                print("Endereço:", colaborador[4])
                print("Sexo:", colaborador[5])
                print("Pix:", colaborador[6])
                print("CPF:", colaborador[11])
                print("Data de Nascimento:", colaborador[12])
                print("Cartão:", colaborador[13])
                print("Cargo:", colaborador[14])

                img_path = colaborador[10]
                img = cv2.imread(img_path)
                print(img_path)
                if img is not None:
                    cv2.imshow("Foto do colaborador:",img)
                    cv2.waitKey(3000)
                    cv2.destroyAllWindows()
                else:
                    print("Foto do colaborador não encontrada")
                

                registrar_colaborador(conn,cursor,escolha)


        
main()