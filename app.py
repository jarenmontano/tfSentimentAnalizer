import datetime
import textwrap
import IPython
from flask import Flask, render_template, request, session
import requests
# https://requests.readthedocs.io/en/latest/
import json

import google.generativeai as genai
import os
os.environ["API_KEY"] = "AIzaSyAWapJjEQeBq4X86Yexu8xfaHwD1uXElpA"

app = Flask(__name__)

# configuring the AI
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])
# for the markdown of gemini text
from IPython.display import display
from IPython.display import Markdown

app.secret_key = '192b9bdd22ab9ed4d12e236c87afcb9a393ec15f71bbf5dc987d54727823bcbf'





#           Basic structure of the return json
# {
#       ""id"": 53,
#       ""sport_id"": 1,
#       ""country_id"": 1161,
#       ""venue_id"": 8909,
#       ""gender"": ""male"",
#       ""name"": ""Celtic"",
#       ""short_code"": ""CEL"",
#       ""image_path"": ""https://cdn.sportmonks.com/images/soccer/teams/21/53.png"",
#       ""founded"": 1888,
#       ""type"": ""domestic"",
#       ""placeholder"": false,
#       ""last_played_at"": ""2023-08-01 18:30:00""
#     },


#  using for my div to send back and forth
    # <div class="card" style="width: 18rem;">
    # <img src="..." class="card-img-top" alt="...">
    #   <div class="card-body">
    #     <h5 class="card-title">Card title</h5>
    #     <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
    #     <a href="#" class="btn btn-primary">Go somewhere</a>
    #   </div>
    # </div>

#this is a helper funtion from the gemini api docs // fixes the responses bad formating "SUPOSEDLY"
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))




# could get removed do not need it anymore
def get_from_one(jsonstring):
    imagepath = jsonstring["image_path"]
    name = jsonstring["name"]
    shortcode = jsonstring["short_code"]
    founded = jsonstring["founded"]
    # used for debugging
    # print('imagepath  :' + imagepath + "  " + 'name  :' + name + '  shortcode  :' + shortcode)
    return imagepath, name, shortcode, founded

def format_history(history):
    history_formatted_string = '''<h1>Chat History<h1> <p class="fs-5">'''
    for chat_item in history:
        history_formatted_string += chat_item + "</br></br>"
    history_formatted_string += "</p>"
    return history_formatted_string

def get_from_all(jsonstring):
    htmlstring = '''<div class="card-group">'''
    print("currently in get_all_from")
    for team in jsonstring["data"]:
        #now to use this data to create the divs
        htmlstring += '''<div class="col pt-5">'''
        htmlstring +='''<div class="card bg-dark border-light" style="width: 18rem;"> '''
        htmlstring +='''<img src="'''
        htmlstring += team["image_path"]
        htmlstring += '''" class="card-img-top" alt="'''
        htmlstring += team["image_path"]
        htmlstring += '''">''' 
        htmlstring += '''<div class="card-body">'''
        htmlstring += '''<h5 class="card-title">'''
        htmlstring += team["name"]
        htmlstring += '''</h5>'''
        htmlstring += '''<p class="card-text"> This team was founded in '''
        htmlstring += str(team["founded"])
        htmlstring += '''.</p>'''
        htmlstring += '''<a href="#" class="btn btn-primary">More Details</a>'''
        htmlstring += '''</div>'''
        htmlstring += '''</div>'''
        htmlstring += '''</div>'''
      
    htmlstring += '''</div>'''
    return htmlstring

def get_players_from_server():
    try:
        # this url is to my local host in .net
        url = "http://localhost:5029/mainresourses"
        response = requests.get(url)
        # print(response.text)
        jsonstring = json.loads(response.text)
        #return get_from_one(jsonstring)
        soccer_teams = get_from_all(jsonstring)
        return soccer_teams
        
        
    except:
        soccer_teams= "failed"
        
        return soccer_teams
        # name = "FAILURE"
        # return name


# failure didn't work
# def get_players():
#     if(len(htmlstring) < 40):
#        soccer_team=  get_players_from_server()
#        return soccer_team
#     return htmlstring




def use_ai(prompt):
    prompt_response = ""
    
    prompt_response = chat.send_message(prompt)
    # the one below is for one time, the one above is for chat(MULTIPLE with History)
    # prompt_response = model.generate_content(prompt)
    #print(prompt_response.text)
    

    return prompt_response.text


@app.route("/")
def index():
    prompt = "Give me information on the Soccer Teams St. Johnstone"
    soccer_teams= get_players_from_server()
    #prompt_response = use_ai(prompt)
    # name = get_players()
    return render_template("index.html", soccer_teams=soccer_teams)
    # return render_template("index.html",  name=name)

@app.route("/" , methods=["POST"])
def return_ai_response():
    session["history"] = []
    user_prompt = request.form["user_prompt"]
    session["history"].append(user_prompt)
    print(user_prompt)
    prompt_response =  use_ai(user_prompt)
    session["history"].append(prompt_response)
    #print(IPython.core.formatters.HTMLFormatter(to_markdown(prompt_response)))
    print(prompt_response)
    history = format_history(session["history"]) 
    soccer_teams= get_players_from_server()
    return render_template("index.html", soccer_teams=soccer_teams, history=history)



if __name__ == "__main__":
    app.run(debug=True)


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=1)
    session.modified = True
    