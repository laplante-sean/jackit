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
    score = models.IntegerField()
    playtime = models.FloatField()
    deaths = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

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
        fields = ['user', 'score', 'playtime', 'deaths']
