from PPlay.gameimage import *
from PPlay.animation import *

posicao_mouse = None


class Habilidade:
    def __init__(self, nome, sprite, tempo_recarga, tempo_delay, velocidade):
        self.nome = nome
        self.sprite = sprite
        self.tempo_recarga = tempo_recarga
        self.tempo_delay = tempo_delay
        self.velocidade = velocidade


class Tiro(Habilidade):
    def __init__(self, nome, sprite, tempo_recarga, tempo_delay, velocidade):
        super().__init__(nome, sprite, tempo_recarga, tempo_delay, velocidade)

    def criarTiro(self, jogador):
        elemento = None
        if self.nome == "Tiro" or self.nome == "Granada":
            elemento = GameImage(self.sprite)
        elif self.nome == "Bala":
            elemento = Animation(self.sprite, 4, loop=False)
        if jogador.sprite.get_curr_frame() == 0:
            elemento.set_position(jogador.sprite.x + jogador.sprite.width / 2.70,
                                  jogador.sprite.y - jogador.sprite.height / 2.70)
            if self.nome == "Bala":
                elemento.set_curr_frame(0)
        if jogador.sprite.get_curr_frame() == 1:
            elemento.set_position(jogador.sprite.x + jogador.sprite.width,
                                  jogador.sprite.y + jogador.sprite.height / 2.70)
            if self.nome == "Bala":
                elemento.set_curr_frame(1)
        if jogador.sprite.get_curr_frame() == 2:
            elemento.set_position(jogador.sprite.x + jogador.sprite.width / 2.70,
                                  jogador.sprite.y + 1.2 * jogador.sprite.height)
            if self.nome == "Bala":
                elemento.set_curr_frame(2)
        if jogador.sprite.get_curr_frame() == 3:
            elemento.set_position(jogador.sprite.x - jogador.sprite.width / 2,
                                  jogador.sprite.y + jogador.sprite.height / 2.70)
            if self.nome == "Bala":
                elemento.set_curr_frame(3)
        return elemento

    def getTiro(self, jogador, mouse, teclado, janela):
        global posicao_mouse
        if self.nome == "Tiro":
            if mouse.is_over_object(janela) and mouse.is_button_pressed(1) and self.tempo_delay >= self.tempo_recarga:
                self.tempo_delay = 0
                tiro = self.criarTiro(jogador)
                return [tiro, jogador.sprite.get_curr_frame()]
        if self.nome == "Bala":
            if teclado.key_pressed("SPACE") and self.tempo_delay > self.tempo_recarga:
                self.tempo_delay = 0
                tiro = self.criarTiro(jogador)
                return [tiro, jogador.sprite.get_curr_frame()]
        if self.nome == "Granada":
            if teclado.key_pressed("E") and self.tempo_delay > self.tempo_recarga:
                posicao_mouse = mouse.get_position()
                self.tempo_delay = 0
                tiro = self.criarTiro(jogador)
                return [tiro, jogador.sprite.get_curr_frame()]

    def mostrarTiro(self, tiro):
        if tiro is not None:
            return tiro[0].draw()

    def moverTiro(self, tiro, janela):
        if tiro is not None:
            if tiro[1] == 0:
                tiro[0].y -= self.velocidade * janela.delta_time()
            if tiro[1] == 1:
                tiro[0].x += self.velocidade * janela.delta_time()
            if tiro[1] == 2:
                tiro[0].y += self.velocidade * janela.delta_time()
            if tiro[1] == 3:
                tiro[0].x -= self.velocidade * janela.delta_time()

    def moverGranada(self, tiro, janela):
        if tiro is not None:
            if posicao_mouse[1] > tiro[0].y:
                tiro[0].y += self.velocidade * janela.delta_time()
            if posicao_mouse[1] < tiro[0].y:
                tiro[0].y -= self.velocidade * janela.delta_time()
            if posicao_mouse[0] > tiro[0].x:
                tiro[0].x += self.velocidade * janela.delta_time()
            if posicao_mouse[0] < tiro[0].x:
                tiro[0].x -= self.velocidade * janela.delta_time()

    def funcionalidadeTiros(self, lista_tiros, tiro, janela):
        if tiro is not None:
            lista_tiros.append(tiro)

        # mostrar os tiros
        for i in range(len(lista_tiros)):
            self.mostrarTiro(lista_tiros[i])

        # fazer os tiros se moverem na tela
        for i in range(len(lista_tiros)):
            if self.nome == "Granada":
                self.moverGranada(lista_tiros[i], janela)
            else:
                self.moverTiro(lista_tiros[i], janela)
        # ir removendo os tiros da lista
        if self.nome == "Granada" and self.tempo_delay > self.tempo_recarga / 5:
            # ir removendo os tiros da lista
            for i in range(len(lista_tiros)):
                lista_tiros.pop(i)
        else:
            for i in range(len(lista_tiros)):
                if lista_tiros[i] is not None:
                    if lista_tiros[i][0].x > janela.width:
                        lista_tiros[i] = None
                    elif lista_tiros[i][0].x < 0:
                        lista_tiros[i] = None
                    elif lista_tiros[i][0].y > janela.height:
                        lista_tiros[i] = None
                    elif lista_tiros[i][0].y < 0:
                        lista_tiros[i] = None
            for i in range(len(lista_tiros)-1):
                if lista_tiros[i] is None:
                    lista_tiros.pop(i)
