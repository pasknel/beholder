from django.contrib import admin
from core.models import Post, Person

# Register your models here.

class PostAdmin(admin.ModelAdmin):

    fields = ["author", "dateOfCreation", "photo", "text", "latitude", "longitude"]

class PersonAdmin(admin.ModelAdmin):

    fields = ["login", "name"]

admin.site.register(Post, PostAdmin)
admin.site.register(Person, PersonAdmin)