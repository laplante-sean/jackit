'''
Admin interface for our leaderboard site
'''

from django.contrib import admin
from .models import Leaderboard

admin.site.register(Leaderboard)
