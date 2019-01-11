from rest_framework import serializers
from shows.models import Show


class ShowSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)

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