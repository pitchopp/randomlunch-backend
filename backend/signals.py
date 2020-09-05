from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from backend.models import Person, Location
from backend.scripts import generate_possible_sessions


@receiver(post_save, sender=Person)
def post_save_person(**kwargs):
    generate_possible_sessions.run()


@receiver(post_delete, sender=Person)
def post_delete_person(**kwargs):
    generate_possible_sessions.run()


@receiver(post_save, sender=Location)
def post_save_location(**kwargs):
    generate_possible_sessions.run()


@receiver(post_delete, sender=Location)
def post_delete_location(**kwargs):
    generate_possible_sessions.run()
