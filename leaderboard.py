import os
import sys
import requests

from collections import Counter
from bs4 import BeautifulSoup

team_name = os.getenv('SLACK_TEAM')
cookie = os.getenv('SLACK_COOKIE')

url = "https://{}.slack.com/customize/emoji".format(team_name)

headers = {
    'Cookie': cookie,
}

# Fetch the form first, to generate a crumb.
r = requests.get(url, headers=headers)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

author_cells = soup.find_all(class_='author_cell')
authors = [cell.find('a').text.strip() for cell in author_cells]

authorCount = Counter(authors)
leaderboard = authorCount.most_common()

print('Emoji Leaderboard')
print('-----------------')
for name, count in leaderboard:
    print('{}: {}'.format(name, count))
