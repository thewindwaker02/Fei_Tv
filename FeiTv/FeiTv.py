import os

# Variável global para controlar qual usuário está logado no momento
usuario_logado = ""

# ==========================================
# 1. LOGIN E CADASTRO
# ==========================================

def novo_cadastro():
    nome = input("Informe um nome de usuário: ")
    senha = input("Crie uma senha: ")

    # Cria o arquivo vazio caso seja a primeira vez rodando o sistema
    if os.path.exists("usuarios.txt") == False:
        arq = open("usuarios.txt", "w", encoding="utf-8")
        arq.close()

    arq = open("usuarios.txt", "r", encoding="utf-8")
    linhas = arq.readlines()
    arq.close()

    usuario_existe = 0
    for l in linhas:
        l = l.strip() # Remove o \n do final da linha para não quebrar a comparação
        pedacos = l.split(",") # Separa o texto na vírgula e transforma numa lista
        if pedacos[0] == nome:
            usuario_existe = 1

    if usuario_existe == 1:
        print("Erro: Este nome de usuário já existe!")
    if usuario_existe == 0:
        # Abre em modo 'a' (append) para adicionar no final do txt sem apagar o resto
        arq2 = open("usuarios.txt", "a", encoding="utf-8")
        arq2.write(nome + "," + senha + "\n")
        arq2.close()
        print("Conta cadastrada com sucesso!")

def entrar_sistema():
    global usuario_logado
    nome = input("Usuário: ")
    senha = input("Senha: ")

    if os.path.exists("usuarios.txt") == False:
        print("Nenhum usuario cadastrado ainda no sistema.")
        return 0

    arq = open("usuarios.txt", "r", encoding="utf-8")
    linhas = arq.readlines()
    arq.close()

    logou = 0
    for l in linhas:
        l = l.strip()
        pedacos = l.split(",")
        if pedacos[0] == nome:
            if pedacos[1] == senha:
                logou = 1
                usuario_logado = nome

    if logou == 1:
        print("\nLogin realizado com sucesso! Bem-vindo(a) " + usuario_logado)
        return 1 # Retorna 1 para avisar o menu principal que o login deu certo
    else:
        print("Usuário ou senha incorretos!\n")
        return 0

# ==========================================
# 2. BUSCAR E LISTAR VÍDEOS
# ==========================================

def pesquisar_conteudo():
    global usuario_logado
    busca = input("O que você deseja buscar? ")
    
    if os.path.exists("videos.txt") == False:
        print("Arquivo videos.txt não existe.")
        return

    arq = open("videos.txt", "r", encoding="utf-8")
    linhas = arq.readlines()
    arq.close()

    achou = 0
    print("\nResultados da Busca:")
    for l in linhas:
        l = l.strip()
        pedacos = l.split(",")
        if len(pedacos) >= 2:
            titulo = pedacos[0]
            descricao = pedacos[1]
            
            # Converte tudo para minúsculo para a busca não dar erro de Case Sensitive
            if busca.lower() in titulo.lower():
                print("- " + titulo + ": " + descricao)
                achou = 1
                
                if os.path.exists("historico.txt") == False:
                    arq2 = open("historico.txt", "w", encoding="utf-8")
                    arq2.close()
                
                arq3 = open("historico.txt", "a", encoding="utf-8")
                arq3.write(usuario_logado + "," + titulo + "," + descricao + "\n")
                arq3.close()

    if achou == 0:
        print("Nenhum resultado para essa pesquisa.")

def exibir_historico():
    global usuario_logado
    
    if os.path.exists("historico.txt") == False:
        print("\nVocê ainda não buscou nenhum vídeo.")
        return
        
    arq = open("historico.txt", "r", encoding="utf-8")
    linhas = arq.readlines()
    arq.close()
    
    contador = 1 # Usado apenas para enumerar os itens na tela de forma amigável
    achou_algo = 0
    print("\n=== INFORMAÇÕES DE VÍDEOS BUSCADOS ===")
    
    for l in linhas:
        l = l.strip()
        pedacos = l.split(",")
        if pedacos[0] == usuario_logado:
            print(str(contador) + ") Título: " + pedacos[1] + " | Descrição: " + pedacos[2])
            contador = contador + 1
            achou_algo = 1
            
    if achou_algo == 0:
        print("Nenhum vídeo buscado ainda.")

# ==========================================
# 3. CURTIR E DESCURTIR
# ==========================================

def interagir_likes():
    titulo_alvo = input("Digite o nome exato do vídeo para curtir/descurtir: ")
    
    if os.path.exists("likes.txt") == False:
        arq = open("likes.txt", "w", encoding="utf-8")
        arq.close()
        
    arq = open("likes.txt", "r", encoding="utf-8")
    linhas = arq.readlines()
    arq.close()
    
    achou = 0
    novas_linhas = []
    
    for l in linhas:
        l = l.strip()
        if l == "":
            continue
            
        pedacos = l.split(",")
        if pedacos[0].lower() == titulo_alvo.lower():
            achou = 1
            curtidas = int(pedacos[1])
            print("O vídeo '" + pedacos[0] + "' possui " + str(curtidas) + " curtida(s).")
            op = input("Deseja: [1] Curtir | [2] Descurtir | [0] Voltar: ")
            
            if op == "1":
                curtidas = curtidas + 1
                print("Curtida registrada!")
            if op == "2":
                # Condição para não deixar as curtidas ficarem negativas
                if curtidas > 0:
                    curtidas = curtidas - 1
                    print("Curtida removida!")
                else:
                    print("O vídeo já tem 0 curtidas.")
                    
            novas_linhas.append(pedacos[0] + "," + str(curtidas))
        else:
            # Mantém a linha inalterada na lista
            novas_linhas.append(pedacos[0] + "," + pedacos[1])
            
    if achou == 0:
        print("Este vídeo ainda não recebeu curtidas.")
        escolha = input("Deseja dar o primeiro like? (s/n): ")
        if escolha == "s" or escolha == "S":
            novas_linhas.append(titulo_alvo + ",1")
            print("Curtida registrada!")
            
    # Sobrescreve o arquivo inteiro com as novas informações
    arq_w = open("likes.txt", "w", encoding="utf-8")
    for linha_nova in novas_linhas:
        arq_w.write(linha_nova + "\n")
    arq_w.close()

# ==========================================
# 4. GERENCIAR FAVORITOS (PLAYLISTS)
# ==========================================

def painel_favoritos():
    global usuario_logado
    rodando_playlist = 1
    
    while rodando_playlist == 1:
        print("\n--- GERENCIAR PLAYLISTS DE FAVORITOS ---")
        print("1. Criar nova Playlist")
        print("2. Editar (Renomear) uma Playlist")
        print("3. Ver minhas Playlists e vídeos")
        print("4. Adicionar vídeo a uma Playlist")
        print("5. Remover vídeo de uma Playlist")
        print("6. Apagar Playlist inteira")
        print("0. Voltar ao Menu Principal")

        decisao = input("Escolha: ")

        if decisao == "1":
            nome_pl = input("Nome da nova playlist: ")
            if os.path.exists("playlists.txt") == False:
                arq = open("playlists.txt", "w")
                arq.close()
            arq2 = open("playlists.txt", "a", encoding="utf-8")
            arq2.write(usuario_logado + "," + nome_pl + "\n")
            arq2.close()
            print("Playlist '" + nome_pl + "' criada com sucesso!")
            
        elif decisao == "2":
            editar_playlist()
        elif decisao == "3":
            listar_playlists()
        elif decisao == "4":
            add_vid_playlist()
        elif decisao == "5":
            rem_vid_playlist()
        elif decisao == "6":
            excluir_playlist_total()
        elif decisao == "0":
            rodando_playlist = 0 
        else:
            print("Opção inválida.")

def editar_playlist():
    global usuario_logado
    antigo = input("Nome atual da playlist que deseja editar: ")
    
    if os.path.exists("playlists.txt") == False:
        print("Você não tem nenhuma playlist para editar.")
        return
        
    arq = open("playlists.txt", "r", encoding="utf-8")
    linhas = arq.readlines()
    arq.close()
    
    achou = 0
    arq_w = open("playlists.txt", "w", encoding="utf-8")
    for l in linhas:
        l = l.strip()
        p = l.split(",")
        if p[0] == usuario_logado and p[1] == antigo:
            if achou == 0:
                novo = input("Digite o novo nome para a playlist: ")
                achou = 1
            arq_w.write(p[0] + "," + novo + "\n")
        else:
            arq_w.write(l + "\n")
    arq_w.close()
    
    if achou == 1:
        # Atualiza o nome da playlist no arquivo de vídeos também para não dar erro
        if os.path.exists("playlist_videos.txt") == True:
            arq_v = open("playlist_videos.txt", "r", encoding="utf-8")
            linhas_v = arq_v.readlines()
            arq_v.close()
            
            arq_vw = open("playlist_videos.txt", "w", encoding="utf-8")
            for v in linhas_v:
                v = v.strip()
                pv = v.split(",")
                if pv[0] == usuario_logado and pv[1] == antigo:
                    arq_vw.write(pv[0] + "," + novo + "," + pv[2] + "\n")
                else:
                    arq_vw.write(v + "\n")
            arq_vw.close()
        print("Playlist renomeada com sucesso!")
    else:
        print("Playlist não encontrada.")

def listar_playlists():
    global usuario_logado
    
    if os.path.exists("playlists.txt") == False:
        print("\nVocê não tem playlists.")
        return
        
    arq = open("playlists.txt", "r", encoding="utf-8")
    linhas_pl = arq.readlines()
    arq.close()
    
    minhas_listas = []
    for l in linhas_pl:
        l = l.strip()
        p = l.split(",")
        if p[0] == usuario_logado:
            minhas_listas.append(p[1])
            
    if len(minhas_listas) == 0:
        print("\nVocê não tem playlists.")
    else:
        linhas_v = []
        if os.path.exists("playlist_videos.txt") == True:
            arq2 = open("playlist_videos.txt", "r", encoding="utf-8")
            linhas_v = arq2.readlines()
            arq2.close()
            
        for pl in minhas_listas:
            print("\nPlaylist: " + pl)
            tem_video = 0
            for v in linhas_v:
                v = v.strip()
                pv = v.split(",")
                if pv[0] == usuario_logado and pv[1] == pl:
                    print("   - " + pv[2])
                    tem_video = 1
            if tem_video == 0:
                print("   (Vazia)")

def add_vid_playlist():
    global usuario_logado
    pl = input("Nome da Playlist: ")
    vid = input("Nome do Vídeo que deseja adicionar: ")
    
    if os.path.exists("playlist_videos.txt") == False:
        arq = open("playlist_videos.txt", "w")
        arq.close()
        
    arq2 = open("playlist_videos.txt", "a", encoding="utf-8")
    arq2.write(usuario_logado + "," + pl + "," + vid + "\n")
    arq2.close()
    print("Vídeo adicionado!")

def rem_vid_playlist():
    global usuario_logado
    pl = input("Nome da Playlist: ")
    vid = input("Nome do Vídeo que deseja remover: ")
    
    if os.path.exists("playlist_videos.txt") == False:
        print("Nenhum video salvo em playlists ainda.")
        return
        
    arq = open("playlist_videos.txt", "r", encoding="utf-8")
    linhas = arq.readlines()
    arq.close()
    
    apagou = 0
    arq_w = open("playlist_videos.txt", "w", encoding="utf-8")
    for l in linhas:
        l = l.strip()
        p = l.split(",")
        if p[0] == usuario_logado and p[1] == pl and p[2] == vid:
            apagou = 1
        else:
            arq_w.write(l + "\n")
    arq_w.close()
    
    if apagou == 1:
        print("Vídeo removido da lista!")
    else:
        print("Vídeo não encontrado.")

def excluir_playlist_total():
    global usuario_logado
    pl = input("Nome da Playlist para apagar: ")
    
    if os.path.exists("playlists.txt") == True:
        arq = open("playlists.txt", "r", encoding="utf-8")
        linhas = arq.readlines()
        arq.close()
        
        apagou = 0
        arq_w = open("playlists.txt", "w", encoding="utf-8")
        for l in linhas:
            l = l.strip()
            p = l.split(",")
            if p[0] == usuario_logado and p[1] == pl:
                apagou = 1
            else:
                arq_w.write(l + "\n")
        arq_w.close()
        
        if apagou == 1:
            print("Playlist excluída com sucesso!")
            
            # Limpa os vídeos que pertenciam a essa playlist do outro arquivo
            if os.path.exists("playlist_videos.txt") == True:
                arq2 = open("playlist_videos.txt", "r", encoding="utf-8")
                linhas_v = arq2.readlines()
                arq2.close()
                
                arq2_w = open("playlist_videos.txt", "w", encoding="utf-8")
                for v in linhas_v:
                    v = v.strip()
                    pv = v.split(",")
                    if pv[0] == usuario_logado and pv[1] == pl:
                        pass 
                    else:
                        arq2_w.write(v + "\n")
                arq2_w.close()
        else:
            print("Playlist não encontrada.")

# ==========================================
# MESTRE DO PROGRAMA (O LOOP PRINCIPAL)
# ==========================================

# Loop principal que mantém o programa rodando até o usuário escolher Encerrar
rodando_programa = 1

while rodando_programa == 1:
    print("\n=== FEltv - ACESSO ===")
    print("1. Fazer Login")
    print("2. Cadastrar Novo Usuário")
    print("3. Encerrar")

    decisao = input("Sua escolha: ")

    if decisao == "1":
        deu_certo = entrar_sistema()
        if deu_certo == 1:
            rodando_painel = 1
            while rodando_painel == 1:
                print("\n=== FEltv - MENU PRINCIPAL (Usuário: " + usuario_logado + ") ===")
                print("1. Buscar vídeo por nome")
                print("2. Listar informações de vídeos buscados")
                print("3. Curtir e descurtir vídeos")
                print("4. Gerenciar favoritos (Playlists)")
                print("5. Sair (Logout)")

                escolha_painel = input("Sua escolha: ")

                if escolha_painel == "1":
                    pesquisar_conteudo()
                elif escolha_painel == "2":
                    exibir_historico()
                elif escolha_painel == "3":
                     interagir_likes()
                elif escolha_painel == "4":
                     painel_favoritos()
                elif escolha_painel == "5":
                     print("Saindo da conta...")
                     rodando_painel = 0
                else:
                    print("Opção não reconhecida.")

    elif decisao == "2":
        novo_cadastro()
    elif decisao == "3":
        print("Fechando o sistema...")
        rodando_programa = 0
    else:
        print("Opção inválida! Tente novamente.")