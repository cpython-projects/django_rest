from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Author


@receiver(post_save, sender=Author)
def author_post_save(sender, instance, created, **kwargs):
    author = instance
    if created:
        print(f'Author: {author} created')
    else:
        print(f'Author: {author} updated')