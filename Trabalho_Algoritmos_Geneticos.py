#Função de otimização: z = 𝑥**2 + 𝑦**2 + (3*𝑥 + 4*𝑦 − 26)**2
#Restrições: 𝑥 ∈ [0,10], 𝑦 ∈ [0,20]
#Codificação: Binária
#Seleção: Ranking
#Cruzamento: 2 pontos aleatórios
#Mutação: Inversão binária
#Elitismo 1 indivíduo por geração
#Função 3 
import matplotlib.pyplot as plt
import statistics
import random
import math

num_individuos = int(input("Quantos indivíduos você gostaria de ter em cada geração?\n"))
geracoes = int(input("Por quantas gerações você gostaria de executar o algoritmo?\n"))
taxa_de_cruzamento = float(input("Qual será a taxa de cruzamento?(por exemplo, 0.6)\n"))
taxa_de_mutação = float(input("Qual será a taxa de mutação?(por exemplo, 0.05)\n"))
INDIVIDUOS_ELITISMO = 1
TEMPO = 1   #quantidade de segundos que o grafico mostrará cada geração

#Gera os individuos baseando-se nos valores de x e y
class individuos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fitness = (x**2 + y**2 + (3*x + 4*y - 26)**2)
        
#Geram numeros aleatorios para x e y, para preencher a primeira geração
def rand_x():
    return round(random.uniform(0, 10), 3)

def rand_y():
    return round(random.uniform(0, 20), 3)

#Retorna o melhor indivíduo da população
def elitismo(populacao):
    melhor_individuo_geracao = max(populacao, key=lambda x: x.fitness)
    return melhor_individuo_geracao

#Separa as partes inteiras e fracionárias de um número decimal 
def separa(num):
    inteira  = int(num)
    fracao = num - inteira
    return inteira, fracao

#Seleção por rank
def provaveis_pais():
    pais = []
    for i in range(math.ceil(num_individuos/10)):
        pais.append(random.choice(populacao1))
    return max(pais, key=lambda x: x.fitness)

#Gerando a máscara para o cruzamento
def mask(tam_mask):
    ponto1 = random.randint(1, tam_mask)
    ponto2 = random.randint(1, tam_mask)
    
    while(ponto2 == ponto1):
        ponto2 = random.randint(1, tam_mask+1)
        
    if(ponto1 > ponto2):
        ponto1, ponto2 = ponto2, ponto1
        
    mascara = ''
    
    for i in range(1, tam_mask+1):
        if(i >= ponto1 and i <= ponto2):
            mascara += '1'
        else:
            mascara += '0'
    
    return mascara

#Fazendo a mutação
def mutacao(filho_bin):
    filho_mutado = list(filho_bin)
    for i in range(len(filho_mutado)):
        alpha = random.random()
        if(alpha < taxa_de_mutação):
            if(filho_mutado[i] == '1'):
                filho_mutado[i] = '0'
            else:
                filho_mutado[i] = '1'
    filho_mutado = ''.join(filho_mutado)
    return filho_mutado

def cruzamento():
    #É sorteado um número para saber se terá cruzamento ou não
    alpha = random.random()
    
    #Sorteio dos pais
    pai1 = provaveis_pais()
    pai2 = provaveis_pais()
    
    #Caso haja cruzamento
    if(alpha <= taxa_de_cruzamento):
    
        #Separa os genes dos pais em parte inteira e fracionária
        pai1_x_inteiro, pai1_x_fracao = separa(pai1.x)
        pai1_y_inteiro, pai1_y_fracao = separa(pai1.y)
        pai2_x_inteiro, pai2_x_fracao = separa(pai2.x)
        pai2_y_inteiro, pai2_y_fracao = separa(pai2.y)
        
        #Converte para binário a parte inteira
        binario_pai1_x_inteiro = bin(pai1_x_inteiro)[2:]
        binario_pai1_y_inteiro = bin(pai1_y_inteiro)[2:]
        binario_pai2_x_inteiro = bin(pai2_x_inteiro)[2:]
        binario_pai2_y_inteiro = bin(pai2_y_inteiro)[2:]
        
        #Converte para binário a parte fracionária
        binario_pai1_x_fracao = (bin(int(pai1_x_fracao*1000))[2:]).zfill(10)
        binario_pai1_y_fracao = (bin(int(pai1_y_fracao*1000))[2:]).zfill(10)
        binario_pai2_x_fracao = (bin(int(pai2_x_fracao*1000))[2:]).zfill(10)
        binario_pai2_y_fracao = (bin(int(pai2_y_fracao*1000))[2:]).zfill(10)

        #Juntando em uma só string
        binario_completo_pai1_x_y = (binario_pai1_x_inteiro + binario_pai1_x_fracao).zfill(15) + (binario_pai1_y_inteiro + binario_pai1_y_fracao).zfill(16)
        binario_completo_pai2_x_y = (binario_pai2_x_inteiro + binario_pai2_x_fracao).zfill(15) + (binario_pai2_y_inteiro + binario_pai2_y_fracao).zfill(16)
        
        mascara = mask(31)
        filho_binario_1 = ''
        filho_binario_2 = ''
        
        #Cruzando
        for i in range(len(mascara)):
            if(mascara[i] == '1'):
                filho_binario_1 += binario_completo_pai1_x_y[i]
                filho_binario_2 += binario_completo_pai2_x_y[i]
            else:
                filho_binario_1 += binario_completo_pai2_x_y[i]
                filho_binario_2 += binario_completo_pai1_x_y[i]
        
        #Mutando
        filho_binario_1 = mutacao(filho_binario_1)
        filho_binario_2 = mutacao(filho_binario_2)
        
        #Verificar se x ou y tem um valor menor que o limite e muda para 0
        if(filho_binario_1[0] == '1'):
            filho_binario_1 = "000000000000000" + filho_binario_1[15:]
        if(filho_binario_2[0] == '1'):
            filho_binario_2 = "000000000000000" + filho_binario_2[15:]
        if(filho_binario_1[15] == '1'):
            filho_binario_1 = filho_binario_1[:15] + "0000000000000000"
        if(filho_binario_2[15] == '1'):               
            filho_binario_2 = filho_binario_2[:15] + "0000000000000000"
            
        #Verifica se x ou y tem um valor maior que o limite e muda para o limite
        filho_1_x_total = round(int(filho_binario_1[5:15], 2)/1000 + int(filho_binario_1[:5], 2), 3)
        filho_2_x_total = round(int(filho_binario_2[5:15], 2)/1000 + int(filho_binario_2[:5], 2), 3)
        
        filho_1_y_total = round(int(filho_binario_1[21:], 2)/1000 + int(filho_binario_1[15:21], 2), 3)
        filho_2_y_total = round(int(filho_binario_2[21:], 2)/1000 + int(filho_binario_2[15:21] ,2), 3)
        
        if(filho_1_x_total > 10):
            filho_binario_1 = "010100000000000" + filho_binario_1[15:]
        if(filho_2_x_total > 10):
            filho_binario_2 = "010100000000000" + filho_binario_2[15:]
        
        if(filho_1_y_total > 20):
            filho_binario_1 = filho_binario_1[:15] + "0101000000000000"
        if(filho_2_y_total > 20):
            filho_binario_2 = filho_binario_2[:15] + "0101000000000000"
            
        #Recalcula em base decimal
        filho_1_x_total = round(int(filho_binario_1[5:15], 2)/1000 + int(filho_binario_1[:5], 2), 3)
        filho_2_x_total = round(int(filho_binario_2[5:15], 2)/1000 + int(filho_binario_2[:5], 2), 3)
        
        filho_1_y_total = round(int(filho_binario_1[21:], 2)/1000 + int(filho_binario_1[15:21], 2), 3)
        filho_2_y_total = round(int(filho_binario_2[21:], 2)/1000 + int(filho_binario_2[15:21] ,2), 3)
            
        #Agora que há certeza que nem x nem y ultrapassaram os limites, podemos fazer novos individuos
        filho1 = individuos(filho_1_x_total, filho_1_y_total)
        filho2 = individuos(filho_2_x_total, filho_2_y_total)
        
        return filho1, filho2
    
    #Caso não haja cruzamento
    else:
        return pai1, pai2

#Calcula e retorna a média do fitness da geração
def media(populacao):
    media_fitness = statistics.mean(individuos.fitness for individuos in populacao)
    return media_fitness

#Plota o gráfico dá media de fitness
def plotar_grafico_media():
    fit = [individuos.fitness for individuos in melhores_individuos]
    plt.plot(geracoes_grafico, media_fitness, color='green')
    plt.plot(geracoes_grafico, fit, color='red')
    plt.xlabel('Gerações')
    plt.ylabel('Fitness')
    plt.title('Média do Fitness e o melhor indivíduo a cada geração')
    plt.grid(True)
    plt.xticks(range(0, len(geracoes_grafico), 1))
    plt.yticks(range(0, 8000, 1000))
    plt.grid(which='minor', axis='both', linestyle=':', linewidth='0.5', color='gray')
    plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(500))
    plt.xlim(0, geracoes)
    plt.ylim(0, 8000)
    plt.plot(geracoes_grafico, fit, label='Melhor Indivíduo', color='red')
    plt.plot(geracoes_grafico, media_fitness, label='Média da População', color='green')
    plt.legend()
    plt.show()

#Plota o gráfico da população toda
def plotar_grafico_geracao(populacao, ax):
    ax.clear()# Limpa a figura atual
    
    x = [individuos.x for individuos in populacao]
    y = [individuos.y for individuos in populacao]
    fitness = [individuos.fitness for individuos in populacao]
    
    melhor_individuo = fitness.index(max(fitness))
    
    x_melhor = x.pop(melhor_individuo)
    y_melhor = y.pop(melhor_individuo)
    fitness_melhor = fitness.pop(melhor_individuo)
    
    ax.scatter(x, y, fitness, c=fitness, cmap='viridis')
    
    ax.scatter(x_melhor, y_melhor, fitness_melhor, color='red')
    
    ax.set_xlim([0, 10])
    ax.set_ylim([0, 20])
    ax.set_zlim([0, 8000])
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Fitness')
    
    ax.set_title(f"Gráfico da geração {len(geracoes_grafico)-1}")
    
    plt.draw()  # Desenha o gráfico
    plt.pause(TEMPO)  # Pausa para permitir a atualização do gráfico
    
    return ax
    
#Janela do gráfico
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.show(block=False)

    
#Em populacao1 serão guardados todos os indivíduos da atual geração
#Em populacao2 serão guardados os melhores individuos e os filhos da geração atual
#Em melhores_individuos serão guardados os melhores indivíduos de cada geração
#Em media_fitness serão guardadas as médias do fitness de cada uma das gerações 
populacao1 = []
populacao2 = []
melhores_individuos = []
media_fitness = []
#Apenas para plotar o gráfico
geracoes_grafico = [0]

#Gerando a geração 0 de indivíduos e guardando o melhor
for i in range(0, num_individuos):
    populacao1.append(individuos(rand_x(),rand_y()))

#Guardando a média dos individuos e o melhor
melhores_individuos.append(elitismo(populacao1))
media_fitness.append(media(populacao1))

#Gráfico
ax = plotar_grafico_geracao(populacao1, ax)
plt.pause(TEMPO)
    
#Gerando a primeira geração em diante
for j in range(geracoes):
    #Será o eixo x do gráfico
    geracoes_grafico.append(j+1)
    #Primeiro, é escolhido o melhor indivíduo da geração, para passar ele para a próxima
    populacao2.append(elitismo(populacao1))
    #Depois é feito o cruzamento 
    for i in range(math.ceil((len(populacao1) - INDIVIDUOS_ELITISMO) / 2)):
        filho1, filho2 = cruzamento()
        populacao2.append(filho1)
        populacao2.append(filho2)
    
    #Guardando a média dos individuos
    media_fitness.append(media(populacao2))
    
    #Gráfico
    ax = plotar_grafico_geracao(populacao2, ax)   
    
    #Guardando o melhor individuo da geração
    melhores_individuos.append(elitismo(populacao2))
    
    #Apaga a geração anterior
    populacao1.clear()
    
    #Copia os individuos da população 2 para população 1
    populacao1 = list(populacao2)
    
    #Apaga população 2, pois ela foi copiada para a população 1
    populacao2.clear()
    
    #E recomeça tudo novamente, caso não tenha chegado no critério de parada
        
#Printanto no terminal os melhores fitness de cada geração        
print("\nMelhores indivíduos de cada geração\n")
for i in range(len(melhores_individuos)):
    print("Geração {:>2}: \tx:{:<6.3f}  \ty:{:<6.3f} \tfit:{:<10.3f} \t\tMedia Fitness: {:<10.3f}".format(i, melhores_individuos[i].x, melhores_individuos[i].y, melhores_individuos[i].fitness, media_fitness[i]))

#Printando o fitness do melhor indivíduo
print("\nO melhor fitness de todas as gerações foi {}".format(max(melhores_individuos, key=lambda x: x.fitness).fitness))

#Plotando o gráfico do fitness médio
plt.show()
plotar_grafico_media()