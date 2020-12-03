# html-json-parser

## Instalação no Heroku
Lançar no Heroku conectando com o GitHub e fazer deploy manualmente.
O Heroku carrega tudo a partir do `requirements.txt` e do `Procfile`.
O `Procfile` contém:
``web: gunicorn -w 1 -k uvicorn.workers.UvicornWorker html-json-parser:app``
Isso lança um worker dyno. atenção para maiúscula em "Procfile"
## Instalação local
Após clonar o repositório, executar:
``pip3 install -r requirements.txt``
Para lançar a aplicação:
``uvicorn --port 5000 --host 127.0.0.1 html-json-parser:app``

## Notas sobre a implementação
* O script implementa a API usando a biblioteca `FastAPI`.
* O script roda em uma instância de `uvicorn`.
* Para fazer a request foi usada a biblioteca `requests`.
* O script implementa um parser de HTML a partir da classe` HTMLParser` da biblioteca padrão Python.
* São ignoradas as tags tipo "void" e o conteúdo rawtext marcado por tags `style` e `script`.
* O parser monta a árvore do documento em sua variável-mempro `a`.
* O parser mantém o caminho para o nó atual na variável-membro `p`, que é tratada como uma pilha.
* O método `desce` percorre recursivamente a árvore, seguindo o caminho guardado em `p` e retorna o nó ativo.
* Cada tag de abertura acrescenta um filho ao nó ativo, e o filho passa a ser o nó ativo.
* Cada tag de fechamento sobe um nível da árvore (o novo nó ativo passa a ser o pai do nó ativo anterior.)

