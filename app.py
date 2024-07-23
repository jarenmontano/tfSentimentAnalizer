from flask import Flask, render_template
import requests
# https://requests.readthedocs.io/en/latest/
import json

app = Flask(__name__)
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


# could get removed do not need it anymore
def get_from_one(jsonstring):
    imagepath = jsonstring["image_path"]
    name = jsonstring["name"]
    shortcode = jsonstring["short_code"]
    founded = jsonstring["founded"]
    # used for debugging
    # print('imagepath  :' + imagepath + "  " + 'name  :' + name + '  shortcode  :' + shortcode)
    return imagepath, name, shortcode, founded


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

def get_players():
    try:
        # this url is to my local host in .net
        url = "http://localhost:5029/mainresourses"
        response = requests.get(url)
        print(response.text)
        jsonstring = json.loads(response.text)
        #return get_from_one(jsonstring)
        soccer_teams = get_from_all(jsonstring)
        return soccer_teams
        
        
    except:
        soccer_teams= "failed"
        
        return soccer_teams
        # name = "FAILURE"
        # return name


@app.route("/")
def index():
    soccer_teams= get_players()
    # name = get_players()
    return render_template("index.html", soccer_teams=soccer_teams)
    # return render_template("index.html",  name=name)

if __name__ == "__main__":
    app.run(debug=True)