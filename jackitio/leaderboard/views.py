'''
Main view for the leaderboard app
'''

from django.http import HttpResponse
from django.template import loader

from .models import Leaderboard

def get_leaderboard():
    '''
    Get all the entries in the leaderboard
    '''
    try:
        return {'leaderboard': Leaderboard.objects.order_by("-score")}
    except BaseException:
        return {'leaderboard': []}

def index(request):
    '''
    Home page and load most recent comic
    '''
    template = loader.get_template('leaderboard/index.html')
    context = get_leaderboard()
    return HttpResponse(template.render(context, request))
