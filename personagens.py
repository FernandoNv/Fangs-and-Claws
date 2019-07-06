delay_menu = delay_tela = 5


class Personagem:
    # atributos dos personagens
    def __init__(self, nome, sprite, qtd_vidas, velocidade):
        self.nome = nome
        self.sprite = sprite
        self.qtd_vidas = qtd_vidas
        self.velocidade = velocidade


class Jogador(Personagem):
    def __init__(self, nome, sprite, qtd_vidas, velocidade,):
        super().__init__(nome, sprite, qtd_vidas, velocidade)

    # self no caso seria um objeto da classe jogador(self -> poderia ser trocado por valentine)
    def controles(self, teclado, janela, frame):
        global delay_tela
        delay_tela += janela.delta_time() * 2

        if teclado.key_pressed("D") and self.sprite.x + 1 + self.sprite.width < janela.width:
            self.sprite.x = self.sprite.x + self.velocidade * janela.delta_time()
            self.sprite.set_curr_frame(1)

        if teclado.key_pressed("S") and self.sprite.y + 1 + self.sprite.width < janela.height:
            self.sprite.y = self.sprite.y + self.velocidade * janela.delta_time()
            self.sprite.set_curr_frame(2)

        if teclado.key_pressed("W") and self.sprite.y - 1 > 0:
            self.sprite.y = self.sprite.y - self.velocidade * janela.delta_time()
            self.sprite.set_curr_frame(0)

        if teclado.key_pressed("A") and self.sprite.x - 1 > 0:
            self.sprite.x = self.sprite.x - self.velocidade * janela.delta_time()
            self.sprite.set_curr_frame(3)


        if teclado.key_pressed("ESC") and frame == 1 and delay_tela >= delay_menu:
            delay_tela = 0
            frame = 4
            return self, frame

        if teclado.key_pressed("ESC") and frame == 4 and delay_tela >= delay_menu:
            delay_tela = 0
            frame = 1
            return self, frame

        return self, frame


class Monstro(Personagem):
    def __init__(self, nome, sprite, qtd_vidas, velocidade, knockback, mover):
        super().__init__(nome, sprite, qtd_vidas, velocidade)
        self.knockback = knockback
        self.mover = mover

    def movimento(self, valentine, janela):
        if self.mover is True:
            if self.sprite.x > valentine.sprite.x:
                self.sprite.x -= self.velocidade * janela.delta_time()
            self.sprite.set_curr_frame(4)
            if self.sprite.x < valentine.sprite.x:
                self.sprite.x += self.velocidade * janela.delta_time()
                self.sprite.set_curr_frame(2)
            if self.sprite.y > valentine.sprite.y:
                self.sprite.y -= self.velocidade * janela.delta_time()
                self.sprite.set_curr_frame(1)
            if self.sprite.y < valentine.sprite.y:
                self.sprite.y += self.velocidade * janela.delta_time()
                self.sprite.set_curr_frame(3)

    def colisao(self, valentine, janela):
        if valentine.sprite.collided(self.sprite):
            #knockback
            if self.sprite.x > valentine.sprite.x:
                if valentine.sprite.x - self.knockback * janela.delta_time() > 0:
                    valentine.sprite.x -= self.knockback * janela.delta_time()
            if self.sprite.x < valentine.sprite.x:
                if valentine.sprite.x + self.knockback * janela.delta_time() < janela.width - valentine.sprite.width:
                    valentine.sprite.x += self.knockback * janela.delta_time()
            if self.sprite.y > valentine.sprite.y:
                if valentine.sprite.y - self.knockback * janela.delta_time() > 0:
                    valentine.sprite.y -= self.knockback * janela.delta_time()
            if self.sprite.y < valentine.sprite.y:
                if valentine.sprite.y + self.knockback * janela.delta_time() < janela.height - valentine.sprite.height:
                    valentine.sprite.y += self.knockback * janela.delta_time()

            valentine.qtd_vidas -= 1

    def levouTiro(self, lista_tiros, habilidade):
        for i in range(len(lista_tiros)):
            if lista_tiros[i] is not None:
                if lista_tiros[i][0].collided(self.sprite):
                    if habilidade.nome is "Tiro":
                        lista_tiros[i] = None
                        self.qtd_vidas -= 1
                    if habilidade.nome is "Bala":
                        self.qtd_vidas -= 1
                    if habilidade.nome is "Granada":
                        self.mover = False
