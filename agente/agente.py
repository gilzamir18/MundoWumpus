from mundowumpus import MeuAmbiente
import random

class Agente:
    def __init__(self):
        self.q = {} #tabela de valores q(a, s)
        self.lr = 0.001 #taxa de aprendizagem
        self.gamma = 0.5 #taxa de desconto
        self.eps = 0.05 #epsilon do algoritmo e-greedy
    

    def agir(self, estado):
        """
        Retorna uma ação com base no estado <estado>.
        """
        if random.random() < self.eps: #se a roleta caiu no pedaço menor da pizza
            #Escolhe uma acao aleatoriamente
            return random.choice([
                MeuAmbiente.ACAO_DIR,
                MeuAmbiente.ACAO_ESQ,
                MeuAmbiente.ACAO_ACIMA,
                MeuAmbiente.ACAO_ABAIXO
            ])
        else: #caso a roleta caia na parte maior da pizza.
            #seleciona uma acao com base na funcao de valor q.
            p = estado['posicao'] #verifica a posicao do estado atual
            b = estado['brisa'][0] #verifica se tem brisa no estado atual, 0 caso não, 1 se sim.
            f = estado['fedor'][0] #verifica se tem fedor no estado atual, 0 caso não, 1 se sim.
            #o estado é uma tupla k contendo a linha, 
            # a coluna, se tem brisa na célula e se tem fedor na célula.
            k = (p[0], p[1], b, f) 
            acoes = [MeuAmbiente.ACAO_DIR,
                     MeuAmbiente.ACAO_ESQ,
                     MeuAmbiente.ACAO_ACIMA,
                     MeuAmbiente.ACAO_ABAIXO]
            
            #Estes ifs apenas garantem que haverá algum valor em q para cada par (estado_atual, acao).
            if not (k, MeuAmbiente.ACAO_DIR) in self.q:
                self.q[(k,  MeuAmbiente.ACAO_DIR)] = 0
            if not (k, MeuAmbiente.ACAO_ESQ) in self.q:
                self.q[(k,  MeuAmbiente.ACAO_ESQ)] = 0
            if not (k, MeuAmbiente.ACAO_ACIMA) in self.q:
                self.q[(k,  MeuAmbiente.ACAO_ACIMA)] = 0
            if not (k, MeuAmbiente.ACAO_ABAIXO) in self.q:
                self.q[(k,  MeuAmbiente.ACAO_ABAIXO)] = 0

            #Este laço apenas bsuca a acao de maior valor para o estado atual
            maior = 0
            for acao in acoes:
                if self.q[(k, acao)] > self.q[(k, maior)]:
                    maior = acao
            return maior #retorna a acao de maior valor

    def aprender(self, st, a, stp1, r, fim):
        """
        A função <aprender> recebe o estado atual (st),
        a ação que foi aplica neste estado atual,
        o estado sucessor <stp1>,
        uma recompensa <r> e
        se o episodio terminou <fim>. Com base nessa transição,
        a função atualiza a tabela <q> com base nas equações de
        atualização de Bellman, formando o algoritmo q-learning.
        """
        #as próximas três linhas capturam informações para formação do estado atual k.
        p = st['posicao'] #pega posicao.
        b = st['brisa'][0] #pega brisa.
        f = st['fedor'][0] #pega fedor.
        k = (p[0], p[1], b, f) #constroi o estado como uma tupla.
        if not (k, a) in self.q: #se não viu o par (k, a) antes, o valor disso é 0 (zero).
            self.q[(k,  a)] = 0 #como o par (k, a) ainda não existe em q, seta o valor pra zero.

        if fim: #um estado final tem o valor de Q(s, a) igual a zero
            pl = stp1['posicao']
            bl = stp1['brisa'][0]
            fl = stp1['fedor'][0]
            kl = (pl[0], pl[1], bl, fl)
            self.q[(kl, MeuAmbiente.ACAO_DIR)] = 0
            self.q[(kl, MeuAmbiente.ACAO_ESQ)] = 0
            self.q[(kl, MeuAmbiente.ACAO_ABAIXO)] = 0
            self.q[(kl, MeuAmbiente.ACAO_ACIMA)] = 0
            #a atualização no estado antes do final muda um pouco:
            self.q[(k, a)] = self.q[(k, a)] + self.lr * (r - self.q[(k, a)])
        else:
            #atualizacao de um estado nao terminal
            pl = stp1['posicao']
            bl = stp1['brisa'][0]
            fl = stp1['fedor'][0]
            kl = (pl[0], pl[1], b, f) #constroi a tupla do estado resultante

            #INICO::Garante que a entrada na tabela para cada acao e estado resultante não seja nula.
            if not (kl, MeuAmbiente.ACAO_DIR) in self.q:
                self.q[(kl,  MeuAmbiente.ACAO_DIR)] = 0
            if not (kl, MeuAmbiente.ACAO_ESQ) in self.q:
                self.q[(kl,  MeuAmbiente.ACAO_ESQ)] = 0
            if not (kl, MeuAmbiente.ACAO_ACIMA) in self.q:
                self.q[(kl,  MeuAmbiente.ACAO_ACIMA)] = 0
            if not (kl, MeuAmbiente.ACAO_ABAIXO) in self.q:
                self.q[(kl,  MeuAmbiente.ACAO_ABAIXO)] = 0
            #FIM::

            #INICIO::Pega o melhor resultado possivel no estado sucessor.
            melhorFuturo = float("-inf")
            for al in [MeuAmbiente.ACAO_DIR, 
                        MeuAmbiente.ACAO_ESQ, 
                        MeuAmbiente.ACAO_ACIMA,
                        MeuAmbiente.ACAO_ABAIXO]:
                if self.q[(kl, al)] > melhorFuturo:
                    melhorFuturo = self.q[kl, al]
            #FIM::

            #ATUALIZACAO DE UM ESTADO NAO TERMINAL
            self.q[(k, a)] = self.q[(k, a)] + self.lr  * (r + self.gamma * melhorFuturo - self.q[(k, a)])
