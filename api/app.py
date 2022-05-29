from cgitb import text
from flask import Flask, jsonify
import os
import json
import datetime as dt
import pytz
from flask_pymongo import PyMongo


#Configure Flask & Flask-PyMongo:
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://superuser:pass1234@mongodb:27017/admin" 
pymongo = PyMongo(app)



def resource_not_found(e):
    """
    An error-handler to ensure that 404 errors are returned as JSON.
    """
    return jsonify(error=str(e)), 404

def format_date(date_time_str):
    date_time_obj = dt.datetime.strptime(date_time_str, '%Y-%m-%d')
    timezone = pytz.timezone('UTC')
    timezone_date_time_obj = timezone.localize(date_time_obj) 
    return timezone_date_time_obj  

def format_time(date_time_str):
    date_time_obj = dt.datetime.strptime(date_time_str, '%Y-%m-%d')
    timezone = pytz.timezone('UTC')
    timezone_date_time_obj = timezone.localize(date_time_obj) 
    return timezone_date_time_obj


@app.route('/')
def hello():
    return ("Welcome to Fz Sports JSON API") 

@app.route('/api/team')
def get_teams():
    list_of_teams = pymongo.db.teams.find()
  #  return jsonify(, ensure_ascii=False)
    return json.dumps(list(list_of_teams), ensure_ascii=False)

@app.route('/api/teams/:<idTeam>/players')
def get_players(idTeam):
    list_of_active = pymongo.db.players.find({"team_id": idTeam})
    list_of_disabled = pymongo.db.disabled_players.find({"team_id": idTeam})
    players =  list(list_of_active) + list(list_of_disabled)
    for i in players: 
        if i["fechaNacimiento"]:
            i["fechaNacimiento"] = format_date(i["fechaNacimiento"])
        if i["horaNacimiento"]:
            i["horaNacimiento"]= format_time(i["horaNacimiento"])
    return json.dumps(list(players), ensure_ascii=False, default=str)

@app.route('/api/teams/players/:<position>')
def get_position(position):
    position = position.capitalize()
    positions = pymongo.db.players.find({"rol.text": position})
    positions_list =  list(positions)
    for i in positions_list: 
        if i["fechaNacimiento"]:
            i["fechaNacimiento"] = format_date(i["fechaNacimiento"])
        if i["horaNacimiento"]:
            i["horaNacimiento"]= format_time(i["horaNacimiento"])
    return json.dumps(list(positions_list), ensure_ascii=False)

    
    

