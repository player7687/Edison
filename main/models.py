from django.db import models
from django.contrib.auth.models import User
from urllib.request import urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from torch import le

class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    age = models.IntegerField()
    def __str__(self):
        return str(self.user)

class SongUploadList(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    duration = models.IntegerField(null = True)
    status = models.BooleanField(null = True)
    cover = models.ImageField(null = True, blank = True)
    acousticness = models.FloatField(null=True)
    danceability = models.FloatField(null=True)
    energy = models.FloatField(null=True)
    instrumentalness = models.FloatField(null=True)
    speechiness = models.FloatField(null=True)
    valence = models.FloatField(null=True)
    loudness = models.FloatField(null=True)
    tempo = models.FloatField(null=True)
    mode = models.IntegerField(null = True)
    song_uri = models.CharField(max_length=150, null = True)

    def __str__(self):
        return str(self.name)

    def get_image_from_url(self, url):
       img_tmp = NamedTemporaryFile()
       with urlopen(url) as uo:
           assert uo.status == 200
           img_tmp.write(uo.read())
           img_tmp.flush()
       img = File(img_tmp)
       self.cover.save(self.name + '-' + self.artist + '.png', img)

    def save(self, *args, **kwargs):
        super(SongUploadList, self).save(*args, **kwargs)
        return self

class GenreSongList(models.Model):
    song = models.ForeignKey(SongUploadList, on_delete=models.CASCADE)
    genre = models.CharField(max_length=100)
    probability = models.FloatField(null = True)

class UserUploadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(SongUploadList, on_delete=models.CASCADE)
    order = models.IntegerField()
    def __str__(self):
        return str(self.user) + ' (' + str(self.order) + ')'

class SpotifyToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=300)
    access_token = models.CharField(max_length=300)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)
    user_dis_name = models.CharField(max_length=150, null=True)
    user_email = models.CharField(max_length=150, null=True)