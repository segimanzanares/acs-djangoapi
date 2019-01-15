from rest_framework import serializers
from shows.models import Show, Episode
from django.utils import timezone
import os

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('id', 'show', 'title', 'description', 'cover')

    def create(self, validated_data):
        """
        Create and return a new `Episode` instance, given the validated data.
        """
        validated_data['created_at'] = timezone.now()
        validated_data['updated_at'] = timezone.now()
        instance = Episode.objects.create(**validated_data)
        # Save file into the model directory
        instance.cover.save(os.path.basename(instance.cover.name), instance.cover, save=True)
        return instance

    def update(self, instance, validated_data):
        """
        Update and return an existing `Show` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.updated_at = timezone.now()
        instance.save()
        return instance

class ShowSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = Show
        fields = ('id', 'title', 'episodes')

    def create(self, validated_data):
        """
        Create and return a new `Show` instance, given the validated data.
        """
        validated_data['created_at'] = timezone.now()
        validated_data['updated_at'] = timezone.now()
        return Show.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Show` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.updated_at = timezone.now()
        instance.save()
        return instance
