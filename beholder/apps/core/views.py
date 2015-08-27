from django.db.models import F, Count
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView,View, DetailView, ListView
from core.FlickrSearch import FlickrSearch
from core.FoursquareSearch import FoursquareSearch
from core.models import Person, Post, Tag, Connection
from core.InstaSearch import *
from core.TwitterSearch import *
from beholder import settings
import json
import time
import random
import requests

# Create your views here.
class Index(TemplateView):
    template_name = "index.html"

class Auth(View):
    client_id = settings.INSTAGRAM_CLIENT_ID
    client_secret = settings.INSTAGRAM_CLIENT_SECRET
    redirect_uri = settings.INSTAGRAM_REDIRECT_URI

    def get(self, request, *args, **kwargs):
        url = "https://api.instagram.com/oauth/authorize/?client_id=%s&redirect_uri=%s&response_type=code" %(
            self.client_id, self.redirect_uri)

        return HttpResponseRedirect(url)

class Finder(View):

    def get(self, requests, *args, **kwargs):
        code = requests.GET.get('code', None)
        return render(self.request, "finder.html", {"code": code})

    def clear_tables(self):
        Connection.objects.all().delete()
        Tag.objects.all().delete()
        Post.objects.all().delete()
        Person.objects.all().delete()
        Tip.objects.all().delete()
        Place.objects.all().delete()
        print('[+] Tables cleared !')

    def post(self, request, *args, **kwargs):
        code = request.POST.get('code', None)
        lat = request.POST.get('latitude', None)
        lng = request.POST.get('longitude', None)
        posts = request.POST.get('posts', None)
        radius = request.POST.get('radius', None)

        #TODO: Criar um novo projeto para cada busca
        self.clear_tables()

        try:
            insta = InstaSearch()
            insta.search(code, lat, lng, int(posts), radius)
        except Exception as e:
            print("Error in Instagram Search !!")
            print(e)

        print('-' * 30)

        try:
            flickr = FlickrSearch()
            flickr.search(lat, lng, int(posts), int(radius))
        except Exception as e:
            print("Error in Flickr Search !!")
            print(e)

        print('-' * 30)

        try:
            twitter = TwitterSearch()
            twitter.search(lat, lng, int(posts), int(radius))
        except Exception as e:
            print("Error in Twitter Search !!")
            print(e)

        print('-' * 30)

        try:
            fs = FoursquareSearch()
            fs.search(lat, lng, radius)
        except Exception as e:
            print("Error in Foursquare Search !!")
            print(e)

        return HttpResponseRedirect("/posts")

class GetUser(ListView):
    model = Post
    template_name = "List.html"

    def get_queryset(self):
        self.author = get_object_or_404(Person, login = self.args[0])
        return Post.objects.filter(author = self.author).order_by('-dateOfCreation')

class ShowPosts(ListView):
    model = Post
    template_name = "Posts.html"

    def get_queryset(self):
        return Post.objects.order_by('-dateOfCreation')

class ShowNetworks(ListView):
    model = Tag
    template_name = "Networks.html"

    def get_queryset(self):
        return Post.objects.all().values('network').annotate(total = Count('network')).order_by('-total')

class ShowPostsPerNetwork(ListView):
    model = Post
    template_name = "PostPerNetwork.html"

    def get_queryset(self):
        return Post.objects.filter(network = self.args[0]).order_by('-dateOfCreation')

class ShowUsers(ListView):
    model = Person
    template_name = "Users.html"

    def get_queryset(self):
        return Person.objects.annotate(num_posts = Count("post")).order_by('-num_posts')#[:3]

class ShowTags(ListView):
    model = Tag
    template_name = "Tags.html"

    def get_queryset(self):
        return Tag.objects.all().values('tag').annotate(total = Count('tag')).order_by('-total')

class ShowTagsPerUser(ListView):
    model = Tag
    template_name = "TagsPerUser.html"

    def get_queryset(self):
        self.author = get_object_or_404(Person, login = self.args[0])
        post = Post.objects.filter(author = self.author)
        return Tag.objects.all().filter(post = post).values('tag').annotate(total = Count('tag')).order_by('-total')
        
class ShowPostsPerTag(ListView):
    model = Post
    template_name = "PostPerTag.html"

    def get_queryset(self):
        tags = Tag.objects.all().filter(tag = self.args[0])
        return Post.objects.filter(tag = tags).order_by('-dateOfCreation')

class ShowConnectionsFromUser(ListView):
    model = Person
    template_name = "ConnectionsFromUser.html"

    def get_queryset(self):
        person = get_object_or_404(Person, login = self.args[0])
        return Connection.objects.filter(user = person)

class ShowPlaces(ListView):
    model = Place
    template_name = "Places.html"

    def get_queryset(self):
        return Place.objects.all().order_by('-checkins')

class ShowTips(ListView):
    model = Tip
    template_name = 'Tips.html'

    def get_queryset(self):
        place = get_object_or_404(Place, id = self.args[0])
        return Tip.objects.filter(place = place).order_by('-dateOfCreation')

class ShowGraph(ListView):
    model = Connection
    template_name = "Graph.html"

    def get_queryset(self):
        return Connection.objects.all()