from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import time
load_dotenv()



options = webdriver.FirefoxOptions()

options.add_argument("--headless")

driver = webdriver.Firefox(options=options)


driver.get("https://twitter.com")

def login(username, password):
    # go to /login directly
    driver.get("https://twitter.com/login")

    username_input = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"]'))
    )

    username_input.send_keys(username)

    username_input.send_keys(Keys.ENTER)

    password_input = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
    )

    password_input.send_keys(password)

    password_input.send_keys(Keys.ENTER)



user_bio = ""
def change_bio(playing_now): 
    global driver
    profile = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="AppTabBar_Profile_Link"]'))
    )
    
    profile_link = profile.get_attribute("href")
    driver.get(profile_link)

    edit_profile = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="editProfileButton"]'))
    )
    edit_profile.click()

    while True:
        try:
            global user_bio
            # click on second element with class "css-901oao r-1awozwy r-1nao33i r-6koalj r-37j5jr r-1inkyih r-16dba41 r-135wba7 r-bcqeeo r-13qz1uu r-qvutc0"
            # which is the bio, use until presence of element located etc etc etc
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.NAME, 'displayName')))
            
            # bio_input should be the first textarea [0]
            bio_input = driver.find_elements(By.CSS_SELECTOR, 'textarea')[0]
            bio_input.click()

            if (user_bio == ""):
                user_bio = bio_input.get_attribute("value")
            if (playing_now != ""):
                bio_input.send_keys(Keys.CONTROL + "a")
                bio_input.send_keys(Keys.DELETE)
                bio_input.send_keys('🎶 ' + playing_now + "\n\n" + user_bio)
            else:
                bio_input.send_keys(Keys.CONTROL + "a")
                bio_input.send_keys(Keys.DELETE)
                bio_input.send_keys(user_bio)
            break
        except Exception as e:
            continue

    button = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="Profile_Save_Button"]'))
    )

    button.click()


    driver.implicitly_wait(3)

sp = None
def start_spotify():
    global sp
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                                               client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                                               redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
                                               scope=os.getenv("SPOTIFY_SCOPE")))


def get_current_playing():
    global sp
    current_playing = sp.currently_playing()
    if current_playing is None:
        return None
    
    artist = current_playing["item"]["artists"][0]["name"]
    song = current_playing["item"]["name"]

    return artist + " - " + song

currently_playing = ""
last_played = ""

erased = False
def verify_currently_playing_and_update_username():
    global erased
    global sp
    global currently_playing
    global last_played
    current_playing_response = get_current_playing()
    if current_playing_response is None:
        if not erased:
            change_bio("")
            erased = True
        return
    
    if currently_playing != current_playing_response:
        erased = False
        change_bio(current_playing_response)
        last_played = currently_playing
        currently_playing = current_playing_response

    
    return

start_spotify()

username = os.getenv("TWITTER_USERNAME")
password = os.getenv("TWITTER_PASSWORD")
login(username, password)

while True:
    print("Checking...")
    verify_currently_playing_and_update_username()
    time.sleep(5)

