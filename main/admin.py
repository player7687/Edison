from django.contrib import admin
from .models import SongUploadList, UserProfile, UserUploadHistory, GenreSongList, SpotifyToken

# Register your models here.

admin.site.register(SongUploadList)
admin.site.register(UserProfile)
admin.site.register(UserUploadHistory)
admin.site.register(GenreSongList)
admin.site.register(SpotifyToken)