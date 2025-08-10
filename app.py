# import pygame
# from random import randrange
# import os
# import time

# # ---------------- CONFIGURAÇÕES ---------------- #
# LARGURA, ALTURA = 600, 600
# FPS = 60
# ARQUIVO_RECORDE = "recorde.txt"

# # Timers para a sequência em milissegundos
# TEMPO_LUZ_ACESA = 600
# TEMPO_LUZ_APAGADA = 200
# TEMPO_ESPERA_INICIAL = 800

# # Cores
# PRETO, CINZA, BRANCO = (0,0,0), (100,100,100), (255,255,255)
# VERDE_CLARO, VERDE_ESCURO = (100,255,100), (0,200,0)
# VERMELHO_CLARO, VERMELHO_ESCURO = (255,100,100), (200,0,0)
# AMARELO_CLARO, AMARELO_ESCURO = (255,255,150), (255,255,0)
# AZUL_CLARO, AZUL_ESCURO = (150,150,255), (0,0,255)
# CORES_ESCURO = [VERDE_ESCURO, VERMELHO_ESCURO, AMARELO_ESCURO, AZUL_ESCURO]
# CORES_CLARO = [VERDE_CLARO, VERMELHO_CLARO, AMARELO_CLARO, AZUL_CLARO]

# # ---------------- INICIALIZAÇÃO DO PYGAME ---------------- #
# pygame.init()
# pygame.mixer.init()
# window = pygame.display.set_mode((LARGURA, ALTURA))
# pygame.display.set_caption("Micro Genius")
# fonte = pygame.font.SysFont("Comic Sans MS", 30)
# clock = pygame.time.Clock()

# try:
#     sons = [
#         pygame.mixer.Sound("sons/som_verde.wav"), pygame.mixer.Sound("sons/som_vermelho.wav"),
#         pygame.mixer.Sound("sons/som_amarelo.wav"), pygame.mixer.Sound("sons/som_azul.wav")
#     ]
# except pygame.error:
#     print("Aviso: Arquivos de som não encontrados. O jogo rodará sem som.")
#     class SomFalso:
#         def play(self): pass
#     sons = [SomFalso(), SomFalso(), SomFalso(), SomFalso()]

# # ---------------- FUNÇÕES AUXILIARES ---------------- #
# def carregar_recorde():
#     if not os.path.exists(ARQUIVO_RECORDE): return 0
#     with open(ARQUIVO_RECORDE, "r") as f:
#         try: return int(f.read().strip())
#         except: return 0
# def salvar_recorde(r):
#     with open(ARQUIVO_RECORDE, "w") as f: f.write(str(r))
# def tocar_som(index): sons[index].play()

# def desenhar_tela(pontos, recorde, cor_ativa=None, hover_centro=False, msg=None):
#     window.fill(BRANCO)
#     cores_a_usar = CORES_ESCURO.copy()
#     if cor_ativa is not None:
#         cores_a_usar[cor_ativa] = CORES_CLARO[cor_ativa]

#     pygame.draw.rect(window, cores_a_usar[0], (100, 100, 200, 200))
#     pygame.draw.rect(window, cores_a_usar[1], (300, 100, 200, 200))
#     pygame.draw.rect(window, cores_a_usar[2], (100, 300, 200, 200))
#     pygame.draw.rect(window, cores_a_usar[3], (300, 300, 200, 200))
#     pygame.draw.rect(window, PRETO, (100, 300, 400, 10))
#     pygame.draw.rect(window, PRETO, (300, 100, 10, 400))
#     pygame.draw.circle(window, BRANCO, (300, 300), 300, 100)

#     if hover_centro:
#         pygame.draw.circle(window, CINZA, (300, 300), 80)
#     else:
#         pygame.draw.circle(window, PRETO, (300, 300), 90)

#     texto_central = fonte.render("Micro Genius", True, BRANCO)
#     window.blit(texto_central, texto_central.get_rect(center=(300, 305)))
    
#     texto_pontos = fonte.render(f"Pontos: {pontos}", True, PRETO)
#     texto_recorde = fonte.render(f"Recorde: {recorde}", True, PRETO)
#     window.blit(texto_pontos, (10, 10))
#     window.blit(texto_recorde, (LARGURA - texto_recorde.get_width() - 10, 10))
    
#     if msg:
#         texto_msg = fonte.render(msg, True, PRETO)
#         window.blit(texto_msg, texto_msg.get_rect(center=(LARGURA / 2, ALTURA - 50)))

# def get_cor_pela_pos(pos):
#     dist_centro = ((pos[0] - 300) ** 2 + (pos[1] - 300) ** 2) ** 0.5
#     if dist_centro <= 90: return "centro"
#     if 210 > dist_centro > 90:
#         if 100 < pos[0] < 300 and 100 < pos[1] < 300: return 0
#         if 300 < pos[0] < 500 and 100 < pos[1] < 300: return 1
#         if 100 < pos[0] < 300 and 300 < pos[1] < 500: return 2
#         if 300 < pos[0] < 500 and 300 < pos[1] < 500: return 3
#     return None

# # ---------------- LÓGICA PRINCIPAL DO JOGO ---------------- #
# def game_loop():
#     rodando = True
#     recorde = carregar_recorde()
#     sequencia, resposta_jogador = [], []
#     estado = "INICIO"
    
#     # --- Variáveis de controle para a sequência não-bloqueante ---
#     indice_da_sequencia = 0
#     tempo_proxima_acao = 0
#     luz_acesa = False

#     while rodando:
#         clock.tick(FPS)
#         agora = pygame.time.get_ticks()
        
#         # --- PROCESSAMENTO DE EVENTOS ---
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 rodando = False
            
#             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                 if estado == "INICIO":
#                     if get_cor_pela_pos(event.pos) == "centro":
#                         estado = "MOSTRANDO"
#                         sequencia = [randrange(4)]
#                         resposta_jogador = []
#                         indice_da_sequencia = 0
#                         tempo_proxima_acao = agora + TEMPO_ESPERA_INICIAL
#                 elif estado == "JOGANDO":
#                     cor_clicada = get_cor_pela_pos(event.pos)
#                     if isinstance(cor_clicada, int):
#                         tocar_som(cor_clicada)
#                         resposta_jogador.append(cor_clicada)
#                         if resposta_jogador[-1] != sequencia[len(resposta_jogador)-1]:
#                             estado = "FIM_DE_JOGO"
#                         elif len(resposta_jogador) == len(sequencia):
#                             estado = "MOSTRANDO"
#                             sequencia.append(randrange(4))
#                             resposta_jogador = []
#                             indice_da_sequencia = 0
#                             tempo_proxima_acao = agora + TEMPO_ESPERA_INICIAL
        
#         # --- LÓGICA DE ATUALIZAÇÃO E DESENHO ---
        
#         cor_ativa_desenho = None
#         mensagem_tela = None

#         if estado == "INICIO":
#             mouse_pos = pygame.mouse.get_pos()
#             hover_centro = get_cor_pela_pos(mouse_pos) == "centro"
#             desenhar_tela(0, recorde, hover_centro=hover_centro, msg="Clique no centro para iniciar!")
        
#         elif estado == "MOSTRANDO":
#             pontos = len(sequencia)
#             if agora > tempo_proxima_acao:
#                 if luz_acesa: # Se a luz estava acesa, apaga
#                     luz_acesa = False
#                     indice_da_sequencia += 1
#                     tempo_proxima_acao = agora + TEMPO_LUZ_APAGADA
#                 else: # Se estava apagada, acende a próxima (ou termina)
#                     if indice_da_sequencia < len(sequencia):
#                         luz_acesa = True
#                         cor_para_mostrar = sequencia[indice_da_sequencia]
#                         tocar_som(cor_para_mostrar)
#                         tempo_proxima_acao = agora + TEMPO_LUZ_ACESA
#                     else: # Acabou a sequência
#                         estado = "JOGANDO"
            
#             if luz_acesa:
#                 cor_ativa_desenho = sequencia[indice_da_sequencia]
            
#             desenhar_tela(pontos, recorde, cor_ativa=cor_ativa_desenho)

#         elif estado == "JOGANDO":
#             mouse_pos = pygame.mouse.get_pos()
#             cor_hover = get_cor_pela_pos(mouse_pos)
#             cor_ativa_desenho = cor_hover if isinstance(cor_hover, int) else None
#             desenhar_tela(len(sequencia), recorde, cor_ativa=cor_ativa_desenho)

#         elif estado == "FIM_DE_JOGO":
#             pontos = len(sequencia) - 1
#             if pontos > recorde:
#                 recorde = pontos
#                 salvar_recorde(recorde)
            
#             desenhar_tela(pontos, recorde, msg=f"Fim de Jogo! Pontos: {pontos}")
#             pygame.display.update()
#             pygame.time.wait(3000)
            
#             estado = "INICIO"
#             sequencia, resposta_jogador = [], []

#         pygame.display.update()

#     pygame.quit()

# # -------------------------------------- INICIA O JOGO -------------------------------
# if __name__ == "__main__":
#     game_loop()

import pygame
from random import randrange
import os
import time
from pathlib import Path  # <-- 1. Importa a biblioteca

print("[DEBUG] app.py IMPORTADO COM SUCESSO")

# ---------------- CONFIGURAÇÕES ---------------- #
LARGURA, ALTURA = 600, 600
FPS = 60

# --- CAMINHOS DE ARQUIVO ROBUSTOS ---
# Define o diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_RECORDE = BASE_DIR / "recorde.txt" # <-- 2. Usa o caminho base

TEMPO_LUZ_ACESA = 600
TEMPO_LUZ_APAGADA = 200
TEMPO_ESPERA_INICIAL = 800

# Cores
PRETO, CINZA, BRANCO = (0,0,0), (100,100,100), (255,255,255)
VERDE_CLARO, VERDE_ESCURO = (100,255,100), (0,200,0)
VERMELHO_CLARO, VERMELHO_ESCURO = (255,100,100), (200,0,0)
AMARELO_CLARO, AMARELO_ESCURO = (255,255,150), (255,255,0)
AZUL_CLARO, AZUL_ESCURO = (150,150,255), (0,0,255)
CORES_ESCURO = [VERDE_ESCURO, VERMELHO_ESCURO, AMARELO_ESCURO, AZUL_ESCURO]
CORES_CLARO = [VERDE_CLARO, VERMELHO_CLARO, AMARELO_CLARO, AZUL_CLARO]

# ---------------- INICIALIZAÇÃO DO PYGAME ---------------- #
pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Micro Genius")
fonte = pygame.font.SysFont("Comic Sans MS", 30)
clock = pygame.time.Clock()

try:
    # <-- 3. Usa o caminho base para os sons
    sons = [
        pygame.mixer.Sound(BASE_DIR / "sons" / "som_verde.wav"),
        pygame.mixer.Sound(BASE_DIR / "sons" / "som_vermelho.wav"),
        pygame.mixer.Sound(BASE_DIR / "sons" / "som_amarelo.wav"),
        pygame.mixer.Sound(BASE_DIR / "sons" / "som_azul.wav")
    ]
except pygame.error:
    print("Aviso: Arquivos de som não encontrados. O jogo rodará sem som.")
    class SomFalso:
        def play(self): pass
    sons = [SomFalso(), SomFalso(), SomFalso(), SomFalso()]

# ---------------- FUNÇÕES AUXILIARES ---------------- #
# (O resto das funções não muda)
def carregar_recorde():
    if not os.path.exists(ARQUIVO_RECORDE): return 0
    with open(ARQUIVO_RECORDE, "r") as f:
        try: return int(f.read().strip())
        except: return 0
def salvar_recorde(r):
    with open(ARQUIVO_RECORDE, "w") as f: f.write(str(r))
def tocar_som(index): sons[index].play()

def desenhar_tela(pontos, recorde, cor_ativa=None, hover_centro=False, msg=None):
    window.fill(BRANCO)
    cores_a_usar = CORES_ESCURO.copy()
    if cor_ativa is not None:
        cores_a_usar[cor_ativa] = CORES_CLARO[cor_ativa]

    pygame.draw.rect(window, cores_a_usar[0], (100, 100, 200, 200))
    pygame.draw.rect(window, cores_a_usar[1], (300, 100, 200, 200))
    pygame.draw.rect(window, cores_a_usar[2], (100, 300, 200, 200))
    pygame.draw.rect(window, cores_a_usar[3], (300, 300, 200, 200))
    pygame.draw.rect(window, PRETO, (100, 300, 400, 10))
    pygame.draw.rect(window, PRETO, (300, 100, 10, 400))
    pygame.draw.circle(window, BRANCO, (300, 300), 300, 100)

    if hover_centro:
        pygame.draw.circle(window, CINZA, (300, 300), 80)
    else:
        pygame.draw.circle(window, PRETO, (300, 300), 90)

    texto_central = fonte.render("Micro Genius", True, BRANCO)
    window.blit(texto_central, texto_central.get_rect(center=(300, 305)))
    
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, PRETO)
    texto_recorde = fonte.render(f"Recorde: {recorde}", True, PRETO)
    window.blit(texto_pontos, (10, 10))
    window.blit(texto_recorde, (LARGURA - texto_recorde.get_width() - 10, 10))
    
    if msg:
        texto_msg = fonte.render(msg, True, PRETO)
        window.blit(texto_msg, texto_msg.get_rect(center=(LARGURA / 2, ALTURA - 50)))

def get_cor_pela_pos(pos):
    dist_centro = ((pos[0] - 300) ** 2 + (pos[1] - 300) ** 2) ** 0.5
    if dist_centro <= 90: return "centro"
    if 210 > dist_centro > 90:
        if 100 < pos[0] < 300 and 100 < pos[1] < 300: return 0
        if 300 < pos[0] < 500 and 100 < pos[1] < 300: return 1
        if 100 < pos[0] < 300 and 300 < pos[1] < 500: return 2
        if 300 < pos[0] < 500 and 300 < pos[1] < 500: return 3
    return None

# ---------------- LÓGICA PRINCIPAL DO JOGO ---------------- #
def game_loop():
    rodando = True
    recorde = carregar_recorde()
    sequencia, resposta_jogador = [], []
    estado = "INICIO"
    
    indice_da_sequencia = 0
    tempo_proxima_acao = 0
    luz_acesa = False

    while rodando:
        clock.tick(FPS)
        agora = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if estado == "INICIO":
                    if get_cor_pela_pos(event.pos) == "centro":
                        estado = "MOSTRANDO"
                        sequencia = [randrange(4)]
                        resposta_jogador = []
                        indice_da_sequencia = 0
                        tempo_proxima_acao = agora + TEMPO_ESPERA_INICIAL
                elif estado == "JOGANDO":
                    cor_clicada = get_cor_pela_pos(event.pos)
                    if isinstance(cor_clicada, int):
                        tocar_som(cor_clicada)
                        resposta_jogador.append(cor_clicada)
                        if resposta_jogador[-1] != sequencia[len(resposta_jogador)-1]:
                            estado = "FIM_DE_JOGO"
                        elif len(resposta_jogador) == len(sequencia):
                            estado = "MOSTRANDO"
                            sequencia.append(randrange(4))
                            resposta_jogador = []
                            indice_da_sequencia = 0
                            tempo_proxima_acao = agora + TEMPO_ESPERA_INICIAL
        
        cor_ativa_desenho = None
        mensagem_tela = None

        if estado == "INICIO":
            mouse_pos = pygame.mouse.get_pos()
            hover_centro = get_cor_pela_pos(mouse_pos) == "centro"
            desenhar_tela(0, recorde, hover_centro=hover_centro, msg="Clique no centro para iniciar!")
        
        elif estado == "MOSTRANDO":
            pontos = len(sequencia)
            if agora > tempo_proxima_acao:
                if luz_acesa:
                    luz_acesa = False
                    indice_da_sequencia += 1
                    tempo_proxima_acao = agora + TEMPO_LUZ_APAGADA
                else:
                    if indice_da_sequencia < len(sequencia):
                        luz_acesa = True
                        cor_para_mostrar = sequencia[indice_da_sequencia]
                        tocar_som(cor_para_mostrar)
                        tempo_proxima_acao = agora + TEMPO_LUZ_ACESA
                    else:
                        estado = "JOGANDO"
            
            if luz_acesa:
                cor_ativa_desenho = sequencia[indice_da_sequencia]
            
            desenhar_tela(pontos, recorde, cor_ativa=cor_ativa_desenho)

        elif estado == "JOGANDO":
            mouse_pos = pygame.mouse.get_pos()
            cor_hover = get_cor_pela_pos(mouse_pos)
            cor_ativa_desenho = cor_hover if isinstance(cor_hover, int) else None
            desenhar_tela(len(sequencia), recorde, cor_ativa=cor_ativa_desenho)

        elif estado == "FIM_DE_JOGO":
            pontos = len(sequencia) - 1
            if pontos > recorde:
                recorde = pontos
                salvar_recorde(recorde)
            
            desenhar_tela(pontos, recorde, msg=f"Fim de Jogo! Pontos: {pontos}")
            pygame.display.update()
            pygame.time.wait(3000)
            
            estado = "INICIO"
            sequencia, resposta_jogador = [], []

        pygame.display.update()

    pygame.quit()

# --- INICIA O JOGO ---
if __name__ == "__main__":
    game_loop()