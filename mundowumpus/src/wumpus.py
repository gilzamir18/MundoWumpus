import gym
import numpy as np  

class MeuAmbiente(gym.Env):
    ID_AGENTE = 2
    ID_POCO = -1
    ID_WUMPUS = 1
    ID_PISO = 0
    ACAO_DIR = 0
    ACAO_ESQ = 1
    ACAO_ACIMA = 2
    ACAO_ABAIXO = 3

    def __init__(self, size=4):
        self.size = size
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Dict(
            {
                "posicao": gym.spaces.Box(0, 4, shape=(2,), dtype=float),
                "brisa": gym.spaces.Box(0, 1, shape=(1,), dtype=float),
                "fedor": gym.spaces.Box(0, 1, shape=(1, ), dtype=float)
            })
        self.reset()


    def validaPos(self, pos):
        return (pos[0] >= 0 and pos[0] < self.size and
                    pos[1] >= 0 and pos[1] < self.size)

    def temFedor(self, p=None):
        if p is None:
            p = self.pos_agente
        x, y = p
        return (
            (self.validaPos( (x-1, y) ) and self.grade[x-1][y] == MeuAmbiente.ID_WUMPUS) or
            (self.validaPos( (x+1, y) ) and self.grade[x+1][y] == MeuAmbiente.ID_WUMPUS) or 
            (self.validaPos( (x, y-1) ) and self.grade[x][y-1] == MeuAmbiente.ID_WUMPUS) or
            (self.validaPos( (x, y+1) ) and self.grade[x][y+1] == MeuAmbiente.ID_WUMPUS)
            )

    def temBrisa(self, p=None):
        if p is None:
            p = self.pos_agente
        x, y = p
        return (
            (self.validaPos( (x-1, y) ) and self.grade[x-1][y] == MeuAmbiente.ID_POCO) or
            (self.validaPos( (x+1, y) ) and self.grade[x+1][y] == MeuAmbiente.ID_POCO) or 
            (self.validaPos( (x, y-1) ) and self.grade[x][y-1] == MeuAmbiente.ID_POCO) or
            (self.validaPos( (x, y+1) ) and self.grade[x][y+1] == MeuAmbiente.ID_POCO)
            )

    def reset(self, seed=None, **options):
        size = self.size
        self.grade = []
        self.seed = seed
        for line in range(size):
            self.grade.append([MeuAmbiente.ID_PISO]*4)
        self.grade[0][0] = MeuAmbiente.ID_AGENTE
        self.grade[-1][-1] = MeuAmbiente.ID_WUMPUS
        self.grade[2][2] = MeuAmbiente.ID_POCO
        self.pos_agente = (0, 0)
        self.objetivo = (size-1, 0)
        return {'posicao': np.array(self.pos_agente, dtype=float), 
                'brisa': np.array([1] if self.temBrisa() else [0], dtype=float), 
                'fedor': np.array([1] if self.temFedor() else [0], dtype=float) }, {}

    def step(self, acao):
        p = self.pos_agente
        if acao == MeuAmbiente.ACAO_DIR:
            prox_linha = p[0] + 1
            if prox_linha < self.size:
                self.pos_agente = (prox_linha, p[1])
        elif acao == MeuAmbiente.ACAO_ESQ:
            prox_linha = p[0] - 1
            if prox_linha >= 0:
                self.pos_agente = (prox_linha, p[1])
        elif acao == MeuAmbiente.ACAO_ACIMA:
            prox_col = p[1] + 1
            if prox_col < self.size:
                self.pos_agente = (p[0], prox_col)
        elif acao == MeuAmbiente.ACAO_ABAIXO:
            prox_col = p[1] - 1
            if prox_col >= 0:
                self.pos_agente = (p[0], prox_col)
        recompensa = -0.001
        nps = self.pos_agente #nova posicao
        fim = False
        if self.pos_agente == self.objetivo:
            recompensa = 1
            fim = True #agente alcançou o alvo
        elif (self.grade[nps[0]][nps[1]] == MeuAmbiente.ID_WUMPUS or
                self.grade[nps[0]][nps[1]] == MeuAmbiente.ID_POCO):
            recompensa = -1
            fim = True #agente morreu
        else:
            self.grade[p[0]][p[1]] = MeuAmbiente.ID_PISO
            self.grade[nps[0]][nps[1]] = MeuAmbiente.ID_AGENTE
        return  ({'posicao': np.array(self.pos_agente, dtype=float), 
                 'brisa': np.array([1] if self.temBrisa() else [0], dtype=float), 
                 'fedor': np.array([1] if self.temFedor() else [0], dtype=float) }, 
                    recompensa, 
                    np.bool_(fim), 
                    np.bool_(False),
                    {})

    def render(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.grade[i][j], end=" ")
            print("")
    
    def close(self):
        pass #remover ou liberar recursos, se necessário
