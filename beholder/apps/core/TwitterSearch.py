from _ast import UAdd
from core.models import Person, Post, Tag
from dateutil import parser
from core.Utils import *
from beholder import settings
from twitter import *
import time

__author__ = 'b0x'

class TwitterSearch:

    def __init__(self):
        self.access_key = settings.TWITTER_ACCESS_KEY
        self.access_secret = settings.TWITTER_ACCESS_SECRET
        self.consumer_key = settings.TWITTER_CONSUMER_KEY
        self.consumer_secret = settings.TWITTER_CONSUMER_SECRET
        self.twitter = None

    def auth(self):
        self.twitter = Twitter(auth = OAuth(self.access_key, self.access_secret, self.consumer_key, self.consumer_secret))

    def parsePost(self, post):
        if post["geo"]:
            pid = post["id"]
            user = post["user"]["screen_name"]
            name = post["user"]["name"]
            text = post["text"].encode('ascii', 'replace')
            latitude = post["geo"]["coordinates"][0]
            longitude = post["geo"]["coordinates"][1]
            profile_picture = post["user"]["profile_image_url_https"]
            created_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(post["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
            photo = ""

            tags = []
            for tag in post["entities"]["hashtags"]:
                tags.append(tag["text"])

            print('[+] Tweet ID: %s' % pid)
            print('\t[+] User: %s' % user)
            print('\t[+] Full Name: %s' % name)
            print('\t[+] Date of Creation: %s' % created_time)
            print('\t[+] Latitude: %s' % latitude)
            print('\t[+] Longitude: %s' % longitude)
            print('\t[+] Hashtags: %s' % tags)
            print('\t[+] Text: %s' % text)
            print('')

            utils = Utils()
            person = utils.get_user(user, name, profile_picture)
            p = utils.save_post(pid, person, created_time, photo, text, latitude, longitude, "Twitter")
            utils.save_tags(tags, p)

            return pid

    def search(self, lat, lng, max_posts, radius):
        print("[*] Starting Twitter Geolocation Search")
        print("[*] Latitude: %s" % lat)
        print("[*] Longitude: %s" % lng)
        print("[*] Total of posts: %d" % max_posts)
        print("[*] Radius: %s meters" % radius)
        self.auth()
        last_id = None
        while max_posts > 0:
            query = self.twitter.search.tweets(q = '', geocode = "%s,%s,%fkm" % (lat, lng, radius/1000.0), count = 100, max_id = last_id)
            print("[*] Total of Posts: %d" % len(query["statuses"]))
            for post in query["statuses"]:
                last_id = self.parsePost(post)
            max_posts -= len(query["statuses"])