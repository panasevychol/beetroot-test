from urllib2 import urlopen
import json
import os

from .constants import GAME_API_URL, PLATFORMS_KEYS


GAMES_INFO = None

def download_games_data(**get_options):
    url = GAME_API_URL
    for key,value in get_options.items():
        url += '&%s=%s' % (key, value)

    return json.loads(urlopen(url).read())

def download_all_games_info():
    games_info = []
    print('Downloading games info')

    for platform_key in PLATFORMS_KEYS:
        games_downloaded, games_total = 0, None

        while games_downloaded != games_total:
            games_data = download_games_data(platform=platform_key,
                                             offset=games_downloaded)
            games_info += games_data['results']

            # Use the code below if you don't need to save all game info

            # for game in games_data['results']:
            #     games_info.append({
            #         'name': game['name'],
            #         'original_release_date': game.get('original_release_date'),
            #         'platforms': [platform.get('abbreviation')
            #                       for platform in game.get('platforms', [])]
            #     })

            if not games_total:
                games_total = games_data['number_of_total_results']
            games_downloaded += games_data['number_of_page_results']

            print('Downoading %s %%' %
                  int((games_downloaded / float(games_total) * 100)))

    print('Download complete')
    return games_info

def get_all_games_info():
    if GAMES_INFO:
        return GAMES_INFO
    elif os.path.exists('games_info.json'):
        with open('games_info.json') as f:
            games_info = json.loads(f.read())
    else:
        with open('games_info.json', 'w') as f:
            games_info = download_all_games_info()
            f.write(json.dumps(games_info))

    global GAMES_INFO
    GAMES_INFO = games_info
    return GAMES_INFO

def find_games(keywords_str):
    keywords = keywords_str.lower().split(' ')
    found_games = []

    for game_info in get_all_games_info():
        if any(keyword in game_info['name'].lower() for keyword in keywords):
            found_games.append(game_info)

    return found_games
