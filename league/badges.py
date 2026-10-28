from .models import Match, Player

MIN_GAMES = 5

# (% minima, icona, titolo) in ordine crescente; sotto MIN_GAMES partite il livello è provvisorio
PROVISIONAL = ('🥚', 'Esordiente')
TIERS = [
    (0, '🐣', 'Matricola'),
    (25, '⚽', 'Titolare'),
    (45, '🔥', 'In forma'),
    (60, '⭐', 'Stella'),
    (75, '👑', 'Leggenda'),
]


def tier_for(games, pct):
    if games < MIN_GAMES:
        return PROVISIONAL
    icon, title = TIERS[0][1:]
    for min_pct, i, t in TIERS:
        if pct >= min_pct:
            icon, title = i, t
    return icon, title


def badges():
    """{player_id: (icona, titolo, dettaglio)}, con la stessa % dei punti disponibili della classifica."""
    stats = {p.id: [0, 0] for p in Player.objects.all()}  # [punti, partite]
    for m in Match.objects.filter(played=True).prefetch_related('team1', 'team2'):
        for team, gf, ga in ((m.team1.all(), m.score1, m.score2), (m.team2.all(), m.score2, m.score1)):
            pts = m.points_per_winner if gf > ga else (1 if gf == ga else 0)
            for p in team:
                stats[p.id][0] += pts
                stats[p.id][1] += 1
    out = {}
    for pid, (pts, games) in stats.items():
        pct = round(100 * pts / (3 * games)) if games else 0
        icon, title = tier_for(games, pct)
        out[pid] = (icon, title, f'{pct}% su {games} partite')
    return out
