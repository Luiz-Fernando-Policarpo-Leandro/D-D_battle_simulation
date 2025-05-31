# import names
import json
import random
from creature import Creature
from battle import Battle

_names = [
    "José", "Maria", "João", "Ana", "Pedro", "Lucas", "Carlos", "Fernanda", "Paula", "Rafael",
    "Juliana", "Felipe", "Beatriz", "Gustavo", "Carla", "Rodrigo", "Camila", "Renato", "Tatiane", "Sérgio",
    "Bruna", "Amanda", "Eduardo", "Monique", "Danilo", "Isabela", "Victor", "Camila", "Natália", "Thiago"
]
_lastnames = [
    "Silva", "Santos", "Oliveira", "Souza", "Costa", "Pereira", "Almeida", "Rodrigues", "Lima", "Martins",
    "Gomes", "Ferreira", "Ribeiro", "Melo", "Carvalho", "Barbosa", "Cavalcanti", "Nascimento", "Machado", "Araujo",
    "Campos", "Pinto", "Moreira", "Fonseca", "Vieira", "Monteiro", "Siqueira", "Tavares", "Chaves", "Dias"
]



with open("creatures.json", "r", encoding="utf-8") as f:
     baseData = json.load(f)


giant_ape_data = baseData["Giant ape"]
commoner_data = baseData["Commoner"]

giant_ape = Creature(**giant_ape_data)
giant_apeb = Creature(**giant_ape_data)
giant_apec = Creature(**giant_ape_data)
commners = []


for c in range(100):
    new_commoner = commoner_data.copy()
    new_commoner["name"] = f"Commoner n{c+1} {random.choice(_names)} {random.choice(_lastnames)}"

    commners.append(Creature(**new_commoner))

simulation = Battle([commners,[giant_ape, giant_apeb],[giant_apec]])
simulation.start