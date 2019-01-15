from rest_framework import serializers
from shows.models import Show, Episode

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('id', 'show', 'title', 'description', 'cover')

    def create(self, validated_data):
        """
        Create and return a new `Episode` instance, given the validated data.
        """
        return Episode.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Show` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
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
        return Show.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Show` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance
