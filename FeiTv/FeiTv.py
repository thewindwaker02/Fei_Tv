import os # importando a biblioteca os pra mexer com os caminhos dos arquivos no pc

# >>>>PT1 SALVAR<<<<
# (salva pra nao perder dados quando fecha o programa)
# (aula 12 e 13 )

def ler_arquivo(nome_arquivo):
    # se o arquivo nem existe ainda, retorna uma lista p nao travar o codigo
    if not os.path.exists(nome_arquivo):
        return []
    
    lista_de_dados = []
    # o 'r' significa read (leitura)
    with open(nome_arquivo, "r", encoding="utf-8") as f:
        linhas = f.readlines()
        for linha in linhas:
            #botei o utf p n ter erro :D
            # strip tira as quebras de linha inuteis (\n)
            # o split separa a string bonitinho toda vez que acha uma virgula
            item_separado = linha.strip().split(",")
            lista_de_dados.append(item_separado)
            
    return lista_de_dados

def salvar_arquivo(nome_arquivo, dados):
    # o 'w' aqui (write) sobrescreve o arquivo todo com os dados atualizados da memoria
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        for linha in dados:
            # junta os itens da lista de novo colocando uma virgula no meio 
            # pra poder ler certo dps com o split
            linha_texto = ",".join(linha)
            f.write(linha_texto + "\n")

# PT 2 LOGIN E CADASTRO

def tela_acesso():
    # loop infinito pro menu nao fechar do nada
    while True:
        print("\n=== FEltv - ACESSO ===")
        print("1. Fazer Login")
        print("2. Cadastrar Usuário")
        print("3. Encerrar")

        decisao = input("Sua escolha: ")

        if decisao == "1":
            usuario = entrar_sistema()
            if usuario != None:
                return usuario
            else:
                print("Usuário ou senha incorretos!\n")
        elif decisao == "2":
            novo_cadastro()
        elif decisao == "3":
            print("Fechando o sistema...")
            exit()
        else:
            print("Opção inválida!")

def novo_cadastro():
    novo_user = input('Informe um nome de usuário: ')
    nova_senha = input('Crie uma senha: ')

    # puxa todo mundo que ja ta cadastrado no txt
    usuarios = ler_arquivo("usuarios.txt")
    
    # ve se esse usuario ja nao existe (evita conta duplicada)
    ja_existe = False
    for u in usuarios:
        if u[0] == novo_user:
            ja_existe = True
            
    if ja_existe == True:
        print("Erro: Este usuário já existe!")
    else:
        # criao cara novo e joga dentro da lista geral
        nova_linha  = [novo_user, nova_senha]
        usuarios.append(nova_linha)
        salvar_arquivo("usuarios.txt", usuarios)
        print('Conta cadastrada com sucesso!')

def entrar_sistema():
    user_digitado = input('Usuário: ')
    senha_digitada = input('Senha: ')

    usuarios = ler_arquivo("usuarios.txt")
    
    # le linha por linha e ve se bate com as infos do txt
    for linha in usuarios:
        if linha[0] == user_digitado and linha[1] == senha_digitada:
            print('Login realizado com sucesso!')
            return user_digitado

    return None # volta vazio (None) se errar a senha ou o usuario nao existir

# PT 3 MENU E BUSCAS

def painel_principal(usuario):
    while True:
        print(f"\n=== FEltv - MENU PRINCIPAL (Usuário: {usuario}) ===")
        print("1. Buscar vídeo pelo nome")
        print("2. Ver Catálogo Completo")
        print("3. Listar meu histórico de buscas")
        print("4. Curtir ou descurtir um vídeo")
        print("5. Gerenciar Playlists de Favoritos")
        print("6. Sair (Logout)")

        decisao = input("Sua escolha: ")

        if decisao == "1":
            pesquisar_conteudo(usuario)
        elif decisao == "2":
            ver_catalogo()
        elif decisao == "3":
            exibir_historico(usuario)
        elif decisao == "4":
             interagir_likes()
        elif decisao == "5":
             painel_favoritos(usuario)
        elif decisao == '6':
             print("Saindo da conta...")
             break # quebra o ciclo do while e desloga a conta
        else:
            print("Opção não reconhecida.")

def ver_catalogo():
    videos_db = ler_arquivo("videos.txt")
    
    # previne erro caso o arquivo ainda nao tenha sido criado
    if len(videos_db) == 0:
        print("\n[!] O catálogo está vazio ou o arquivo 'videos.txt' não foi encontrado.")
    else:
        print("\n=== CATÁLOGO COMPLETO FEltv ===")
        for linha in videos_db:
            # verifica se tem as duas partes p n crashar
            if len(linha) >= 2:
                print(f"-> {linha[0]} | Descrição: {linha[1]}")
        print("===============================")

def pesquisar_conteudo(nome_user):
    # .lower() transforma tudo em minusculo pq eh mais facil e evita erro de CAPS LOCK
    termo_busca = input("O que você deseja buscar? ").lower()
    videos_db = ler_arquivo("videos.txt")
    historico_db = ler_arquivo("historico.txt")
    video_achado = False

    for linha in videos_db:
        if len(linha) >= 2:
            titulo = linha[0]
            info = linha[1]
            
            # verifica se o q o cara digitou ta dentro do titulo do txt
            if termo_busca in titulo.lower():
                print(f"Encontrado: {titulo} - {info}")
                # bota na lista de historico do usuario pra usar dps
                historico_db.append([nome_user, titulo, info])
                video_achado = True

    # se achou pelo menos um video, ele salva o historico atualizado
    if video_achado == True:
        salvar_arquivo("historico.txt", historico_db)
    else:
        print("Nenhum resultado para essa pesquisa.")

def exibir_historico(nome_user):
    historico_db = ler_arquivo("historico.txt")
    
    meu_historico = []
    # varre o txt inteiro e puxa so o historico de quem ta logado agr
    for h in historico_db:
        if h[0] == nome_user:
            meu_historico.append(h)
    
    if len(meu_historico) == 0:
        print("Você ainda não realizou buscas.")  
    else:
        print(f"\n=== HISTÓRICO DE {nome_user.upper()} ===")
        contador = 1
        for linha in meu_historico:  
            print(f"{contador}) {linha[1]}")
            contador += 1 # contador pra ir listando tipo 1, 2, 3...

# LIKES E DESLIKES 

def interagir_likes():
    titulo_alvo = input("Digite o nome exato do vídeo: ")
    likes_db = ler_arquivo("likes.txt")
    
    encontrado = False
    for l in likes_db:
        # compara em minusculo tbm pra evitar erro de digitacao
        if l[0].lower() == titulo_alvo.lower():
            encontrado = True
            print(f"O vídeo '{l[0]}' possui {l[1]} curtida(s).")
            op = input("Deseja: [1] Curtir | [2] Descurtir | [0] Voltar: ")
            
            if op == "1":
                # tem q virar int(numero) primeiro pra conseguir somar 1 
                # dps volta pra string(texto) pq txt so aceita texto
                l[1] = str(int(l[1]) + 1)
                print("Curtida registrada!")
            elif op == "2":
                if int(l[1]) > 0:
                    l[1] = str(int(l[1]) - 1) # tira 1 like
                    print("Curtida removida!")
            break
            
    # se o video nunca teve like na vida, o programa cria o registro dele aqui memo
    if encontrado == False:
        print("Este vídeo ainda não recebeu curtidas no sistema.")
        primeiro_like = input("Dar o primeiro like? (s/n): ").lower()
        if primeiro_like == 's':
            # cria com 1 curtida de cara
            likes_db.append([titulo_alvo, "1"])
            print("Curtida registrada!")
        
    # salva no fim de tudo
    salvar_arquivo("likes.txt", likes_db)

#PLAYLIST DE FAVORITOS

def painel_favoritos(nome_user):
    while True:
        print("\n--- GERENCIAR PLAYLISTS ---")
        print("1. Criar nova Playlist")
        print("2. Renomear uma Playlist")
        print("3. Ver minhas Playlists e vídeos")
        print("4. Adicionar vídeo a uma Playlist")
        print("5. Remover vídeo de uma Playlist")
        print("6. Apagar Playlist inteira")
        print("0. Voltar")

        decisao = input("Escolha: ")

        if decisao == "1":
            nome_pl = input("Nome da lista: ")
            pls = ler_arquivo("playlists.txt")
            nova_pl = [nome_user, nome_pl]
            pls.append(nova_pl)
            salvar_arquivo("playlists.txt", pls)
            print("Playlist criada!")
        elif decisao == "2":
            editar_playlist(nome_user)
        elif decisao == "3":
            listar_playlists(nome_user)
        elif decisao == "4":
            add_vid_playlist(nome_user)
        elif decisao == "5":
            rem_vid_playlist(nome_user)
        elif decisao == "6":
            excluir_playlist_total(nome_user)
        elif decisao == "0":
            break # sai dessa funcao e volta pro menu de antes

def listar_playlists(nome_user):
    pls = ler_arquivo("playlists.txt")
    vids = ler_arquivo("playlist_videos.txt")
    
    minhas_pls = []
    # pega so os nomes das playlists q sao do usuario logado
    for p in pls:
        if p[0] == nome_user:
            minhas_pls.append(p[1])
    
    if len(minhas_pls) == 0:
        print("Você não tem playlists.")
    else:
        for pl in minhas_pls:
            print(f"\n[Playlist]: {pl}")
            for v in vids:
                # mostra so os videos salvos nessa playlist especifica 
                if v[0] == nome_user and v[1] == pl:
                    print(f"   - {v[2]}")

def editar_playlist(nome_user):
    antigo = input("Nome atual da playlist: ")
    pls = ler_arquivo("playlists.txt")
    
    encontrado = False
    for p in pls:
        if p[0] == nome_user and p[1] == antigo:
            novo = input("Novo nome: ")
            p[1] = novo # troca na memoria
            salvar_arquivo("playlists.txt", pls)
            encontrado = True
            
            # ATENCAO: se trocar o nome da playlist, tem q trocar nos videos q 
            # estao vinculados a ela tb, senao buga o sistema todo
            vids = ler_arquivo("playlist_videos.txt")
            for v in vids:
                if v[0] == nome_user and v[1] == antigo:
                    v[1] = novo
            salvar_arquivo("playlist_videos.txt", vids)
            print("Alterado com sucesso!")
            
    if encontrado == False:
        print("Playlist não encontrada.")

def add_vid_playlist(nome_user):
    pl = input("Nome da Playlist: ")
    vid = input("Nome do Vídeo: ")
    vids = ler_arquivo("playlist_videos.txt")
    novo_video = [nome_user, pl, vid]
    vids.append(novo_video)
    salvar_arquivo("playlist_videos.txt", vids)
    print("Vídeo adicionado!")

def rem_vid_playlist(nome_user):
    pl = input("Playlist: ")
    vid = input("Vídeo: ")
    vids = ler_arquivo("playlist_videos.txt")
    
    vids_novo = []
    for v in vids:
        # se NAO for o video que a gnt quer apagar, joga na lista nova.
        # se for, ele ignora e assim o video some.
        if not (v[0] == nome_user and v[1] == pl and v[2] == vid):
            vids_novo.append(v)
            
    salvar_arquivo("playlist_videos.txt", vids_novo)
    print("Vídeo removido da lista (caso existisse)!")

def excluir_playlist_total(nome_user):
    pl = input("Nome da Playlist para apagar: ")
    
    # limpa na lista de playlists e salva sem ela
    pls = ler_arquivo("playlists.txt")
    pls_novo = []
    for p in pls:
        if not (p[0] == nome_user and p[1] == pl):
            pls_novo.append(p)
    salvar_arquivo("playlists.txt", pls_novo)
    
    # tb limpa nos videos q tavam dentro dela
    vids = ler_arquivo("playlist_videos.txt")
    vids_novo = []
    for v in vids:
        if not (v[0] == nome_user and v[1] == pl):
            vids_novo.append(v)
    salvar_arquivo("playlist_videos.txt", vids_novo)
    
    print("Playlist excluída com sucesso!")
# COMEÇO DO PROGRAMA
# ADENDO A MIM MESMO: o while True prende o usuario e o codigo segue rodando

while True:
    usuario_logado = tela_acesso()
    painel_principal(usuario_logado)