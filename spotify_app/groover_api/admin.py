from django.contrib import admin
from .models import Artists, Album, New_Releases

# Register your models here.

admin.site.register(Artists)
admin.site.register(Album)
admin.site.register(New_Releases)
