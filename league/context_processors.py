from .badges import MIN_GAMES, PROVISIONAL, TIERS, badges


def player_badges(request):
    return {'player_badges': badges(), 'badge_tiers': TIERS,
            'badge_provisional': PROVISIONAL, 'badge_min_games': MIN_GAMES}
