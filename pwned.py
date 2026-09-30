import hashlib
import time
import os

# --- Paleta de Cores ---
class Cor:
    VERDE = '\033[92m'
    VERMELHO = '\033[91m'
    AMARELO = '\033[93m'
    AZUL = '\033[94m'
    MAGENTA = '\033[95m'
    NEGRITO = '\033[1m'
    RESET = '\033[0m'

# --- Banco de Dados ---
# Dicionário baseado em relatórios de vazamentos do NordVPN.

# Top 20 senhas mais usadas no Brasil
senhas_brasil = [
    "admin", "123456", "12345678", "123456789", "12345",
    "lucas123", "flamengo", "brasil", "102030", "12q3456",
    "fera@123", "1234567", "142536", "********", "1234567890", 
    "senha", "password", "qwerty", "111111", "123123"
]

# Top 20 senhas mais usadas Globalmente
senhas_global = [
    "123456", "admin", "12345678", "123456789", "12345",
    "password", "Aa123456", "1234567890", "Pass@123", "admin123",
    "1234567", "123123", "111111", "12345678910", "P@ssw0rd",
    "Password", "Aa@123456", "admintelecom", "Admin@123", "112233"
]

# Juntando as duas listas e removendo as duplicatas para criar a base do servidor
todas_senhas = list(set(senhas_brasil + senhas_global))

def gerar_banco_servidor():
    """Gera o banco de dados do servidor contendo APENAS os hashes SHA-1."""
    banco = []
    for s in todas_senhas:
        hash_sha1 = hashlib.sha1(s.encode('utf-8')).hexdigest().upper()
        banco.append(hash_sha1)
    
    # Adicionando alguns hashes aleatórios para fazer volume visual
    banco.append("5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8")
    banco.append("5BAA6AB329381920391029384910293849102938")
    return sorted(banco)

BANCO_SERVIDOR = gerar_banco_servidor()

# --- Funções Visuais e Didáticas ---
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def animacao_loading(texto, segundos):
    """Simula um carregamento/tempo de rede para efeito didático."""
    print(f"{Cor.AZUL}{texto}{Cor.RESET}", end="")
    for _ in range(segundos * 2):
        print(f"{Cor.AZUL}.{Cor.RESET}", end="", flush=True)
        time.sleep(0.5)
    print("\n")

def mostrar_dicionarios_senhas():
    limpar_tela()
    print(f"{Cor.NEGRITO}{Cor.VERMELHO}=== DICIONÁRIOS DE VAZAMENTOS (TEXTO CLARO) ==={Cor.RESET}\n")
    print("Estas são as senhas coletadas de vazamentos reais (Data Breaches).")
    print("Elas costumam circular na internet desta forma, desprotegidas:\n")
    
    print(f"{Cor.NEGRITO}{Cor.VERDE}Top Senhas - BRASIL:{Cor.RESET}")
    # Mostra as primeiras 10 para não poluir muito a tela
    for i, s in enumerate(senhas_brasil[:10]):
        print(f" {i+1:02d}. {s}")
    print(" ... (e muitas outras)")
    
    print(f"\n{Cor.NEGRITO}{Cor.AZUL}Top Senhas - GLOBAL:{Cor.RESET}")
    for i, s in enumerate(senhas_global[:10]):
        print(f" {i+1:02d}. {s}")
    print(" ... (e muitas outras)\n")
    
    input(f"{Cor.NEGRITO}Pressione ENTER para voltar ao menu...{Cor.RESET}")

def mostrar_banco_dados():
    limpar_tela()
    print(f"{Cor.NEGRITO}{Cor.MAGENTA}=== BANCO DE DADOS DO SERVIDOR HIBP ==={Cor.RESET}\n")
    print("O servidor processou o dicionário e agora armazena apenas os Hashes SHA-1.")
    print("Se um hacker invadir o servidor agora, é apenas isso que ele vai ver:\n")
    
    for i, h in enumerate(BANCO_SERVIDOR[:10]):
        print(f"Registro {i+1:02d}: {Cor.AMARELO}{h}{Cor.RESET}")
    print(f"Registro ...: {Cor.AMARELO}(e mais bilhões de hashes...){Cor.RESET}\n")
    
    input(f"{Cor.NEGRITO}Pressione ENTER para voltar ao menu...{Cor.RESET}")

def verificar_senha():
    limpar_tela()
    print(f"{Cor.NEGRITO}{Cor.MAGENTA}=== TESTE DE VAZAMENTO (K-ANONYMITY) ==={Cor.RESET}\n")
    senha_teste = input("Digite a senha que deseja testar: ")
    
    print(f"\n{Cor.NEGRITO}[CLIENTE]{Cor.RESET} Gerando hash SHA-1 localmente (na sua máquina)...")
    time.sleep(1)
    hash_teste = hashlib.sha1(senha_teste.encode('utf-8')).hexdigest().upper()
    print(f"Hash gerado: {Cor.AMARELO}{hash_teste}{Cor.RESET}\n")
    
    print(f"{Cor.NEGRITO}[CLIENTE]{Cor.RESET} Separando o hash (K-Anonymity)...")
    time.sleep(1)
    prefixo = hash_teste[:5]
    sufixo_teste = hash_teste[5:]
    print(f"Prefixo (Enviado à rede) : {Cor.VERDE}{prefixo}{Cor.RESET}")
    print(f"Sufixo  (Fica em segredo): {Cor.AZUL}{sufixo_teste}{Cor.RESET}\n")
    
    animacao_loading("[REDE] Enviando apenas o prefixo para o servidor", 2)
    
    print(f"{Cor.NEGRITO}[SERVIDOR]{Cor.RESET} Buscando prefixo '{Cor.VERDE}{prefixo}{Cor.RESET}' no banco de dados...")
    time.sleep(1.5)
    
    # Servidor filtra hashes que começam com o prefixo e devolve os sufixos
    resultados_servidor = [h[5:] for h in BANCO_SERVIDOR if h.startswith(prefixo)]
    
    if len(resultados_servidor) == 0:
        print(f"O servidor encontrou: {Cor.NEGRITO}0 sufixos{Cor.RESET}\n")
    else:
        print(f"O servidor encontrou {len(resultados_servidor)} sufixo(s) correspondente(s):")
        for suf in resultados_servidor:
            print(f" -> {Cor.AMARELO}{suf}{Cor.RESET}")
        print()
        
    animacao_loading("[REDE] Retornando lista de sufixos para o cliente", 2)
    
    print(f"{Cor.NEGRITO}[CLIENTE]{Cor.RESET} Comparando o sufixo local com a lista do servidor...")
    time.sleep(1.5)
    
    if sufixo_teste in resultados_servidor:
        print(f"\n{Cor.VERMELHO}{Cor.NEGRITO}>>> ALERTA! <<< {Cor.RESET}")
        print(f"{Cor.VERMELHO}Match exato encontrado! Sua senha está na base de vazamentos.{Cor.RESET}\n")
    else:
        print(f"\n{Cor.VERDE}{Cor.NEGRITO}>>> SEGURO! <<< {Cor.RESET}")
        print(f"{Cor.VERDE}Nenhum match. Sua senha não foi encontrada na base de vazamentos.{Cor.RESET}\n")

    input(f"{Cor.NEGRITO}Pressione ENTER para voltar ao menu...{Cor.RESET}")

# --- Menu Principal ---
def menu():
    while True:
        limpar_tela()
        print(f"{Cor.NEGRITO}{Cor.AZUL}========================================={Cor.RESET}")
        print(f"{Cor.NEGRITO}{Cor.AZUL}     SIMULADOR - HAVE I BEEN PWNED       {Cor.RESET}")
        print(f"{Cor.NEGRITO}{Cor.AZUL}========================================={Cor.RESET}")
        print("1. Ver Dicionários de Senhas (Texto Claro)")
        print("2. Ver Banco de Dados (Hashes no Servidor)")
        print("3. Testar uma Senha (K-Anonymity na prática)")
        print("4. Sair")
        print(f"{Cor.AZUL}========================================={Cor.RESET}")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            mostrar_dicionarios_senhas()
        elif escolha == '2':
            mostrar_banco_dados()
        elif escolha == '3':
            verificar_senha()
        elif escolha == '4':
            print("\nEncerrando demonstração. Obrigado!\n")
            break
        else:
            print(f"{Cor.VERMELHO}Opção inválida!{Cor.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    menu()