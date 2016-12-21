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
    Super secure leaderboard submissions. (it's not though)
    '''
    user = data.get("user", None)
    playtime = data.get("playtime", None)
    score = data.get("score", None)
    deaths = data.get("deaths", None)
    levels = data.get("levels_completed", None)

    if user is None or playtime is None or score is None or deaths is None\
    or levels is None:
        return False

    '''
    Super secure (not really...at all)
    '''
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
        return False

    if comp == code:
        return True
    return False

def cheated(data):
    '''
    Attempt to find cheaty cheaters
    '''
    sys.path.append(REPO_BASE_DIR)
    # TODO: Check things like. Do they have more points than possible?
    # did they finish way to fast?
    # did they finish more levels than possible?
    # etc...
    return False, ""

def get_leaderboard():
    '''
    Get all the entries in the leaderboard
    '''
    try:
        ret = Leaderboard.objects.order_by("-score", "deaths", "playtime")
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
        c = d.get("game_id", None)

        if c is not None:
            if validate_code(d, c):
                try:
                    form = LeaderboardForm(request.POST)
                    leader = form.save(commit=False)
                    leader.cheated, leader.cheated_reason = cheated(d)
                    leader.save()
                except BaseException as e:
                    print("Error creating form from post data: ", str(e))
                    print("Post data: ", request.POST)
            else:
                print("Validation failed")

    return HttpResponse("Success!")
