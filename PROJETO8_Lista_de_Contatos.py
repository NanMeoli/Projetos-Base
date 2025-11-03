lista_contatos = []

def adicionar_contato():
    """Adiciona um novo contato à lista."""
    print("\n--- Adicionar Novo Contato ---")
    
    nome = input("Digite o Nome do contato: ").strip()
    if not nome:
        print("❌ O nome não pode ser vazio. Operação cancelada.")
        return

    telefone = input("Digite o Telefone: ").strip()
    email = input("Digite o E-mail: ").strip()
    
    novo_contato = {
        'nome': nome,
        'telefone': telefone,
        'email': email
    }
 
    lista_contatos.append(novo_contato)
    print(f"\n✅ Contato '{nome}' adicionado com sucesso!")


def listar_contatos():
    """Exibe todos os contatos cadastrados."""
    print("\n--- Lista de Contatos ---")
    
    if not lista_contatos:
        print("⚠️ A lista de contatos está vazia.")
        return 
        
    for i, contato in enumerate(lista_contatos):
        print(f"[{i+1}] Nome: {contato['nome']}")
        print(f"    Telefone: {contato['telefone']}")
        print(f"    E-mail: {contato['email']}")
        print("-" * 20)


def remover_contato():
    """Remove um contato da lista pelo número (índice)."""
    if not lista_contatos:
        print("\n⚠️ Não há contatos para remover.")
        return
        
    listar_contatos()
    print("\n--- Remover Contato ---")
    
    try:
        num_remover = input("Digite o NÚMERO do contato que deseja remover (ou 'c' para cancelar): ").lower().strip()
        
        if num_remover == 'c':
            print("❌ Operação de remoção cancelada.")
            return

        indice_remover = int(num_remover) - 1

        if 0 <= indice_remover < len(lista_contatos):
            contato_removido = lista_contatos.pop(indice_remover)
            print(f"\n✅ Contato de '{contato_removido['nome']}' removido com sucesso!")
        else:
            print(f"❌ Número inválido. O número deve estar entre 1 e {len(lista_contatos)}.")
            
    except ValueError:
        print("❌ Entrada inválida. Por favor, digite apenas o número do contato.")


def menu_principal():
    """Função principal que executa o loop do menu."""
    
    print("--- 📱 Sistema de Lista de Contatos ---")
    
    while True:
        print("\n--- Menu ---")
        print("[1] Adicionar Contato")
        print("[2] Listar Contatos")
        print("[3] Remover Contato")
        print("[4] Sair")
        
        escolha = input("Escolha uma opção (1-4): ").strip()

        if escolha == '1':
            adicionar_contato()
        elif escolha == '2':
            listar_contatos()
        elif escolha == '3':
            remover_contato()
        elif escolha == '4':

            print("\n👋 Encerrando o programa. Até logo!")
            break 
        else:
            print("❌ Opção inválida. Por favor, escolha um número de 1 a 4.")

if __name__ == "__main__":
    menu_principal()