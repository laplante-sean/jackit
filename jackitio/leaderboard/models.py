'''
Database Models
'''

from django.db import models
from django.forms import ModelForm

class Leaderboard(models.Model):
    '''
    Database model for a leaderboard entry strip
    '''
    user = models.CharField(max_length=50, default="No Name Loser")
    score = models.IntegerField(default=0)
    playtime = models.FloatField(default=0)
    deaths = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    levels_completed = models.IntegerField(default=0)
    cheated = models.BooleanField(default=False)
    cheated_reason = models.CharField(max_length=100, default="")

    def __str__(self):
        return "[{}]: {} - {}".format(self.pub_date, self.user, self.score)

class LeaderboardForm(ModelForm):
    '''
    Handles post data to update the leaderboard
    '''
    class Meta:
        '''
        Info about the model
        '''
        model = Leaderboard
        fields = ['user', 'score', 'playtime', 'deaths', 'levels_completed']
