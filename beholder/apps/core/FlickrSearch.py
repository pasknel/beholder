from datetime import datetime
from core.Utils import *
import flickrapi, json, time
from beholder import settings

class FlickrSearch:

    def __init__(self):
        self.api_key = settings.FLICKR_API_KEY
        self.api_secret = settings.FLICKR_API_SECRET
        self.flickr = None

    def getPhotoInfo(self, photo_id):
        data = self.flickr.photos.getInfo(photo_id = photo_id, format = 'parsed-json')
        created_time = datetime.fromtimestamp(int(data['photo']['dateuploaded'])).strftime('%Y-%m-%d %H:%M:%S')
        print("\t[*] Created time: %s" % created_time)
        tags = []
        for tag in data['photo']['tags']['tag']:
            tags.append(tag['raw'])
        print('\t[*] Tags: %s' % tags)
        return (created_time, tags)

    def getPerson(self, owner):
        data = self.flickr.people.getInfo(user_id = owner, format = 'parsed-json')
        username = data['person']['username']['_content']
        path_alias = data['person']['path_alias']
        iconserver = data['person']['iconserver']
        iconfarm = data['person']['iconfarm']
        nsid = data['person']['nsid']
        profile_picture = "http://farm%s.staticflickr.com/%s/buddyicons/%s.jpg" % (iconfarm, iconserver, nsid)
        fullname = data['person']['realname']['_content']

        print('\t[*] Login: %s' % username)
        print('\t[*] Path alias: %s' % path_alias)
        print('\t[*] Full name: %s' % fullname)
        print('\t[*] Profile picture: %s' % profile_picture)

        return (path_alias, fullname, profile_picture)

    def parsePhoto(self, photo, latitude, longitude):
        title = photo['title']
        farm = photo['farm']
        server = photo['server']
        photo_id = photo['id']
        secret = photo['secret']
        owner = photo['owner']
        url = "https://farm%s.staticflickr.com/%s/%s_%s_n.jpg" % (farm, server, photo_id, secret)

        print('[+] Photo ID: %s' % photo_id)
        print('\t[*] URL: %s' % url)
        print('\t[*] Title: %s' % title)

        (user, name, profile_picture) = self.getPerson(owner)
        utils = Utils()
        person = utils.get_user(user, name, profile_picture)

        (created_time, tags) = self.getPhotoInfo(photo_id)
        p = utils.save_post(photo_id, person, created_time, url, title, latitude, longitude, "Flickr")
        utils.save_tags(tags, p)
        print('')

    def search(self, latitude, longitude, max_posts, radius):
        self.flickr = flickrapi.FlickrAPI(self.api_key, self.api_secret, format = 'parsed-json')
        data = self.flickr.photos.search(has_geo = 1, lat = latitude, lon = longitude, radius = radius/1000.0, page = 1)
        total = data['photos']['total']
        photos = data['photos']['photo']
        perpage = data['photos']['perpage']
        page = int(data['photos']['page'])
        pages = int(data['photos']['pages'])
        while max_posts > 0 and pages > 0:
            print("Total of photos: %d" % len(photos))
            for photo in photos:
                try:
                    self.parsePhoto(photo, latitude, longitude)
                except Exception as e:
                    print(e)
            page += 1
            pages -= 1
            max_posts -= len(photos)
            if pages > 0:
                data = self.flickr.photos.search(has_geo = 1, lat = latitude, lon = longitude, radius = radius/1000.0, page = page)
                photos = data['photos']['photo']