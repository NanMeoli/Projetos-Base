def sistema_cadastro():
    """Função principal que executa o sistema de cadastro de participantes."""

    participantes = []
    
    print("--- 📝 Sistema Simples de Cadastro de Participantes ---")
    
    while True:

        print("\n--- Novo Cadastro ---")

        nome = input("Nome Completo: ").strip()
        if not nome:
            print("❌ Nome não pode ser vazio.")
            continue

        email = input("E-mail: ").strip()
        if not email or "@" not in email:
            print("❌ E-mail inválido. Certifique-se de incluir o '@'.")
            continue

        cpf = input("CPF (somente números): ").strip()
        if not cpf or not cpf.isdigit() or len(cpf) != 11:
            print("❌ CPF inválido. Deve conter 11 dígitos numéricos.")
            continue

        cpf_duplicado = False
        for p in participantes:
            if p['cpf'] == cpf:
                cpf_duplicado = True
                break
        
        if cpf_duplicado:
            print(f"⚠️ Erro: Já existe um participante cadastrado com o CPF {cpf}.")
        else:

            novo_participante = {
                'nome': nome,
                'email': email,
                'cpf': cpf
            }

            participantes.append(novo_participante)
            print("✅ Participante cadastrado com sucesso!")

        continuar = input("\nDeseja cadastrar outro participante? (s/n): ").lower()
        if continuar != 's':
            break
            
    print("\n--- 📊 Resultado Final ---")

    if participantes:
        print("\nLista de Participantes:")
        for i, p in enumerate(participantes):
            cpf_formatado = f"{p['cpf'][:3]}.{p['cpf'][3:6]}.{p['cpf'][6:9]}-{p['cpf'][9:]}"
            print(f"  {i+1}. Nome: {p['nome']} | E-mail: {p['email']} | CPF: {cpf_formatado}")
    else:
         print("Nenhum participante foi cadastrado.")
    print(f"\n✨ Quantidade Total de Inscritos: **{len(participantes)}**")

if __name__ == "__main__":
    sistema_cadastro()