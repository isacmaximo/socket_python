import socket
import json

#definindo o host (local nesse exemplo)
HOST = 'localhost'
#definindo uma porta
PORT = 60000
#variável que representa o socket
#socket trabalhando com IPV4 (primeiro parâmetro) e TCP [fluxo] (segundo parâmetro)
sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#passando o host e a porta
sckt.bind((HOST, PORT))
#colocando o socket em modo de esculta
sckt.listen()
#print para saber em que parte do código está (aguardando uma conexão)
print("Aguardando conexão de um cliente...")

#conexão e endereço são o retorno da aceitação do socket
connection, address = sckt.accept()
#print para mostar o endereço que está conectado
print("Conectado em: ", address)

#json de ítens 
itens = [{
    "itens":[
        {
        "nome": "Arroz",
        "valor": 5
        },
        {
        "nome": "Macarrão",
        "valor": 4
        },
        {
        "nome": "Feijão",
        "valor": 6
        },
        {
        "nome": "Carne",
        "valor": 25
        },
        {
        "nome": "Frango",
        "valor": 18
        },
        {
        "nome": "Suco",
        "valor": 6
        },
        {
        "nome": "Refrigerante",
        "valor": 5
        },
    ]
    ,
}]

#laço para que tenha a recepção e tranmissão dos dados até que se encerre 
while True:
    
    #dados que serão recebidos (teraão tamanho máximo de 100MB)
    data = connection.recv(102400)
    recebido = data.decode("utf-8") #dados recebidos serão codificados em utf-8
    res = json.loads(recebido) #dado recebido se tranforma em json novamente

   

    #cada função espera a resposta (json recebido do lado do cliente)
    #no json tem uma chave "c" que representa o comando

    #legenda de comando:
    #l : listar produtos
    #f : fechar conexão
    #e: erro

    #após cada função o servidor enviará novamente json em formato de bytes
    #no lado do cliente os bytes serão deserializados e serão um json novamente



    #comando de fechar
    if res["c"] == "f":
        jsonDict = {"c": "f"}
        data = json.dumps(jsonDict)
        connection.send(bytes(data, encoding="utf-8"))
        print("Fechando a conexão...")
        connection.close() #fechamento da conexão
        break #quebra do laço e o script do servidor termina

    #comando não esperado pelo servidor
    elif res["c"] == "e":
        jsonDict = {
                    "msg": "Entrada inválida!",
                    }
        data = json.dumps(jsonDict)
        connection.send(bytes(data, encoding="utf-8"))
    
    #função de mostrar a lista de ítens 
    elif res["c"] == "l":
        print('\nLista de compras solicitada!')
        jsonDict = {"lista": itens, "t": len(itens[0]["itens"])}
        data = json.dumps(jsonDict)
        connection.send(bytes(data, encoding="utf-8"))
    
    #função de salvar a lista de compras em um txt
    elif res["c"] == "s":
        print('\nSalvando lista de compras...')
        lista_compras = res["carrinho"]

        arquivo = open("compras.txt", "a")
        arquivo.writelines("==========================================")
        for i in range(len(lista_compras)):
            arquivo.writelines("\nProduto: " + lista_compras[i]["produto"])
            arquivo.writelines("\nQuantidade: " + str(lista_compras[i]["quantidade"]))
            arquivo.writelines("\nValor (unidade): " + "R$" + str(lista_compras[i]["valor"]))
            arquivo.writelines("\n")
        
        arquivo.writelines("\n\nTotal" + " R$" + str(res["total"]))
        arquivo.close()
        

    


