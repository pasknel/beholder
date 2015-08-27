"""beholder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from core.views import Index, Finder, Auth, GetUser, ShowUsers, ShowPosts, ShowTags, ShowPostsPerTag, \
    ShowConnectionsFromUser, ShowGraph, ShowNetworks, ShowPostsPerNetwork, ShowTagsPerUser, ShowPlaces, ShowTips

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^finder/', Finder.as_view()),
    url(r'^auth/', Auth.as_view()),
	url(r'^$', Index.as_view()),
    url(r'^users/(.+)/$', GetUser.as_view(), name='User_Detail'),
    url(r'^networks/$', ShowNetworks.as_view(), name='Networks'),
    url(r'^networks/(.+)/$', ShowPostsPerNetwork.as_view(), name='Networks_Detail'),
    url(r'^users/$', ShowUsers.as_view(), name="All_Users"),
    url(r'^posts/$', ShowPosts.as_view(), name="All_Posts"),
    url(r'^tags/$', ShowTags.as_view(), name="All_Tags"),
    url(r'^tags/from/(.+)/$', ShowTagsPerUser.as_view(), name='Tags_Per_User_Detail'),
    url(r'^tags/(.+)/$', ShowPostsPerTag.as_view(), name='Posts_Per_Tag_Detail'),
    url(r'^places/$', ShowPlaces.as_view(), name='All_Places'),
    url(r'^places/(.+)/$', ShowTips.as_view(), name='Tips_Per_Place'),
    url(r'^connections/from/(.+)/$', ShowConnectionsFromUser.as_view(), name='Connections_From_User'),
    url(r'^graph/$', ShowGraph.as_view(), name='Global_Graph'),
]
