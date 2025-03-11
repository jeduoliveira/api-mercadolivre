# API MercadoLIvre

este script tem como função acessa o MLB de um item via python

## Premissa

Ter git e python instalados

## 1. Clonar  repositório

        git clone https://github.com/jeduoliveira/api-mercadolivre

## 2. Criar aplicativo no MercadoLivre


Criar um aplicativo no link https://developers.mercadolivre.com.br/devcenter/, clique no botão **Criar Nova aplicação**. 

Coloque um nome, nome curto, a descrição em uma imagem qualquer.


Na proxima pagina, coloque https://holderjs.com no campo **URIs de redirect**. Selecione osEscopos **(read, offiline access e write)**. Depois busque por items e selecione o que for necessário. No campo **URL de retornos de chamada de notificação** também coloque a URL https://holderjs.com 


## 3. Configurar variáveis de ambiente

Crie um arquivo **.env** copiando de **.env.example**

Com o arquivo .env e o aplicativo criado, Edite o aplicativo e pegue as informações do **ID do aplicativo** e a **Chave secreta**, coloque no arquivo .env nas variaveis CLIENT_ID e CLIENT_SECRET.


Agora execute uma vez o comando abaixo 
    
        python3 api.py --MLB MLB2037467576

## 4. Autenticacao no MercadoLivre

Vai ocorrer um erro e o script vai mostrar uma URL, pegue essa URL e abra em um browser, ao fazer a autorização com o mercadolivre você será redirecionado para uma URL **https://holderjs.com?code=**

Pegue o valor do code e coloquei no arquivo **.env** na variavel **CODE**

agora execute novamente o comando abaixo

        python3 api.py --MLB MLB2037467576


## 5. Resilucao de Problemas

Se por um acaso para de retornar o conteudo json, apague o valor da variavel **REFRESH_TOKEN** e refaca o processo **4.**