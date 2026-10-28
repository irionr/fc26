from django.db import models
from django.utils import timezone


class Player(models.Model):
    name = models.CharField('nome', max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Match(models.Model):
    ONE_V_ONE = '1v1'
    TWO_V_TWO = '2v2'
    MODES = [(ONE_V_ONE, '1 contro 1'), (TWO_V_TWO, '2 contro 2')]

    mode = models.CharField('modalità', max_length=3, choices=MODES, default=ONE_V_ONE)
    scheduled_at = models.DateTimeField('data/ora', default=timezone.now)
    played = models.BooleanField('giocata', default=False)
    score1 = models.PositiveSmallIntegerField('gol squadra 1', null=True, blank=True)
    score2 = models.PositiveSmallIntegerField('gol squadra 2', null=True, blank=True)
    team1 = models.ManyToManyField(Player, related_name='matches_as_team1')
    team2 = models.ManyToManyField(Player, related_name='matches_as_team2')

    class Meta:
        ordering = ['-scheduled_at', '-id']

    @property
    def points_per_winner(self):
        return 3

    @property
    def winners(self):
        """Giocatori vincitori; lista vuota se non giocata o pareggio."""
        if not self.played or self.score1 is None or self.score2 is None:
            return []
        if self.score1 > self.score2:
            return list(self.team1.all())
        if self.score2 > self.score1:
            return list(self.team2.all())
        return []

    def __str__(self):
        t1 = ' + '.join(p.name for p in self.team1.all())
        t2 = ' + '.join(p.name for p in self.team2.all())
        return f'{t1} vs {t2}'
