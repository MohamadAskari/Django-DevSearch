from django.db import models
from users.models import Profile
import uuid

class Project(models.Model):
    author = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    image = models.ImageField(null=True, blank=True, default="default.jpg")
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return self.title

    @property    
    def getVoteCount(self):
        total_votes = self.review_set.all()
        up_votes = total_votes.filter(value='up')
        ratio = (up_votes.count() / total_votes.count()) * 100
        self.vote_total = total_votes.count()
        self.vote_ratio = ratio
        self.save()

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
            
        return url

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']


class Review(models.Model):
    VOTE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE)
    creation_date = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)

    class Meta:
        unique_together = [['owner', 'project']]
        
    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return self.name