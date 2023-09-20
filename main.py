from agents.edital_lookup_agent import lookup as edital_lookup_agent

import os
import env

os.environ["OPENAI_API_KEY"] = env.APIKEY
os.environ["CURL"] = env.CURL

requisito = "editais ou licitações de pesquisa e desenvolvimento de software e hardware"

lista_de_editais = edital_lookup_agent(requisito = requisito)

print(lista_de_editais)