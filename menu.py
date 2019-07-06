from PPlay.animation import *
from PPlay.gameimage import *

# Ajudar na criacao dos botoes do menu(nao escrever a mesma coisa varias vezes)
# recebe o nome do botao e as coordenadas x e y do botao

def criarBotao(nome, x, y):
    bt = Animation("sprites/geral/bt-" + nome + ".png", 2, loop=False)
    bt.set_position(x, y)
    bt.set_curr_frame(0)

    return bt


class Hud:
    def __init__(self, sprite_personagem, sprite_nome_personagem, qtd_vidas, sprite_granada, sprite_bala):
        self.sprite_personagem = sprite_personagem
        self.sprite_nome_personagem = sprite_nome_personagem
        self.qtd_vidas = qtd_vidas
        self.sprite_granada = sprite_granada
        self.sprite_bala = sprite_bala

    def criarListaVidas(self, lista_qtd_vidas, qtd_vidas, janela):
        for i in range(qtd_vidas):
            lista_qtd_vidas.append(GameImage("sprites/geral/gotaSangue.png"))
            lista_qtd_vidas[i].x = janela.width - janela.width * (85 - i * 5) / 100
            lista_qtd_vidas[i].y = janela.height - janela.height * 87 / 100

    def mostrarQtdVidas(self, lista_qtd_vidas, qtd_vidas):
        for i in range(qtd_vidas):
            lista_qtd_vidas[i].draw()

    def mostrarHabilidadePersonagem(self, habilidade):
        habilidade.draw()
