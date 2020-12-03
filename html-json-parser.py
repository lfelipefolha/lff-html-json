from html.parser import HTMLParser
from fastapi import FastAPI, HTTPException
import requests, json

class Parser(HTMLParser):
  def __init__(self):  # Acrescenta membros adicionais à classe:
    self.p = [] # -> pilha das migalhas do caminho
    self.a = [] # -> árvore do documento
    # lista de tags que não precisam ser fechadas:
    self.void ="area, base, br, col, embed, hr, img, input, link, meta, param, source, track, wbr".split(", ")
    # flag de raw text
    self.raw = False
    super().__init__() # chama o construtor herdado

  def desce(self,a=None,p=None): # desce recursivamente a árvore até o nó ativo:
    if a is None: a, p = self.a, self.p # se não tem argumentos, começa na raiz
    return self.desce(a[-1][p[0]],p[1:]) if p else a # recursão

  def handle_starttag(self, tag, ats):# Ao encontrar tag abrindo (ats = atributos):
    if tag in self.void: return # ignorar void tags
    if tag=='script' or tag=='style': # entrar em modo raw text
        self.raw=True
        return
    self.desce().append({tag:[]}) # acrescenta nó à árvores;
    self.p.append(tag) # deixa uma migalha no caminho;
    if ats: # se há atributos especiais, acrescenta-os ao nó ativo.
      self.desce().append({'@'+k:v for k,v in ats}) # ex.: "@atributo : valor"
  def handle_endtag(self, tag): # Ao encontrar tag fechando:
    if tag in self.void: return # ignorar void tags
    if tag=='script' or tag=='style': # sair do modo raw text
        self.raw=False
        return
    expected=self.p.pop() # sobe a árvore (come uma migalha e volta o caminho).
    try: assert tag==expected
    except:print(f'expected "{expected}" ; got "{tag}"')
  def handle_data(self, data): # Ao encontrar conteúdo textual:
    if not (data.isspace() or self.raw): # garante que não é vazio e que não é raw text
      self.desce().append(data.strip()) # deleta espaço extra e acrescenta ao nó ativo:


app = FastAPI()

@app.post("/")
def parse(url: str =''):
    if not url: raise HTTPException(status_code=400, detail="No url submitted")
    r = requests.get(url)
    p = Parser()
    try:
        p.feed(r.text)
        response = p.a
        return {"json":response}
    except:
        raise HTTPException(status_code=504, detail="Internal server error")

