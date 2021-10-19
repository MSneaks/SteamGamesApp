from django.shortcuts import render
from django.http import HttpResponse
import requests
# Create your views here.
def index(request):
    return render(request, 'landingpage.html')

def projects(request):
    return render(request, 'projects.html')

def huffman(request):
    return render(request, 'huffman.html')

def steamfriends(request):
    return render(request, 'sf.html')

def steamGames(request):
    if request.method == "POST":
        steamID1 = request.POST["steamID1"]
        steamID2 = request.POST["steamID2"]
    numbers = {"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0,"0":0}
    verify1="Good Input"
    verify2="Good Input"
    requestURL1=""
    requestURL2=""
    response1={}
    response2={}
    result1 = ""
    result2 = ""
    common_games = []
    if len(steamID1)!=17:
        verify1 = "Bad Input"
    for i in range(len(steamID1)):
        if steamID1[i] not in numbers:
            verify1 = "Bad Input"
    if len(steamID2)!=17:
        verify2 = "Bad Input"
    for i in range(len(steamID2)):
        if steamID2[i] not in numbers:
            verify2 = "Bad Input"
    if verify1 == "Good Input":
        requestURL1 ="http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="+yourSteamAPIKey+"&steamid=" + steamID1 +"&format=json/"
        response1=requests.get(requestURL1).json()
        if (response1['response'].get('games')==None):
            result1 = "Nothing here"
        else:
            response1 =response1['response']['games']
            result1 = "We Exist!"
    if verify2 == "Good Input":
        requestURL2 ="http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="+yourSteamAPIKey+"&steamid=" + steamID2 +"&format=json/"
        response2=requests.get(requestURL2).json()
        if (response2['response'].get('games')==None):
            result2 = "Nothing here"
        else:
            response2 =response2['response']['games']
            result2 = "We Exist!"
    if result2 == "We Exist!" and result1 == "We Exist!":
        apps =requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2").json()
        appids = apps['applist']["apps"]
        appIDName ={}
        for i in appids:
            appIDName[i['appid']] = i['name']
        player1games = {}
        for i in response1:
            player1games[i['appid']] = 0
        for j in response2:
            if j['appid'] in player1games:
                if j['appid'] in appIDName:
                    common_games.append(appIDName[j['appid']])
        common_games.sort()
    context = {
    'common_games' : common_games,
    "verify1":verify1,
    "verify2":verify2,
    "result1":result1,
    "result2":result2,
    }
    #{'response': response},
    return render(request,'steamGames.html',context)
