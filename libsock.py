import socket
import json
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

HOST = 'localhost' #host pode ser uma porta ou um nom
PORT = 60000 #mesma porta que o servidor está escutando

#variável que representa o socket
#socket trabalhando com IPV4 (primeiro parâmetro) e TCP [fluxo] (segundo parâmetro)
sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#função de conectar
def conectar():
    
    #tentativa de conectar
    try:
        sckt.connect((HOST, PORT)) #socket precisa de um host e uma porta para estabelecer a conexão
        messagebox.showinfo("Informação de Conexão", "Conexão com o servidor estabelecida!") #mensagem exibindo que deu certo a conexão

        #botão de encerrar conexão aparecerá pois a conexão já está estabelecida
        BtEnc = Button(LadoEsquerdo, text = "ENCERRAR", font = ("Arial", 12), bg = "goldenrod2",width = 10, cursor = "hand2", command=desconectar)
        BtEnc.place(x = 10, y = 60)

        #botão de listar ítens ficará visível após a conexão ser estabelecida
        BtListar = Button(LadoEsquerdo, text = "LISTAR", font = ("Arial", 12), bg = "goldenrod2",width = 10, cursor = "hand2", command=listar)
        BtListar.place(x = 10, y = 110)

        #botão de conectar não existirá pois a conexão já está estabelecida 
        BtCon.destroy()


    #caso o servidor esteja indisponível
    except:
        messagebox.showerror("Informação de conexão", "Servidor indisponível no momento!")  #a mensagem informará o problema
    
    
#função de desconectar
def desconectar():
    jsonDict = {"c": "f"} #enviará para o servidor um json com um comando de fechar
    data = json.dumps(jsonDict) #serializando o json (transformando em uma string)
    sckt.sendall(bytes(data, encoding="utf-8")) #enviando o json como bytes na codificação utf-8
    messagebox.showinfo("Informação de Conexão", "Conexão com o servidor encerrada!") #mensagem de informação
    sckt.close() #término da conexão
    janela.destroy() #término do programa (fecha tudo)
    

#função de listar todos os ítens e exibir outras funcionalidades na tela
def listar():
    
    jsonDict = {"c": "l"} #enviará para o servidor um json com um comando de listar
    data = json.dumps(jsonDict) #serializando o json 
    sckt.sendall(bytes(data, encoding="utf-8")) #enviando o json como bytes na codificação utf-8

    data = sckt.recv(1024) #recepção de dados (bytes) com buffer de 1MB (1024 bytes)
    recebido = data.decode("utf-8") #deserializando o json na codificação utf-8
    resposta = json.loads(recebido) #tranformando os dados recebidos em json novamente

    carrinho = [] #lista que representará o carrinho
    
    options = () #tupla de opções de código do ítem (será carragada logo abaixo)
    options2 = ("1","2","3","4","5","6","7","8","9","10") #tupla de opções de quantidade de ítens


    for i in range(resposta["t"]):   #laço que irá percorrer a chave de tamanho da lista de ítens do json recebido
        options = options + (str(i),) #a tupla de opções de de código receberá os ídices (que são os códigos)


    exibir = "\nLegenda:\nCÓDIGO - NOME - VALOR\n\n" #string inicial para exibir a lista de ítens

    for i in range (len(resposta["lista"][0]["itens"])): #laço que percorrerá toda a lista de ítens recebido através do json
        #string que está recebendo  código nome e valor unitário de cada ítem
        exibir = exibir + str(i) + " - " + resposta["lista"][0]["itens"][i]["nome"] + " - " + "R$" + str(resposta["lista"][0]["itens"][i]["valor"]) + "\n"
    
    #Texto(UI) com todos os ítens (recebidos da string "exibir")
    ListaLabel = Label(LadoDireito, text = exibir, font = ("Arial", 12), bg = "gray15", fg = "white", justify="left")
    ListaLabel.place(x = 10, y = 5)

    #Texto(UI) de "código"
    CodigoLabel = Label(LadoDireito, text = "Código: ", font = ("Arial", 12), bg = "gray15", fg = "white", justify="left")
    CodigoLabel.place(x = 10, y = 250)

    #Texto(UI) de "quantidade"
    QtdLabel = Label(LadoDireito, text = "Quantidade: ", font = ("Arial", 12), bg = "gray15", fg = "white", justify="left")
    QtdLabel.place(x = 10, y = 300)

    variable = StringVar() #variável que representará o código escolhido
    cb= ttk.Combobox(janela, textvariable= variable, width=2) #menu de opções de código dos ítens
    cb['values']= options #valores do menu recebem a tupla opções
    cb.current(0) #menu de opções  de código de ítem é setado com o primeiro ítem (no caso é 0)
    cb['state']= 'readonly' #menu de opções é apenas leitura
    #alocação na tela
    cb.pack()
    cb.place(x = 250, y = 250)

    variable2 = StringVar() #variável que representará a quantidade escolhida
    cb2= ttk.Combobox(janela, textvariable= variable2, width=2) #menu de opções de quantidade dos ítens
    cb2['values']= options2 #valores do menu recebem a tupla opções2
    cb2.current(0) #menu de opções de quantidade de ítem é setado com o primeiro ítem (no caso é 1)
    cb2['state']= 'readonly'  #menu de opções é apenas leitura
     #alocação na tela
    cb2.pack()
    cb2.place(x = 250, y = 300)

    
    #função de adicionar no carrinho
    def adc_carrinho():
        produto =  int(variable.get()) #codigo do produto é pego pela varável do menu de códigos do produto
        quantidade = int(variable2.get()) #quantidade do produto é pego pela varável do menu de quantidade do produto

        #função para verificar se um ítem já existe no carrinho
        def  pesquisar():
            for i in range(len(carrinho)): #laço irá percorrer todo o carrinho de compras
                if carrinho[i]["produto"] == produto: #caso o produto que está no carrinho é o mesmo que está tentando adicionar
                    carrinho[i]["quantidade"] = str(carrinho[i]["quantidade"] + quantidade) #apenas atualiza a quantidade desse valor
                    return 1 #retorno 1 representa que já foi alterado
            return 0 #retorno 0 representa que o ítem não existe no carrinho e será adicionado
        
        valor_pesquisa = pesquisar() #variável que pega o retorno da função pesquisar (valor 0 ou 1)

        if(valor_pesquisa == 0): #se o valor da pesquisa for igual a zero
            #então a lista de carrinho recebe um json (dicionário em python) contendo produto, quantidade e valor
            carrinho.append({
                            "produto": produto,
                            "quantidade": quantidade,
                            "valor": resposta["lista"][0]["itens"][produto]["valor"]
                            })

        #mensagem que informa qual ítem foi adicionado
        messagebox.showinfo("Informação de compra", resposta["lista"][0]["itens"][produto]["nome"] + " adicionado ao carrinho!")

    #botão que tem a função de adiconar ítem ao carrinho
    BtEnviar = Button(LadoDireito, text = "ADICIONAR AO CARRINHO", font = ("Arial", 12), bg = "goldenrod2",width = 25, cursor = "hand2", command= adc_carrinho)
    BtEnviar.place(x = 10, y = 350)

    #lista de ítens recebida pelo json
    lista_itens = resposta["lista"][0]["itens"]

    #funão de mostrar o carrinho
    def mostrar_carrinho():
        itens_carrinho = ["CARRINHO:\n\n"] #string inicial do conteúdo do carrinho
    
        for i in range (len(carrinho)): #laço que percorrerá todo o carrinho para pegar as informações de produto, quantidade e valor que contém np carrinho
            itens_carrinho.append("Produto: " + lista_itens[carrinho[i]["produto"]]["nome"])
            itens_carrinho.append("Quantidade: " + str(carrinho[i]["quantidade"]))
            itens_carrinho.append("Valor unitário: " + "R$" + str(carrinho[i]["valor"]))
            itens_carrinho.append("\n")
            #itens_carrinho = itens_carrinho + "Produto: " + lista_itens[carrinho[i]["produto"]]["nome"] + "\nQuantidade: " + str(carrinho[i]["quantidade"]) + "\nValor unitário: " + "R$" + str(carrinho[i]["valor"]) + "\n"

        #Tela(IU) do carrinho
        janela2 = Toplevel()
        janela2.geometry ( "400x400" ) #dimensões da tela de login
        janela2.title( "Carrinho" ) #título da janela
        janela2.resizable( width  =  False , height  =  False ) #tela não é redimensionável (tamanho fixo)
        
        #UI
        rolagem = Scrollbar(janela2) #Barra de rolagem na tela do carrinho
        rolagem.pack(side = RIGHT, fill = Y) #barra de rolagem posicionada na direita e rolagem na vertical (eixo y)
        #lista de ítens (conteudo)
        TT = Listbox(janela2, yscrollcommand = rolagem.set, font = ("Arial", 14), justify = LEFT)
        #ítens do carrinho serão inseridos na lista de ítens rolável
        for x in itens_carrinho:        
            TT.insert(END, x)
        #lista de ítens 
        TT.pack(side = TOP, fill = BOTH)     
        rolagem.config(command = TT.yview)

        #total dos ítens no carrinho
        valor_total = 0
        for i in range (len(carrinho)):
            valor_total = valor_total + (carrinho[i]["quantidade"] * carrinho[i]["valor"])

        #componente que exibirá o valor total
        Total = Label(janela2, text = "TOTAL: R$" + str(valor_total), font = ("Arial", 16), bg = "gray15", fg = "white", justify="left")
        Total.place(x = 200, y = 300)

    BtMc = Button(LadoDireito, text = "CARRINHO", font = ("Arial", 12), bg = "goldenrod2",width = 10, cursor = "hand2", command=mostrar_carrinho)
    BtMc.place(x = 180, y = 0)






    
#enviando mensagem a quem escuta (servidor)


#parte gráfica (tela principal)
janela  =  Tk () #janela de login
janela.geometry ( "400x400" ) #dimensões da tela de login
janela.title( "Socket Client" ) #título da janela
janela.resizable( width  =  False , height  =  False )

#configuração lado esquerdo
LadoEsquerdo = Frame(janela, width = 120, height = 400, bg = "grey10")
LadoEsquerdo.pack(side = LEFT)

#configuração do lado direito
LadoDireito = Frame(janela, width = 280, height = 400, bg = "grey15")
LadoDireito.pack(side = RIGHT)

#botões do lado esquerdo
BtCon = Button(LadoEsquerdo, text = "CONECTAR", font = ("Arial", 12), bg = "goldenrod2",width = 10, cursor = "hand2", command=conectar)
BtCon.place(x = 10, y = 10)







#loop de eventos para a tela ficar ativa, para a interface funcionar
mainloop()