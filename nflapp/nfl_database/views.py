from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Teams
from .models import Players
from django.conf import settings
from nfl_database.test import test_print
from nfl_database.scrapeESPN import getRoster
import json
from django.core import serializers

def index(request):

    teams = Teams.objects.all()
    context = {
        'teams': teams
    }
    print ("loaded page")

    return render(request,'nfl_database/index.html', context)

def team_info(request,id):
    teams = Teams.objects.all()
    team = Teams.objects.get(id=id)
    roster = Players.objects.filter(team_id=id)
    print(len(roster))
    context = {
        'teams' : teams,
        'team' : team,
        'roster': roster,
    }
    print("team_info = "+team.name)
    return render(request,'nfl_database/team_info.html', context)

def update_players(request):
    text = "player db updated"
    teams = Teams.objects.all()
    for team in teams:
        print(team.espn_link)
        players = getRoster(team.espn_link)
        for player_id in players:
            print(player_id+"\t"+players[player_id])
            player, created = Players.objects.update_or_create(
                espnid = player_id,
                defaults = {
                'name' : players[player_id],
                'position' : '',
                'team_id' : team.id,
                'image' : 'http://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/'+player_id+'.png&w=350&h=254'
                }
            )

    return HttpResponse(text)

def show_players(request,id):
    team = Teams.objects.get(id=id)
    text = ("getting players . . ."+team.city+" "+team.name)
    roster = getRoster(team.espn_link)
    for player in roster:
        print(player+"\t"+roster[player])
    return HttpResponse(text)

def event(request):
    p = (settings.BASE_DIR+"/static/nfl_teams.csv")
    file_object  = open(p, "r")
    file_contents = file_object.readlines()
    print ("contents of nfl csv read")
    for line in file_contents:
        line_contents = line.strip().split(',')
        city = line_contents[0]
        name = line_contents[1]
        logo = line_contents[2]
        espn = line_contents[3]
        color1 = line_contents[4]
        color2 = line_contents[5]

        team, created = Teams.objects.update_or_create(
            city = city,
            name = name,
            defaults = {
                'color1' : color1,
                'color2' : color2,
                'logo_img' : "img/logos/"+logo,
                'background_img' : '',
                'espn_link' : espn,
            }
        )
        print(str(created)+" "+name)
    text = "updated"
    print(text)
    return HttpResponse(text)

def event2(request):
    text="hello"
    test_print(text)
    return HttpResponse(text)

def event3(request):
    data = serializers.serialize('json', Teams.objects.all())
    return HttpResponse(json.dumps(data), content_type='application/json')

