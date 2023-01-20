from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Tweet, Comment, StatusTweet, StatusType


class StatusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusType
        fields = '__all__'



class TweetSerializer(serializers.ModelSerializer):
    statuses = serializers.ReadOnlyField(source='get_status_count')

    class Meta:
        model = Tweet
        fields = '__all__'
        read_only_fields = ['profile']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['profile', 'tweet']


class StatusTweetSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(write_only=True)

    class Meta:
        model = StatusTweet
        fields = "__all__"
        read_only_fields = ['profile', 'tweet', 'type']

    def create(self, validated_data):
        status_type = get_object_or_404(StatusType, slug=validated_data['slug'])
        validated_data.pop('slug')
        validated_data['type'] = status_type
        try:
            instance = super().create(validated_data)
        except IntegrityError:
            status_tweet = StatusTweet.objects.filter(**validated_data).first()
            if status_tweet:
                status_tweet.delete()
                raise serializers.ValidationError('У данного поста есть статус, текущий статус удален!')
            else:
                status_type = validated_data.pop('type')
                status_tweet = StatusTweet.objects.get(**validated_data)
                status_tweet.type = status_type
                status_tweet.save()
                instance = status_tweet
        return instance
