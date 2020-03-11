from rest_framework import serializers
from backend.models import *


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = 'name',


class PersonSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    client = ClientSerializer()

    class Meta:
        model = Person
        fields = '__all__'


class CoupleSerializer(serializers.ModelSerializer):
    person_1 = PersonSerializer()
    person_2 = PersonSerializer()

    class Meta:
        model = Couple
        fields = 'person_1', 'person_2'


class SessionSerializer(serializers.ModelSerializer):
    couples = CoupleSerializer(many=True)

    class Meta:
        model = Session
        fields = 'id', 'creation_date', 'valid', 'couples'
