import os
from math import radians, sin, cos, sqrt, atan2
from django.db.models import Model, SET_NULL, CharField, FloatField, IntegerField, ForeignKey, TextField, BooleanField, \
    ImageField, DateField, CASCADE


class Location(Model):
    name = CharField(max_length=50)
    address = TextField()
    latitude = FloatField()
    longitude = FloatField()

    def get_distance_from(self, location: 'Location') -> float:
        # approximate radius of earth in m
        r = 6373000

        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(location.latitude)
        lon2 = radians(location.longitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return r * c

    def __str__(self):
        return self.name


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class Client(Model):
    name = CharField(max_length=50)

    def __str__(self):
        return self.name


class Person(Model):
    profile_picture = ImageField(upload_to=get_image_path, blank=True, null=True)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    location = ForeignKey(Location, on_delete=SET_NULL, null=True)
    mobility = IntegerField()
    client = ForeignKey(Client, on_delete=SET_NULL, null=True, blank=True)
    mission = CharField(max_length=50, null=True, blank=True)
    phone_number = CharField(max_length=15, null=True, blank=True)
    can_move = BooleanField(default=False)
    active = BooleanField(default=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def can_meet(self, person: 'Person') -> bool:
        location1 = self.location
        location2 = person.location
        distance = location1.get_distance_from(location2)
        return (self.mobility + person.mobility) >= distance

    @classmethod
    def test_persons_can_meet(cls, person1, person2):
        return person1.can_meet(person2)

    def get_meetable_persons(self, list_persons=None):
        if list_persons:
            pool = list_persons
        else:
            pool = self.objects.all()
        return [p for p in pool if p != self and self.can_meet(p)]


class Session(Model):
    creation_date = DateField(auto_now_add=True)
    valid = BooleanField(default=False)


class Couple(Model):
    person_1 = ForeignKey(Person, on_delete=CASCADE, related_name='+')
    person_2 = ForeignKey(Person, on_delete=CASCADE, related_name='+')
    session = ForeignKey(Session, on_delete=CASCADE, related_name='couples')


class PossibleSession(Model):
    @classmethod
    def get_random(cls) -> "PossibleSession":
        return cls.objects.order_by('?').first()


class PossibleCouple(Model):
    person_1 = ForeignKey(Person, on_delete=CASCADE, related_name='+')
    person_2 = ForeignKey(Person, on_delete=CASCADE, related_name='+')
    session = ForeignKey(PossibleSession, on_delete=CASCADE, related_name='couples')
