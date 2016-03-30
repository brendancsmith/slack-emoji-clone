import os
import sys
import requests
import shutil

from collections import Counter
from bs4 import BeautifulSoup

# ----

team_name = os.getenv('SLACK_TEAM')
cookie = os.getenv('SLACK_COOKIE')

# ----

url = "https://{}.slack.com/customize/emoji".format(team_name)

headers = {
    'Cookie': cookie,
}

# ----

def fetch_emoji_info(url):
    # Fetch the form first, to generate a crumb.
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    emoji_rows = soup.find_all('tr', class_='emoji_row')

    get_emoji_url = lambda row: row.find('span', 'emoji-wrapper')['data-original']
    emoji_urls = [get_emoji_url(row) for row in emoji_rows]

    get_emoji_name = lambda row: row.find_all('td', 'align_middle')[1].text.strip().strip(':')
    emoji_names = [get_emoji_name(row) for row in emoji_rows]

    return zip(emoji_names, emoji_urls)


emoji_info = fetch_emoji_info(url)
print(len(emoji_info), "emojis")


# ----

dest = team_name
if os.path.exists(dest):
    shutil.rmtree(dest)
os.makedirs(dest)

for emoji_name, emoji_url in emoji_info:
    response = requests.get(emoji_url, stream=True)

    emoji_imgtype = os.path.splitext(emoji_url)[1]
    filename = emoji_name + emoji_imgtype

    #import pdb
    #pdb.set_trace()

    filepath = os.path.join(dest, filename)

    with open(filepath, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
