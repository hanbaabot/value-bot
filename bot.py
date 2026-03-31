import requests
import time
from scipy.stats import poisson
from telegram import Bot

ODDS_API_KEY = "API_KEY_BURAYA"
TELEGRAM_TOKEN = "TOKEN_BURAYA"
CHAT_ID = "CHAT_ID_BURAYA"

bot = Bot(token=TELEGRAM_TOKEN)

def get_odds():
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={ODDS_API_KEY}&regions=eu&markets=h2h"
    return requests.get(url).json()

def match_prob(home_xg, away_xg):
    home_win = draw = away_win = 0
    for i in range(5):
        for j in range(5):
            p = poisson.pmf(i, home_xg) * poisson.pmf(j, away_xg)
            if i > j:
                home_win += p
            elif i == j:
                draw += p
            else:
                away_win += p
    return home_win, draw, away_win

def run():
    matches = get_odds()
    for m in matches:
        try:
            home = m['home_team']
            away = m['away_team']
            odds = m['bookmakers'][0]['markets'][0]['outcomes']

            home_odds = odds[0]['price']
            draw_odds = odds[1]['price']
            away_odds = odds[2]['price']

            home_p, draw_p, away_p = match_prob(1.5, 1.2)

            for name, prob, odd in [
                ("HOME", home_p, home_odds),
                ("DRAW", draw_p, draw_odds),
                ("AWAY", away_p, away_odds),
            ]:
                value = (prob * odd) - 1
                if value > 0.05:
                    msg = f"{home} vs {away} | {name} | Value: {value:.2f}"
                    bot.send_message(chat_id=CHAT_ID, text=msg)
        except:
            pass

while True:
    run()
    time.sleep(3600)
