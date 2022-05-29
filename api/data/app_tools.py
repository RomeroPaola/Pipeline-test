from sre_constants import JUMP
from xml.dom.minidom import Element
from pandas import array
import requests
import json
import xmltodict
import pymongo
import bson 
import os
from bson.raw_bson import RawBSONDocument


URL = "https://fx-nunchee-assets.s3.amazonaws.com/data/sports.xml"

def get_data():
    response = requests.get(URL)
    with open('feed.xml', 'wb') as file:  #downloading the xml file
        file.write(response.content)
        file.close()
   
    with open("feed.xml", encoding="UTF-8") as xml_file:   
         data_dict = xmltodict.parse(xml_file.read())   
            # data_dict” is the variable in which I loaded the XML data after converting it to dictionary datatype.    
            # Convert the xml_data into a dictionary and store it in a variable 
         json_data = json.dumps(data_dict,  ensure_ascii= False, indent=4).replace("@id", "_id").replace("#", "").replace("@", "") #taking the json object and returning a string
         xml_file.close()        

    with open("data.json", "w", encoding="UTF-8") as json_file: 
        json_file.write(json_data)#write the json data to output file
        json_file.close()     

def setup_db(teams_list, players_list, disabled_list):
    
     # let’s create a MongoClient using the pymnogo library to the running instance
    uri = "mongodb://superuser:pass1234@127.0.0.1:27017/?authSource=admin&authMechanism=SCRAM-SHA-256"  
    myclient = pymongo.MongoClient(uri)
    db = myclient["admin"]
  
   # plantel = db["plantelEquipo"]
    teams = db["teams"]
    players = db["players"]
    disabled = db["disabled_players"]
    
    teams.insert_many(teams_list)
    players.insert_many(players_list)
    disabled.insert_many(disabled_list)
                
     
#connecting to database

def process_data():
    equipos = []
    active_players = []
    released_players= []
        
    with open('data.json', "r", encoding="UTF-8") as file:
     
        file_data = json.load(file)
           
        for k, v in file_data.items():
           for i, y in v.items():
               if i == "equipo":
                   for equipo in y:
                        for any in equipo["jugadores"]['jugador']:
                            any["team_id"]= equipo['_id']
                            active_players.append(any)

                        if equipo["jugadoresDadosBaja"]['cant']!= "0":
                                if equipo["jugadoresDadosBaja"]['cant']== "1":
                                    equipo["jugadoresDadosBaja"]['jugador']["team_id"]= equipo['_id']
                                    released_players.append(equipo["jugadoresDadosBaja"]['jugador'])

                                else:    
                                    for val in equipo["jugadoresDadosBaja"]['jugador']:
                                        val["team_id"]= equipo['_id']
                                        released_players.append(val) 
                       
                        del equipo["jugadores"]    
                        del equipo["jugadoresDadosBaja"]              
                        equipos.append(equipo)
                     
    with open("teams.json", "w", encoding="UTF-8") as teams:
        teams.write(json.dumps(equipos, ensure_ascii= False, indent=4))
        teams.close()

    with open("players.json", "w", encoding="UTF-8") as players:
        players.write(json.dumps(active_players, ensure_ascii= False, indent=4))
        players.close()

    with open("disabled_players.json", "w", encoding="UTF-8") as disabled:
        disabled.write(json.dumps(released_players, ensure_ascii= False, indent=4))
        disabled.close()

   # setup_db(equipos,active_players,released_players)                     
