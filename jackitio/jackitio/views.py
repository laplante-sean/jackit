'''
Main views for the website. Redirects to leaderboard app
'''

from django.shortcuts import redirect

def index(_): #Passing _ variable to avoid linting warning
    '''
    Redirect to leaderboard
    '''
    return redirect("/leaderboard/", permanent=True)
