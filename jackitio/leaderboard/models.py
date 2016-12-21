'''
Database Models
'''

import datetime
from django.utils import timezone
from django.db import models

class Leaderboard(models.Model):
    '''
    Database model for a leaderboard entry strip
    '''
    user = models.CharField(max_length=10, default="")
    score = models.IntegerField()
    playtime = models.IntegerField()
    deaths = models.IntegerField()

    def was_published_recently(self):
        '''
        Returns if the score was published in the last day
        '''
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return "{} - {}".format(self.user, self.score)
