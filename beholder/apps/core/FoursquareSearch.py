from _ast import UAdd
from core.models import Person
from datetime import datetime
from dateutil import parser
from core.Utils import *
from beholder import settings
import foursquare

__author__ = 'b0x'

class FoursquareSearch:

    def __init__(self):
        self.client_id = settings.FOURSQUARE_CLIENT_ID
        self.client_secret = settings.FOURSQUARE_CLIENT_SECRET
        self.foursquare = None

    def auth(self):
        try:
            self.foursquare = foursquare.Foursquare(client_id = self.client_id, client_secret = self.client_secret)
            return True
        except Exception as e:
            print(e)
        return False

    def parse_photo(self, photo):
        photoId = photo['id']
        url = photo['prefix'] + 'original' + photo['suffix']
        createdAt = datetime.fromtimestamp(int(photo["createdAt"])).strftime('%Y-%m-%d %H:%M:%S')

        user = photo['user']
        userId = user['id']
        firstName = user['firstName']
        lastName = user['lastName']
        profilePicture = user['photo']['prefix'] + 'original' + user['photo']['suffix']

        print('\t\t[+] Photo Id: %s' % photoId)
        print('\t\t[+] Photo url: %s' % url)
        print('\t\t[+] Created at: %s' % createdAt)
        print('\t\t[+] User Id: %s' % userId)
        print('\t\t[+] User Name: %s %s' % (firstName, lastName))
        print('\t\t[+] Profile Picture: %s' % profilePicture)
        print('')

    def get_photos(self, venue_id):
        try:
            data = self.foursquare.venues.photos(VENUE_ID = venue_id, params = {'limit' : 100})
            photos = data['photos']
            items = photos['items']
            print('\t[*] Photos:')
            for photo in items:
                self.parse_photo(photo)
        except Exception as e:
            print(e)

    def parse_tip(self, place, tip):
        tipId = tip['id']
        text = tip['text']
        createdAt = datetime.fromtimestamp(int(tip['createdAt'])).strftime('%Y-%m-%d %H:%M:%S')

        user = tip['user']
        userId = user['id']
        firstName = user['firstName']
        lastName = user['lastName']
        name = "%s %s" % (firstName, lastName)
        photo = user['photo']
        profilePicture = photo['prefix'] + 'original' + photo['suffix']

        utils = Utils()
        person = utils.get_user(userId, name, profilePicture)
        tip = utils.save_tip(tid=tipId, author=person, place=place, text=text, dateOfCreation=createdAt)

        print('\t\t[+] Tip Id: %s' % tipId)
        print('\t\t[+] Created at: %s' % createdAt)
        print('\t\t[+] User ID: %s' % userId)
        print('\t\t[+] Full Name: %s' % name)
        print('\t\t[+] Profile Picture: %s' % profilePicture)
        print('\t\t[+] Text: %s' % text)
        print('')

    def get_tips(self, place):
        try:
            tips = self.foursquare.venues.tips(VENUE_ID = place.id)
            items = tips['tips']
            print('\t[*] Tips')
            for tip in items['items']:
                self.parse_tip(place, tip)
        except Exception as e:
                print(e)

    def parse_venue(self, venue):
        venueId = venue['id']
        name = venue['name']
        checkinsCount = venue['stats']['checkinsCount']

        print('[*] Venue: %s' % name)
        print('\t[+] Checkins Count: %s' % checkinsCount)
        print('\t[+] Venue ID: %s' % venueId)

        utils = Utils()
        place = utils.get_place(pid=venueId, name=name, checkins=checkinsCount)
        #place.tip_set.count()

        self.get_tips(place)
        #self.get_photos(venueId)

        print('')

    def get_venues(self, latitude, longitude, radius):
        try:
            result = self.foursquare.venues.search(params = {'ll' : '%f,%f' % (float(latitude), float(longitude)), 'radius' : radius})
            venues = result['venues']
            return venues
        except Exception as e:
            print(e)
        return None

    def search(self, latitude, longitude, radius):
        if self.auth():
            venues = self.get_venues(latitude, longitude, radius)
            for venue in venues:
                self.parse_venue(venue)