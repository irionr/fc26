from django import forms

from .badges import badges
from .models import Match, Player


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name']


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['mode', 'scheduled_at', 'team1', 'team2']
        widgets = {
            'scheduled_at': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'team1': forms.CheckboxSelectMultiple,
            'team2': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scheduled_at'].input_formats = ['%Y-%m-%dT%H:%M']
        b = badges()
        for f in ('team1', 'team2'):
            self.fields[f].label_from_instance = lambda p: f'{b[p.id][0]} {p.name}'

    def clean(self):
        data = super().clean()
        t1, t2, mode = data.get('team1'), data.get('team2'), data.get('mode')
        if t1 is None or t2 is None or mode is None:
            return data
        size = 2 if mode == Match.TWO_V_TWO else 1
        if len(t1) != size or len(t2) != size:
            raise forms.ValidationError(
                f'In modalità {mode} ogni squadra deve avere esattamente {size} giocator{"i" if size > 1 else "e"}.')
        if set(t1) & set(t2):
            raise forms.ValidationError('Un giocatore non può stare in entrambe le squadre.')
        return data


class ResultForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['score1', 'score2']

    def clean(self):
        data = super().clean()
        if data.get('score1') is None or data.get('score2') is None:
            raise forms.ValidationError('Inserisci entrambi i punteggi.')
        return data
