import pygame
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura_tela = 600  # Largura reduzida
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Cobra vs Capivaras")

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
cinza = (200, 200, 200)

# Carregar imagens
cobra_imagens = [pygame.image.load(f'cobra_{i}.png').convert_alpha() for i in range(1, 4)]
capivara_imagens = [pygame.image.load(f'capi_{i}.png').convert_alpha() for i in range(1, 4)]

# Redimensionar imagens das capivaras (3x)
capivara_imagens = [pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3)) for img in capivara_imagens]

# Definir a velocidade inicial para as capivaras
VELOCIDADE_CAPIVARA = 4  # Velocidade inicial
VELOCIDADE_AUMENTO = 1.5  # Aumento de 50%

# Classe para a cobra
class Cobra:
    def __init__(self):
        self.imagem_index = 0
        self.imagem = cobra_imagens[self.imagem_index]
        self.rect = self.imagem.get_rect(center=(largura_tela // 2, altura_tela - 100))  # Posiciona mais embaixo
        self.velocidade = 5
        self.frame_count = 0
        self.angulo = 0  # Ângulo de rotação

    def mover(self, direcao):
        if direcao == "esquerda" and self.rect.left > 0:
            self.rect.x -= self.velocidade
        elif direcao == "direita" and self.rect.right < largura_tela:
            self.rect.x += self.velocidade

    def atualizar_imagem(self):
        self.frame_count += 1
        if self.frame_count % 10 == 0:  # Altera a imagem a cada 10 quadros
            self.imagem_index = (self.imagem_index + 1) % len(cobra_imagens)
        
        # Atualiza a imagem rotacionada
        self.imagem = pygame.transform.rotate(cobra_imagens[self.imagem_index], self.angulo)
        self.rect = self.imagem.get_rect(center=self.rect.center)

    def girar(self, sentido):
        if sentido == "direita":
            self.angulo = -30  # Gira para -30 graus (para a direita)
        elif sentido == "esquerda":
            self.angulo = 30  # Gira para 30 graus (para a esquerda)
        else:
            self.angulo = 0  # Retorna para 0 graus

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

# Classe para a capivara
class Capivara:
    def __init__(self, x, y):
        self.imagem_index = 0
        self.imagem = capivara_imagens[self.imagem_index]
        self.rect = self.imagem.get_rect(center=(x, y))
        self.velocidade = VELOCIDADE_CAPIVARA  # Usa a velocidade inicial
        self.frame_count = 0

    def mover(self):
        self.rect.y += self.velocidade

    def atualizar_imagem(self):
        self.frame_count += 1
        if self.frame_count % 10 == 0:  # Altera a imagem a cada 10 quadros
            if self.imagem_index == 2:  # Se está no frame 3, volta para 1
                self.imagem_index = 1
            elif self.imagem_index == 1:  # Se está no frame 2, vai para 3
                self.imagem_index = 2
            else:  # Se está no frame 1, vai para 2
                self.imagem_index = 1
            
            self.imagem = capivara_imagens[self.imagem_index]
            self.rect = self.imagem.get_rect(center=self.rect.center)  # Atualiza o rect

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

# Função para verificar se uma nova capivara pode ser criada na posição
def pode_posicionar(capivaras, nova_rect):
    for capivara in capivaras:
        if capivara.rect.colliderect(nova_rect):
            return False
    return True

# Função para desenhar botões
def desenhar_botao(tela, texto, posicao):
    fonte = pygame.font.SysFont(None, 40)
    texto_surface = fonte.render(texto, True, preto)
    largura_botao = texto_surface.get_width() + 40
    altura_botao = texto_surface.get_height() + 20
    retangulo_botao = pygame.Rect(posicao[0], posicao[1], largura_botao, altura_botao)

    # Desenha o botão
    pygame.draw.rect(tela, cinza, retangulo_botao, border_radius=10)
    tela.blit(texto_surface, (posicao[0] + 20, posicao[1] + 10))

# Tela inicial
def tela_inicial():
    while True:
        tela.fill(branco)
        
        # Título
        fonte_titulo = pygame.font.SysFont(None, 55)
        texto_titulo = fonte_titulo.render("Cobras Vs Capivaras", True, preto)
        tela.blit(texto_titulo, (largura_tela // 2 - texto_titulo.get_width() // 2, altura_tela // 2 - 100))

        # Botões
        botao_jogar_posicao = (largura_tela // 2 - 100, altura_tela // 2 - 25)
        botao_sair_posicao = (largura_tela // 2 - 100, altura_tela // 2 + 35)
        desenhar_botao(tela, "Jogar", botao_jogar_posicao)
        desenhar_botao(tela, "Sair", botao_sair_posicao)

        # Rodapé
        fonte_rodape = pygame.font.SysFont(None, 30)
        texto_rodape = fonte_rodape.render("Criado por Kleber Klaar", True, preto)
        tela.blit(texto_rodape, (largura_tela // 2 - texto_rodape.get_width() // 2, altura_tela - 30))

        pygame.display.flip()

        # Evento de controle
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if (largura_tela // 2 - 100 <= mouse_pos[0] <= largura_tela // 2 + 100) and (altura_tela // 2 - 25 <= mouse_pos[1] <= altura_tela // 2 + 25):
                    return "jogar"  # Se clicar em "Jogar"
                elif (largura_tela // 2 - 100 <= mouse_pos[0] <= largura_tela // 2 + 100) and (altura_tela // 2 + 35 <= mouse_pos[1] <= altura_tela // 2 + 85):
                    pygame.quit()  # Se clicar em "Sair"
                    return

# Tela de Game Over
def tela_game_over(pontuacao):
    while True:
        tela.fill(branco)
        
        # Mensagem de Game Over
        fonte_game_over = pygame.font.SysFont(None, 55)
        texto_game_over = fonte_game_over.render("Game Over!", True, preto)
        tela.blit(texto_game_over, (largura_tela // 2 - texto_game_over.get_width() // 2, altura_tela // 2 - 100))

        # Mensagem com a pontuação
        fonte_pontuacao = pygame.font.SysFont(None, 40)
        texto_pontuacao = fonte_pontuacao.render(f"Você desviou de {pontuacao} capivaras!", True, preto)
        tela.blit(texto_pontuacao, (largura_tela // 2 - texto_pontuacao.get_width() // 2, altura_tela // 2))

        # Botões
        botao_jogar_novamente_posicao = (largura_tela // 2 - 150, altura_tela // 2 + 50)
        botao_sair_posicao = (largura_tela // 2 - 100, altura_tela // 2 + 110)
        desenhar_botao(tela, "Jogar Novamente", botao_jogar_novamente_posicao)
        desenhar_botao(tela, "Sair", botao_sair_posicao)

        pygame.display.flip()

        # Evento de controle
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if (largura_tela // 2 - 150 <= mouse_pos[0] <= largura_tela // 2 + 150) and (altura_tela // 2 + 50 <= mouse_pos[1] <= altura_tela // 2 + 100):
                    return "jogar"  # Se clicar em "Jogar Novamente"
                elif (largura_tela // 2 - 100 <= mouse_pos[0] <= largura_tela // 2 + 100) and (altura_tela // 2 + 110 <= mouse_pos[1] <= altura_tela // 2 + 160):
                    pygame.quit()  # Se clicar em "Sair"
                    return

# Loop principal do jogo
def jogo():
    cobra = Cobra()
    capivaras = []
    pontuacao = 0  # Inicializa a pontuação
    clock = pygame.time.Clock()
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            cobra.mover("esquerda")
            cobra.girar("esquerda")
        elif teclas[pygame.K_RIGHT]:
            cobra.mover("direita")
            cobra.girar("direita")
        else:
            cobra.girar(None)  # Reseta a rotação quando nenhuma tecla é pressionada

        # Atualiza a imagem da cobra
        cobra.atualizar_imagem()

        # Atualiza capivaras
        if random.randint(1, 30) == 1:  # Chance de aparecer nova capivara
            x = random.randint(0, largura_tela)
            nova_rect = pygame.Rect(x, -50, capivara_imagens[0].get_width(), capivara_imagens[0].get_height())
            if pode_posicionar(capivaras, nova_rect):  # Verifica se pode posicionar
                capivaras.append(Capivara(x, -50))

        for capivara in capivaras[:]:
            capivara.mover()
            capivara.atualizar_imagem()  # Atualiza a imagem da capivara
            
            if capivara.rect.top > altura_tela:
                capivaras.remove(capivara)
                pontuacao += 1  # Incrementa a pontuação

                # Aumenta a velocidade a cada 20 pontos
                if pontuacao % 20 == 0:
                    global VELOCIDADE_CAPIVARA
                    VELOCIDADE_CAPIVARA *= VELOCIDADE_AUMENTO  # Aumenta a velocidade

            # Verifica colisão usando máscaras
            if (cobra.get_mask().overlap(capivara.get_mask(), (capivara.rect.x - cobra.rect.x, capivara.rect.y - cobra.rect.y))):
                print("Você foi pego pelas capivaras!")
                rodando = False

        # Desenha tudo
        tela.fill(branco)

        # Desenha a pontuação
        fonte_pontuacao = pygame.font.SysFont(None, 40)
        texto_pontuacao = fonte_pontuacao.render(f"Pontos: {pontuacao}", True, preto)
        tela.blit(texto_pontuacao, (10, 10))  # Exibe a pontuação no topo à esquerda

        cobra.desenhar(tela)
        for capivara in capivaras:
            capivara.desenhar(tela)

        pygame.display.flip()
        clock.tick(60)

    # Tela de Game Over
    resultado = tela_game_over(pontuacao)
    return resultado

# Inicia o jogo
if __name__ == "__main__":
    # Exibe a tela inicial
    resultado = tela_inicial()
    while resultado == "jogar":
        resultado = jogo()
