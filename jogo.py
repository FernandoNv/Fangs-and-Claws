from PPlay.gameimage import *
from PPlay.window import *
from PPlay.animation import *
from PPlay.sound import *
from menu import criarBotao
from menu import Hud
from personagens import Jogador, Monstro
from habilidades import Tiro
from pontuacao import getPontuacao, carregarPontuacao, matriz_pontuacao, gravarPontuacao
from random import *

carregarPontuacao()
x = 1000
y = 700
janela = Window(x, y)
pontuacao = 0

janela.set_title("Fangs&Claws")
teclado = janela.get_keyboard()
mouse = Window.get_mouse()
background = GameImage("sprites/background-menu.png")
background_jogo = GameImage("sprites/background-jogo.png")
background_jogo_pause = GameImage("sprites/background-jogo-pause.png")
# utilizado para ajudar na passagem entre as tela(menu, o jogo, placar)
frame = 0

bt_jogar = criarBotao("jogar", 400, 350)
bt_configuracoes = criarBotao("configuracoes", 350, 420)
bt_placar = criarBotao("placar", 400, 490)
bt_sair = criarBotao("sair", 400, 560)
bt_voltar = criarBotao("voltar", 31, 610)

area_botoes = GameImage("sprites/geral/configuracoes.png")
area_botoes.set_position(0, 195)

placar_background = GameImage("sprites/geral/placar-background.png")
placar_background.set_position(147, 262)

game_over = GameImage("sprites/background-game-over.png")

valentine = Jogador("Valentine", Animation("sprites/mainchar/valentine/valentine.png", 5, loop=False), 3, 200)
valentine.sprite.set_position((janela.width / 2) - (valentine.sprite.width / 2),
                              (janela.height / 2) - (valentine.sprite.height / 2))

# nome, sprite, tempo_recarga, tempo_delay, velocidade)
habilidade_tiro = Tiro("Tiro", "sprites/mainchar/valentine/val_bullet.png", 300, 300, 400)
habilidade_bala = Tiro("Bala", "sprites/mainchar/valentine/skills/bullet.png", 10000, 10000, 900)
habilidade_granada = Tiro("Granada", "sprites/mainchar/valentine/skills/granada.png", 10000, 10000, 400)

lista_tiros = []
lista_balas = []
lista_granadas = []

# musica do menu
sound_menu = Sound("sounds/bensound-epic-menu.ogg")
sound_menu.set_repeat(True)

# musica do jogo
sound_jogo = Sound("sounds/bensound-instinct-jogo.ogg")
sound_jogo.set_repeat(True)

# hud jogo
valentine_foto = GameImage("sprites/geral/valentine.png")
valentine_foto.set_position(10, 10)

valentine_nome = GameImage("sprites/geral/valentine-nome.png")
valentine_nome.set_position(141, 33)

sprite_granada = Animation("sprites/mainchar/valentine/skills/valentine_skill_1.png", 2, loop=False)
sprite_granada.set_position(x - x * 15 / 100 * 1.5, y - y * 15 / 100)

sprite_bala = Animation("sprites/mainchar/valentine/skills/valentine_skill_2.png", 2, loop=False)
sprite_bala.set_position(x - x * 15 / 100, y - y * 20 / 100)

lista_qtd_vidas = []
hud_jogo = Hud(valentine_foto, valentine_nome, valentine.qtd_vidas, sprite_granada, sprite_bala)
hud_jogo.criarListaVidas(lista_qtd_vidas, hud_jogo.qtd_vidas, janela)

# parte dos monstros

# inicializando a lista de monstros + funcao que coloca monstro na lista
monstros = []
monstrosRecarga = 25
tempo = 25

cont_monstros = 0


def addMonstro(monstros, janela):
    global cont_monstros
    tipo = randint(1, 2)

    if cont_monstros >= 20:
        cont_monstros = 0
        monstros.append(
                Monstro("Werewolf Boss", Animation("sprites/monstros/werewolves/werewolfBoss.png", 5, loop=False), 5,
                        55, 15000, True))
        monstros.append(
                Monstro("Vampire Boss", Animation("sprites/monstros/vampires/vampireBoss.png", 5, loop=False), 3, 100,
                        15000, True))
    if cont_monstros == 10:
        cont_monstros += 1
        if tipo == 1:
            monstros.append(
                Monstro("Werewolf Boss", Animation("sprites/monstros/werewolves/werewolfBoss.png", 5, loop=False), 5,
                        55, 15000, True))
        else:
            monstros.append(
                Monstro("Vampire Boss", Animation("sprites/monstros/vampires/vampireBoss.png", 5, loop=False), 3, 100,
                        15000, True))
    else:
        if tipo == 1:
            monstros.append(
                Monstro("werewolf", Animation("sprites/monstros/werewolves/werewolf.png", 5, loop=False), 2, 50, 15000,
                        True))
        if tipo == 2:
            monstros.append(
                Monstro("vampire", Animation("sprites/monstros/vampires/vampire.png", 5, loop=False), 1, 75, 15000,
                        True))
        cont_monstros += 1
    tipo = randint(1, 4)
    if tipo == 1:
        monstros[len(monstros) - 1].sprite.x = randint(0, janela.width)
        monstros[len(monstros) - 1].sprite.y = 0 - monstros[len(monstros) - 1].sprite.height
    if tipo == 2:
        monstros[len(monstros) - 1].sprite.x = janela.width + monstros[len(monstros) - 1].sprite.width
        monstros[len(monstros) - 1].sprite.y = randint(0, janela.height)
    if tipo == 3:
        monstros[len(monstros) - 1].sprite.x = randint(0, janela.width)
        monstros[len(monstros) - 1].sprite.y = janela.height + monstros[len(monstros) - 1].sprite.height
    if tipo == 4:
        monstros[len(monstros) - 1].sprite.x = 0 - monstros[len(monstros) - 1].sprite.height
        monstros[len(monstros) - 1].sprite.y = randint(0, janela.height)


# funcao que checa se monstro ta vivo
def isVivo(Personagem):
    if Personagem.qtd_vidas <= 0:
        return False
    else:
        return True


def gameOver():
    global frame
    global monstros
    global valentine
    global pontuacao
    global lista_tiros
    global lista_granadas
    global habilidade_granada
    global habilidade_tiro
    global habilidade_bala
    global cont_monstros

    resp = False
    while resp is False:
        janela.update()
        game_over.draw()
        janela.draw_text(str(pontuacao), 450, 470, size=30, color=(220, 220, 220), font_name="Arial", bold=True,
                         italic=False)
        if teclado.key_pressed("SPACE"):
            resp = True
        janela.update()

    if matriz_pontuacao[4][0] < pontuacao:
        nome = input("Digite seu nome: ")
        getPontuacao(int(pontuacao), nome)
    frame = 0
    valentine.qtd_vidas = 3
    valentine.sprite.set_position((janela.width / 2) - (valentine.sprite.width / 2),
                                  (janela.height / 2) - (valentine.sprite.height / 2))
    monstros = []
    pontuacao = 0
    lista_tiros = []
    lista_granadas = []
    habilidade_granada.tempo_delay = 1000
    habilidade_granada.tempo_recarga = 1000
    habilidade_tiro.tempo_delay = 300
    habilidade_tiro.tempo_recarga = 300
    habilidade_bala.tempo_delay = 1000
    habilidade_bala.tempo_recarga = 1000
    cont_monstros = 0


def main():
    global frame
    global valentine
    global monstrosRecarga
    global pontuacao
    # frame do menu
    while frame == 0 or frame == 1 or frame == 2 or frame == 3 or frame == 4 or frame == 5:
        # frame do menu iniciar
        if frame == 0:
            while frame == 0:
                background.draw()
                sound_menu.play()
                if mouse.is_over_object(bt_jogar):
                    bt_jogar.set_curr_frame(1)
                    if mouse.is_button_pressed(1):
                        frame = 1
                else:
                    bt_jogar.set_curr_frame(0)

                if mouse.is_over_object(bt_configuracoes):
                    bt_configuracoes.set_curr_frame(1)
                    if mouse.is_button_pressed(1):
                        frame = 2
                else:
                    bt_configuracoes.set_curr_frame(0)

                if mouse.is_over_object(bt_placar):
                    bt_placar.set_curr_frame(1)
                    if mouse.is_button_pressed(1):
                        frame = 3
                else:
                    bt_placar.set_curr_frame(0)

                if mouse.is_over_object(bt_sair):
                    if mouse.is_button_pressed(1):
                        frame = 5
                    bt_sair.set_curr_frame(1)
                else:
                    bt_sair.set_curr_frame(0)
                bt_jogar.draw()
                bt_configuracoes.draw()
                bt_placar.draw()
                bt_sair.draw()
                janela.update()
        # frame para rodar o jogo
        if frame == 1:
            while frame == 1:
                sound_menu.stop()
                sound_jogo.play()
                sound_jogo.increase_volume(100)
                background_jogo.draw()
                tiro = None
                bala = None
                granada = None

                # parte dos monstros
                if monstrosRecarga >= tempo:
                    addMonstro(monstros, janela)
                    monstrosRecarga = 0
                else:
                    monstrosRecarga += 10 * janela.delta_time()

                for i in range(len(monstros)):
                    if monstros[i] is not None:
                        monstros[i].levouTiro(lista_tiros, habilidade_tiro)
                        monstros[i].levouTiro(lista_balas, habilidade_bala)
                        monstros[i].levouTiro(lista_granadas, habilidade_granada)
                        if habilidade_granada.tempo_delay > habilidade_granada.tempo_recarga / 5:
                            for j in range(len(monstros)):
                                if monstros[j] is not None:
                                    monstros[j].mover = True
                        monstros[i].movimento(valentine, janela)
                        monstros[i].colisao(valentine, janela)
                        monstros[i].sprite.draw()
                        if isVivo(monstros[i]) is False:
                            if monstros[i].nome == "werewolf":
                                pontuacao += 200
                            if monstros[i].nome == "Werewolf Boss":
                                pontuacao += 500
                            if monstros[i].nome == "vampire":
                                pontuacao += 100
                            if monstros[i].nome == "Vampire Boss":
                                pontuacao += 300
                            monstros[i] = None

                valentine, frame = valentine.controles(teclado, janela, frame)
                hud_jogo.qtd_vidas = valentine.qtd_vidas
                valentine.sprite.draw()

                hud_jogo.mostrarQtdVidas(lista_qtd_vidas, hud_jogo.qtd_vidas)
                hud_jogo.mostrarHabilidadePersonagem(hud_jogo.sprite_personagem)
                hud_jogo.mostrarHabilidadePersonagem(hud_jogo.sprite_nome_personagem)
                hud_jogo.mostrarHabilidadePersonagem(hud_jogo.sprite_granada)
                hud_jogo.mostrarHabilidadePersonagem(hud_jogo.sprite_bala)

                janela.draw_text(str(pontuacao), 50, 120, size=23, color=(220, 220, 220),
                                 font_name="Arial", bold=True, italic=False)

                # retorna um vetor com o tiro e o frame do jogador para fazer o mover do tiro
                tiro = habilidade_tiro.getTiro(valentine, mouse, teclado, background_jogo)
                habilidade_tiro.funcionalidadeTiros(lista_tiros, tiro, janela)
                # marcar o tempo para o proximo tiro
                habilidade_tiro.tempo_delay += janela.delta_time() * habilidade_tiro.velocidade

                bala = habilidade_bala.getTiro(valentine, mouse, teclado, background_jogo)
                habilidade_bala.funcionalidadeTiros(lista_balas, bala, janela)
                # marcar o tempo para o proximo tiro
                habilidade_bala.tempo_delay += janela.delta_time() * habilidade_bala.velocidade

                granada = habilidade_granada.getTiro(valentine, mouse, teclado, background_jogo)
                habilidade_granada.funcionalidadeTiros(lista_granadas, granada, janela)
                # marcar o tempo para o proximo tiro
                habilidade_granada.tempo_delay += janela.delta_time() * habilidade_granada.velocidade

                if habilidade_granada.tempo_delay < habilidade_granada.tempo_recarga:
                    hud_jogo.sprite_granada.set_curr_frame(1)
                else:
                    hud_jogo.sprite_granada.set_curr_frame(0)

                if habilidade_bala.tempo_delay < habilidade_bala.tempo_recarga:
                    hud_jogo.sprite_bala.set_curr_frame(1)
                else:
                    hud_jogo.sprite_bala.set_curr_frame(0)
                if valentine.qtd_vidas <= 0:
                    gameOver()
                janela.update()
        # frame para fechar o jogo
        if frame == 2:
            while frame == 2:
                background.draw()
                area_botoes.draw()
                bt_voltar.draw()
                if mouse.is_over_object(bt_voltar):
                    bt_voltar.set_curr_frame(1)
                    if mouse.is_button_pressed(1):
                        frame = 0
                else:
                    bt_voltar.set_curr_frame(0)
                janela.update()
        # frame para a tela de placar
        if frame == 3:
            while frame == 3:
                background.draw()
                placar_background.draw()

                for i in range(int(len(matriz_pontuacao))):
                    janela.draw_text(str(matriz_pontuacao[i][1]), janela.width - janela.width * 70 / 100,
                                     janela.height - janela.height * (40 - 7 * i) / 100, size=23, color=(220, 220, 220),
                                     font_name="Arial", bold=True, italic=False)
                    janela.draw_text(str(matriz_pontuacao[i][0]), janela.width - janela.width * 40 / 100,
                                     janela.height - janela.height * (40 - 7 * i) / 100, size=23, color=(220, 220, 220),
                                     font_name="Arial", bold=True, italic=False)

                bt_voltar.draw()
                if mouse.is_over_object(bt_voltar):
                    bt_voltar.set_curr_frame(1)
                    if mouse.is_button_pressed(1):
                        frame = 0
                else:
                    bt_voltar.set_curr_frame(0)
                janela.update()

        # frame para o menu dentro do jogo
        if frame == 4:
            while frame == 4:
                background_jogo_pause.draw()
                valentine, frame = valentine.controles(teclado, janela, frame)
                janela.update()

        if frame == 5:
            janela.close()


main()
gravarPontuacao()
