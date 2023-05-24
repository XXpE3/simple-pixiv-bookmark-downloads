import os
import feedparser
import requests
import configparser
from bs4 import BeautifulSoup
from retrying import retry

# Load or create settings from cfg file
config = configparser.ConfigParser()
if os.path.exists('Settings.cfg'):
    config.read('Settings.cfg')
else:
    config.add_section('Settings')
    RSS_URL = 'https://rsshub.app/pixiv/user/bookmarks/'
    RSS_URL += input("Please enter your Pixiv numerical ID: ")
    config.set('Settings', 'RSS_URL', RSS_URL)
    
    DOWNLOAD_DIR = input("Please enter the download folder, default is ./downloaded_images: ")
    DOWNLOAD_DIR = DOWNLOAD_DIR if DOWNLOAD_DIR else 'downloaded_images'
    config.set('Settings', 'DOWNLOAD_DIR', DOWNLOAD_DIR)
    
    DOWNLOADED_FILE = input("Please enter the file to save the download history, default is ./downloaded_images.txt: ")
    DOWNLOADED_FILE = DOWNLOADED_FILE if DOWNLOADED_FILE else 'downloaded_images.txt'
    config.set('Settings', 'DOWNLOADED_FILE', DOWNLOADED_FILE)
    
    with open('Settings.cfg', 'w') as configfile:
        config.write(configfile)

RSS_URL = config.get('Settings', 'RSS_URL')
DOWNLOAD_DIR = config.get('Settings', 'DOWNLOAD_DIR')
DOWNLOADED_FILE = config.get('Settings', 'DOWNLOADED_FILE')

@retry(stop_max_attempt_number=5, wait_fixed=5000)
def download_image(url):
    response = requests.get(url, stream=True)
    response.raise_for_status()  # This will raise a HTTPError if the status is 4xx or 5xx

    if response.headers['Content-Type'].startswith('image/'):
        filename = os.path.join(DOWNLOAD_DIR, url.split("/")[-1])
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f'Downloaded {url}')
    else:
        print(f"URL {url} does not appear to be an image. Skipping.")

def main():
    # Ensure download directory exists
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Load already downloaded images
    if os.path.exists(DOWNLOADED_FILE):
        with open(DOWNLOADED_FILE, 'r') as f:
            downloaded_images = f.read().splitlines()
    else:
        downloaded_images = []

    # Parse the RSS feed
    feed = feedparser.parse(RSS_URL)

    # Loop over each entry in the feed
    for entry in feed.entries:
        # Use BeautifulSoup to find image URLs
        soup = BeautifulSoup(entry.description, 'html.parser')
        img_tags = soup.find_all('img')

        for img in img_tags:
            url = img.get('src')
            if url.endswith('.png') or url.endswith('.jpg'):
                if url not in downloaded_images:
                    try:
                        download_image(url)
                        downloaded_images.append(url)
                        with open(DOWNLOADED_FILE, 'a') as f:
                            f.write(url + '\n')
                    except requests.exceptions.RequestException as e:
                        print(f"Error downloading {url}: {e}")

if __name__ == "__main__":
    main()
