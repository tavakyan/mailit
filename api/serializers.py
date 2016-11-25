from rest_framework import serializers
from api.models import MailItem, LANGUAGE_CHOICES, STYLE_CHOICES


class MailItemSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    senderName = serializers.CharField(required=False, allow_blank=True, max_length=100)
    senderAddress = serializers.CharField(required=False, allow_blank=True, max_length=200)
    senderCity = serializers.CharField(required=False, allow_blank=True, max_length=50)
    senderState = serializers.CharField(required=False, allow_blank=True, max_length=20)
    senderZip = serializers.CharField(required=False, allow_blank=True, max_length=20)
    senderCountry = serializers.CharField(required=False, allow_blank=True, max_length=40)


    recipientName = serializers.CharField(required=False, allow_blank=True, max_length=100)
    recipientAddress = serializers.CharField(required=False, allow_blank=True, max_length=200)
    recipientCity = serializers.CharField(required=False, allow_blank=True, max_length=50)
    recipientState = serializers.CharField(required=False, allow_blank=True, max_length=20)
    recipientZip = serializers.CharField(required=False, allow_blank=True, max_length=20)
    recipientCountry = serializers.CharField(required=False, allow_blank=True, max_length=40)

    message = serializers.CharField(required=False, allow_blank=True, max_length=10000)
    status = serializers.CharField(required=False, allow_blank=True, max_length=100)

    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `MailItem` instance, given the validated data.
        """
        return MailItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `MailItem` instance, given the validated data.
        """
        instance.message = validated_data.get('message', instance.message)
        instance.save()
        return instance
