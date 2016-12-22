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

def validate_code(data, code):
    '''
    Validate code
    '''
    user = data.get("user", None)
    playtime = data.get("playtime", None)
    score = data.get("score", None)
    deaths = data.get("deaths", None)
    levels = data.get("levels_completed", None)

    if user is None or playtime is None or score is None or deaths is None\
    or levels is None or code is None:
        return False

    try:
        result = {}
        code_obj = marshal.load(open(os.path.join(REPO_BASE_DIR, "gen.dump"), "rb"))

        # pylint: disable=W0122
        exec(code_obj, {
            'user':user,
            'playtime':playtime,
            'score':score,
            'deaths':deaths
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
        except BaseException as e:
            print("Error creating form from post data: ", str(e))
            print("Post data: ", request.POST)

    return HttpResponse("Success!")
