'''
Main view for the leaderboard app
'''
import os
import sys
import marshal

from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from jackitio.settings import REPO_BASE_DIR
from .models import Leaderboard, LeaderboardForm


# TODO: Populate with level flags
FLAGS = [
    "flag{TEST0}",
    "flag{TEST1}",
    "flag{TEST2}",
    "flag{TEST3}",
    "flag{TEST4}",
    "flag{TEST5}",
    "flag{TEST6}",
    "flag{TEST7}",
    "flag{TEST8}"
]


def validate_code(data, code):
    '''
    Validate code
    '''
    user = data.get("user", None)
    playtime = data.get("playtime", "0.0").strip()
    score = int(data.get("score", 0))
    deaths = int(data.get("deaths", 0))
    levels_completed = int(data.get("levels_completed", 0))
    level_completed = data.get("level_completed", None)

    if user is None or playtime is None or score is None or deaths is None\
    or levels_completed is None or code is None:
        return False

    level = None
    try:
        result = {}
        if level_completed is not None:
            level_completed = int(level_completed)

            from jackit.levels import (
                Level_01, Level_02, Level_03, Level_04,
                Level_05, Level_06, Level_07, Level_08
            )

            levels = [
                Level_01, Level_02, Level_03, Level_04,
                Level_05, Level_06, Level_07, Level_08
            ]

            print("Level completed: ", level_completed)
            level = levels[level_completed]
            print("Map: ", level._map)

        code_obj = marshal.load(open(os.path.join(REPO_BASE_DIR, "gen3.dump"), "rb"))

        # pylint: disable=W0122
        exec(code_obj, {
            'user': user,
            'playtime': playtime,
            'total_points': score,
            'deaths': deaths,
            'levels_completed': levels_completed,
            'level_completed': level_completed,
            'completed_level': level
        }, locals())

    except BaseException as e:
        print(e)
        return False

    comp = result.get("code", None)
    if not comp:
        print("No code!")
        return False

    if comp == code:
        return True
    return False


def validate(data):
    '''
    Make sure everything looks tasty
    '''
    sys.path.append(REPO_BASE_DIR)

    if not validate_code(data, data.get("game_id", None)):
        return True, "Invalid game_id"

    playtime = data.get("playtime", None)
    if playtime is None:
        return True, "No playtime provided"

    try:
        float(playtime)
    except ValueError:
        return True, "Invalid float for playtime {}".format(playtime)

    if float(playtime) < 1:
        return True, "Playtime too short {}".format(playtime)

    try:
        prt = playtime.split('.')[1]
        if len(prt) < 9:
            return True, "Invalid playtime {}".format(playtime)
    except IndexError:
        return True, "Invalid playtime {}".format(playtime)

    levels_completed = data.get("levels_completed", None)
    if levels_completed is None:
        return True, "No levels completed"

    try:
        int(levels_completed)
    except ValueError:
        return True, "Invalid int for levels_completed {}".format(levels_completed)

    if int(levels_completed) > 8:
        return True, "Too many levels completed {}".format(levels_completed)

    if int(levels_completed) < 2 and int(data.get("score", 0)) > 8:
        return True, "Too many points {}".format(data.get("score", 0))

    if int(data.get("score", 0)) > 1092:
        return True, "Too many points {}".format(data.get("score", 0))

    return False, ""


def get_leaderboard():
    '''
    Get all the entries in the leaderboard
    '''
    try:
        ret = Leaderboard.objects.order_by("-score", "deaths", "playtime", "-levels_completed")
        if len(ret) > 50:
            ret = ret[:50]
        return {'leaderboard': ret}
    except BaseException:
        return {'leaderboard': []}


def index(request):
    '''
    Home page and load most recent leaderboard
    '''
    template = loader.get_template('leaderboard/index.html')
    context = get_leaderboard()
    return HttpResponse(template.render(context, request))


@csrf_exempt
def submit(request):
    '''
    Submit a score
    '''
    if request.POST:
        d = request.POST.dict()
        try:
            form = LeaderboardForm(request.POST)
            leader = form.save(commit=False)
            leader.cheated, leader.cheated_reason = validate(d)
            leader.save()

            if leader.cheated and leader.cheated_reason != "Invalid game_id":
                return HttpResponse("Great job cheater: " + FLAGS[0])

        except BaseException as e:
            print("Error creating form from post data: ", str(e))
            print("Post data: ", request.POST)
    else:
        return HttpResponse("Invalid method")

    return HttpResponse("Success!")


@csrf_exempt
def lvlcomplete(request):
    '''
    Submit a level completion
    '''
    d = {}
    if request.POST:
        d = request.POST.dict()
        try:
            cheated, cheated_reason = validate(d)
        except BaseException as e:
            print("Error creating form from post data: ", str(e))
            print("Post data: ", request.POST)
            return HttpResponse("Internal error. Could not get level flag")
    else:
        return HttpResponse("Invalid method")

    if cheated:
        print("Cheated on level: ", cheated_reason)
        return HttpResponse("No cheating on levels! Maybe try to cheat on score submission?")

    flag = None
    level_completed = d.get("level_completed", None)
    if level_completed is not None:
        level_completed = int(level_completed) + 1
        try:
            flag = FLAGS[level_completed]
        except:
            return HttpResponse("You messed up the level number or something...")

    print("Success: ", flag)
    return HttpResponse("Great job: " + flag)
