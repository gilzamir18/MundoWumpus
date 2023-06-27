import mundowumpus #importa o modulo do mundo wumpus
import gym #importa o gym
from agente import Agente #importa a classe do agente
import time  #para pausar
from matplotlib import pyplot #para plotar gráfico

env = gym.make("Wumpus-v0") #cria o ambiente
agente = Agente() #cria o agente

recompensas = []
for i in range(200): #epocas 
    soma = 0 #soma de recompensas em cada episodio
    estado_atual, _ = env.reset() #reseta o ambiente e pega o estado mais recente que o agente perceberá.
    fim = False #flag de fim de episódio
    while not fim: #enquanto nao terminar
        acao = agente.agir(estado_atual) #faz o agente selecionar uma acao
        novo_estado, recompensa, fim, _, _ = env.step(acao) #aplica a acao no ambiente
        agente.aprender(estado_atual, acao, novo_estado, recompensa, fim) #manda o agente aprender com a experiência (transição)
        soma += recompensa #atualiza a soma de recompensas por episodio
        #Se quiser rodar a simulacao de forma mais lenta (60fps):
        #time.sleep(1/60.0) 
        if fim: #se terminou episodio
            print(f"Ep{i}:: Soma de recompensas: {soma}") #imprime soma de recompensas
            novo_estado = None #reseta o novo estado
            estado_atual = None #reseta o estado atual
            recompensas.append(soma) #registra a soma de recompensas para plotar mais na frente
            break #interrompe o episodio atual
        else: #caso o episodio nao tenha chegado ao fim
            estado_atual = novo_estado  #atualiza o estado atual como sendo o estado mais novo
pyplot.plot(recompensas) #plota todas as recompensas
pyplot.show() #mostra o grafico