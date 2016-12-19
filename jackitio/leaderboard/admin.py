'''
Admin interface for our comic site
'''

from django.contrib import admin
from .models import Leaderboard

admin.site.register(Leaderboard)
