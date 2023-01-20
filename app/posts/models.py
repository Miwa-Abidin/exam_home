from django.db import models

from accounts.models import Profile


class AbstractPost(models.Model):
    text = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Tweet(AbstractPost):
    def __str__(self):
        return f'Tweet {self.id} by {self.profile.user.username}'

    def get_status_count(self):
        available_statuses = StatusType.objects.all()
        status_tweet = StatusTweet.objects.filter(tweet=self)
        result = {}
        for s_type in available_statuses:
            result[s_type.name] = 0
            for s_tweet in status_tweet:
                if s_tweet.type == s_type:
                    result[s_type.name] += 1
        return result


class Comment(AbstractPost):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment {self.id} by {self.profile.user.username} to {self.tweet.id}'


class StatusType(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class StatusTweet(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.SET_DEFAULT, default=1)
    type = models.ForeignKey(StatusType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['tweet', 'profile']

    def __str__(self):
        return f'{self.tweet.id} - {self.profile} - {self.type}'
