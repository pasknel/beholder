from core.models import Person, Post, Tag, Connection, Place, Tip

__author__ = 'b0x'

class Utils:

    def get_user(self, user, name, profile_picture):
        person = None
        try:
            person = Person.objects.get(login = user)
        except Person.DoesNotExist:
            person = Person(login = user, name = name, profile_picture = profile_picture)
            person.save()
        return person

    def get_place(self, pid, name, checkins):
        place = None
        try:
            place = Place.objects.get(id = pid)
        except Place.DoesNotExist:
            place = Place(id = pid, name = name, checkins = checkins)
            place.save()
        return place

    def save_post(self, pid, person, created_time, photo, text, latitude, longitude, network):
        post = Post(id = pid, author = person, dateOfCreation = created_time, photo = photo, text = text[:120], latitude = latitude, longitude = longitude, network = network)
        post.save()
        return post

    def save_tags(self, tags, post):
        for tag in tags:
            t = Tag(tag = tag)
            t.save()
            t.post.add(post)

    def save_connection(self, post, type, text = ""):
        connection = Connection(post = post, type = type, text = text)
        connection.save()
        return connection

    def save_tip(self, tid, author, place, text, dateOfCreation):
        tip = Tip(id = tid, author = author, place = place, text = text, dateOfCreation = dateOfCreation)
        tip.save()
        return tip