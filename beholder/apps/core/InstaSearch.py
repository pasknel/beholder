from core.Utils import Utils
from core.models import Person, Post, Tag, Connection
from datetime import datetime
from beholder import settings
import requests
import time

__author__ = 'b0x'

class InstaSearch:

    def __init__(self):
        self.client_id = settings.INSTAGRAM_CLIENT_ID
        self.client_secret = settings.INSTAGRAM_CLIENT_SECRET
        self.redirect_uri = settings.INSTAGRAM_REDIRECT_URI
        self.url = "https://api.instagram.com/oauth/access_token"

    def get_token(self, code):
        post = {}
        post["client_id"] = self.client_id
        post["client_secret"] = self.client_secret
        post["grant_type"] = "authorization_code"
        post["redirect_uri"] = self.redirect_uri
        post["code"] = code

        response = requests.post(self.url, data=post)
        data = response.json()
        access_token = data["access_token"]
        print('[*] Access token received: %s' % access_token)
        return access_token

    def parsePost(self, post):
        # View pretty json - http://jsonformatter.curiousconcept.com/
        print(post)

        pid = post["id"]
        user = post["user"]["username"]
        name = post["user"]["full_name"]
        tags = post["tags"]
        caption = post["caption"]
        location = post["location"]
        created_time = datetime.fromtimestamp(int(post["created_time"])).strftime('%Y-%m-%d %H:%M:%S')
        images = post["images"]
        photo = images["standard_resolution"]["url"]
        profile_picture = post["user"]["profile_picture"]
        likes = post["likes"]
        comments = post["comments"]

        text = ""
        if caption:
            text = caption["text"]

        if location:
            latitude = location["latitude"]
            longitude = location["longitude"]

            print("[*] Post ID: %s" % pid)
            print('[*] User: %s' % user)
            print('[*] Full name: %s' % name)
            print('[*] Date of creation: %s' % created_time)
            print('[*] Tags:  %s' % tags)
            print('[*] Latitude: %s - Longitude: %s' % (latitude, longitude))
            print('[*] Photo: %s' % (photo))
            print('[*] Text: %s' % text)
            print('')

            utils = Utils()
            person = utils.get_user(user, name, profile_picture)
            p = utils.save_post(pid, person, created_time, photo, text, latitude, longitude, "Instagram")
            utils.save_tags(tags, p)

            if len(likes["data"]) > 0:
                c = utils.save_connection(p, 0)
                for like in likes["data"]:
                    person_who_likes = utils.get_user(like["username"], like["full_name"], like["profile_picture"])
                    c.user.add(person_who_likes)
                    print('[+] Like from: %s' % (person_who_likes.login))

            if comments["count"] > 0:
                for comment in comments["data"]:
                    c = utils.save_connection(p, 1, comment["text"])
                    person_who_comments = utils.get_user(comment["from"]["username"], comment["from"]["full_name"], comment["from"]["profile_picture"])
                    c.user.add(person_who_comments)
                    print('[+] Comment from: %s' % person_who_comments.login)
            print('')
        return created_time

    def search(self, code, lat, lng, max_posts, radius):
        print("[*] Starting Instagram Geolocation Search")
        print("[*] Latitude: %s" % lat)
        print("[*] Longitude: %s" % lng)
        print("[*] Total of posts: %d" % max_posts)
        print("[*] Radius: %s meters" % radius)
        access_token = self.get_token(code)

        if access_token:
            timestamp = int(time.time())

            while max_posts > 0:
                url = (
                    "https://api.instagram.com/v1/media/search?\
                    lat=%s&\
                    lng=%s&\
                    access_token=%s\
                    &distance=%s\
                    &max_timestamp=%s" % (lat, lng, access_token, radius, timestamp)
                ).replace(" ", "")

                try:
                    response = requests.get(url)
                    parser = response.json()
                    posts = parser["data"]
                    print('[*] Total found: %d\n' % len(posts))

                    for post in posts:
                        self.parsePost(post)

                    timestamp -= 432000
                    max_posts -= len(posts)
                except Exception as e:
                    print("-" * 30)
                    print('[!] EXCEPTION IN INSTAGRAM SEARCH')
                    print(e)
                    print("-" * 30)