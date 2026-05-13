import os

# ==========================================
# SISTEMA DE ARQUIVOS (Exigência do PDF)
# ==========================================
# Lemos e salvamos tudo em .txt para não perder dados ao fechar o programa

def ler_arquivo(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        return []
    with open(nome_arquivo, "r", encoding="utf-8") as f:
        return [linha.strip().split(",") for linha in f.readlines()]

def salvar_arquivo(nome_arquivo, dados):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        for linha in dados:
            f.write(",".join(map(str, linha)) + "\n")

# ==========================================
# TELAS DE ACESSO E CADASTRO
# ==========================================

def tela_acesso():
    while True:
        print("\n=== SISTEMA DE VÍDEOS ===")
        print("1. Fazer Login")
        print("2. Criar Cadastro")
        print("3. Encerrar")

        decisao = input("Sua escolha: ")

        if decisao == "1":
            dados_usuario = entrar_sistema()
            if dados_usuario:
                return dados_usuario   # Retorna dicionário com nome e tipo (admin ou comum)
            else:
                print("Credenciais incorretas!\n")
        elif decisao == "2":
            novo_cadastro()
        elif decisao == "3":
            print("Fechando o sistema...")
            exit()
        else:
            print("Alternativa inválida!")

def novo_cadastro():
    novo_user = input('Informe um nome de usuário: ')
    nova_senha = input('Crie uma senha: ')
    
    # Se o nome for "admin", ele vira administrador. Se não, é usuário comum (0)
    tipo_conta = "1" if novo_user.lower() == "admin" else "0"

    usuarios = ler_arquivo("usuarios.txt")
    usuarios.append([novo_user, nova_senha, tipo_conta])
    salvar_arquivo("usuarios.txt", usuarios)
    
    print('Conta criada com sucesso!')

def entrar_sistema():
    user_digitado = input('Usuário: ')
    senha_digitada = input('Senha: ')

    usuarios = ler_arquivo("usuarios.txt")
    for linha in usuarios:
        user_banco, senha_banco, tipo_conta = linha[0], linha[1], linha[2]

        if user_banco == user_digitado and senha_banco == senha_digitada:
            print('Acesso liberado!')
            return {"nome": user_digitado, "admin": tipo_conta == "1"}

    return None # Caso não encontre a combinação

# ==========================================
# PAINEL ADMINISTRADOR (Exigência para Duplas)
# ==========================================

def painel_admin():
    while True:
        print("\n=== PAINEL DE CONTROLE (ADMINISTRADOR) ===")
        print("1. Cadastrar vídeo no sistema")
        print("2. Excluir vídeo do sistema")
        print("3. Consultar todos os usuários")
        print("4. Ver estatísticas do sistema (Top 5)")
        print("0. Sair da conta")

        decisao = input("Sua escolha: ")

        if decisao == "1":
            titulo = input("Título do novo vídeo: ")
            desc = input("Descrição: ")
            vids = ler_arquivo("videos.txt")
            vids.append([titulo, desc])
            salvar_arquivo("videos.txt", vids)
            print("Vídeo cadastrado com sucesso!")
            
        elif decisao == "2":
            titulo = input("Qual vídeo deseja excluir? ")
            vids = ler_arquivo("videos.txt")
            vids_atualizado = [v for v in vids if v[0] != titulo]
            salvar_arquivo("videos.txt", vids_atualizado)
            print("Vídeo excluído (caso existisse)!")
            
        elif decisao == "3":
            print("\n--- USUÁRIOS CADASTRADOS ---")
            for u in ler_arquivo("usuarios.txt"): 
                tipo = "Administrador" if u[2] == "1" else "Comum"
                print(f"User: {u[0]} | Tipo: {tipo}")
                
        elif decisao == "4":
            gerar_estatisticas()
            
        elif decisao == "0":
            break

def gerar_estatisticas():
    usuarios = ler_arquivo("usuarios.txt")
    videos = ler_arquivo("videos.txt")
    likes = ler_arquivo("likes.txt")
    
    print("\n--- ESTATÍSTICAS FEltv ---")
    print(f"Total de usuários cadastrados: {len(usuarios)}")
    print(f"Total de vídeos cadastrados: {len(videos)}")
    
    print("\n🏆 TOP 5 VÍDEOS MAIS CURTIDOS 🏆")
    # Organiza a lista de likes do maior pro menor
    ranking = sorted(likes, key=lambda x: int(x[1]), reverse=True)
    for i, (nome, qtd) in enumerate(ranking[:5], 1):
        print(f"{i}º lugar: {nome} ({qtd} likes)")

# ==========================================
# PAINEL USUÁRIO COMUM
# ==========================================

def painel_principal(usuario):
    while True:
        print(f"\n=== PAINEL DO USUÁRIO: {usuario['nome']} ===")
        print("1. Pesquisar vídeo")
        print("2. Ver histórico de buscas")
        print("3. Dar like em vídeo")
        print("4. Tirar like de vídeo")
        print("5. Gerenciar Playlists de favoritos")
        print("6. Sair da conta")

        decisao = input("Sua escolha: ")

        if decisao == "1":
            pesquisar_conteudo(usuario['nome'])
        elif decisao == "2":
            exibir_historico(usuario['nome'])
        elif decisao == "3":
             dar_like()
        elif decisao == "4":
             remover_like()
        elif decisao == '5':
             painel_favoritos(usuario['nome'])
        elif decisao == '6':
             print("Deslogando...")
             break
        else:
            print("Opção não reconhecida.")

def pesquisar_conteudo(nome_user):
    termo_busca = input("O que você deseja assistir? ").lower()
    videos_db = ler_arquivo("videos.txt")
    historico_db = ler_arquivo("historico.txt")
    video_achado = False

    for linha in videos_db:
        titulo, info = linha[0], linha[1]

        # Verifica se a palavra pesquisada está no título (tudo em minúsculo pq eh mais facil)
        if termo_busca in titulo.lower():
            print(f"-> {titulo} | {info}")
            # Salva o resultado no histórico de buscas no arquivo TXT
            historico_db.append([nome_user, titulo, info])
            video_achado = True

    salvar_arquivo("historico.txt", historico_db)

    # Se terminar de ler o arquivo e a variável ainda for False, avisa o usuário
    if not video_achado:
        print("Não encontramos resultados para sua busca.")

def exibir_historico(nome_user):
    historico_db = ler_arquivo("historico.txt")
    # Filtra apenas o histórico do usuário logado no momento
    meu_historico = [h for h in historico_db if h[0] == nome_user]
    
    if not meu_historico:
        print("Seu histórico de buscas está vazio.")  
    else:
        print("\n=== SEU HISTÓRICO ===")
        # O >>enumerate<< cria um contador 'posicao' que começa do número 1
        for posicao, linha in enumerate(meu_historico, 1):  
            print(f"{posicao}) {linha[1]} - {linha[2]}")

def dar_like():
    titulo_alvo = input("Digite exatamente o nome do vídeo que deseja dar like: ")
    likes_db = ler_arquivo("likes.txt")
    
    encontrado = False
    for l in likes_db:
        if l[0] == titulo_alvo:
            l[1] = str(int(l[1]) + 1) # Soma 1 like
            encontrado = True
            break
            
    if not encontrado:
        # Se o vídeo nunca tomou like, cria o registro dele com 1 like
        likes_db.append([titulo_alvo, "1"])
        
    salvar_arquivo("likes.txt", likes_db)
    print("Like registrado com sucesso!")

def remover_like():
    titulo_alvo = input("Digite exatamente o nome do vídeo para remover o like: ")
    likes_db = ler_arquivo("likes.txt")
    
    for l in likes_db:
        if l[0] == titulo_alvo and int(l[1]) > 0:
            l[1] = str(int(l[1]) - 1) # Tira 1 like
            salvar_arquivo("likes.txt", likes_db)
            print("Like removido!")
            return
            
    print("Este vídeo não possui likes ou não foi encontrado.")  

def painel_favoritos(nome_user):
    while True:
        print("\n=== SUAS PLAYLISTS DE FAVORITOS ===")
        print("1. Criar nova Playlist")
        print("2. Ver minhas Playlists e Vídeos")
        print("3. Salvar vídeo em uma Playlist")
        print("4. Excluir vídeo de uma Playlist")
        print("0. Voltar ao painel anterior")

        decisao = input("Sua escolha: ")

        if decisao == "1":
            nome_pl = input("Qual o nome da nova playlist? ")
            playlists_db = ler_arquivo("playlists.txt")
            playlists_db.append([nome_user, nome_pl])
            salvar_arquivo("playlists.txt", playlists_db)
            print("Playlist criada!")
            
        elif decisao == "2":
            print("\n--- LISTA DE FAVORITOS ---")
            pls_db = ler_arquivo("playlists.txt")
            favs_db = ler_arquivo("favoritos_videos.txt")
            
            # Pega as playlists apenas desse usuário
            minhas_pls = [p[1] for p in pls_db if p[0] == nome_user]
            for pl in minhas_pls:
                print(f"\n📂 Playlist: {pl}")
                for f in favs_db:
                    if f[0] == nome_user and f[1] == pl:
                        print(f"   ▶ {f[2]}")
                        
        elif decisao == "3":
            nome_pl = input("Nome da Playlist destino: ")
            nome_vid = input("Nome do Vídeo: ")
            favs_db = ler_arquivo("favoritos_videos.txt")
            favs_db.append([nome_user, nome_pl, nome_vid])
            salvar_arquivo("favoritos_videos.txt", favs_db)
            print("Vídeo salvo na playlist!")
            
        elif decisao == "4":
            nome_pl = input("Nome da Playlist: ")
            nome_vid = input("Nome do Vídeo para remover: ")
            favs_db = ler_arquivo("favoritos_videos.txt")
            # Salva no TXT tudo, MENOS o vídeo que a pessoa quer apagar
            favs_novo = [f for f in favs_db if not (f[0] == nome_user and f[1] == nome_pl and f[2] == nome_vid)]
            salvar_arquivo("favoritos_videos.txt", favs_novo)
            print("Vídeo excluído da lista!")
            
        elif decisao == "0":
            break
        else:
            print("Comando inválido.")

# ==========================================
# INÍCIO DO PROGRAMA
# ==========================================
# ADENDO A MIM MESMO: A função tela_acesso() prende o usuário até que ele faça o login ou saia 
# Quando logar, o dicionário vem para a variável conta_ativa e o programa segue

conta_ativa = tela_acesso()
print(f"Olá, {conta_ativa['nome']}! Que bom ver você por aqui.")

# Direciona para o menu correto dependendo de quem logou
if conta_ativa['admin']:
    painel_admin()
else:
    painel_principal(conta_ativa)