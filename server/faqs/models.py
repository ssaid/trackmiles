from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.


class Faq(models.Model):

    question = RichTextField()
    answer = RichTextField()
    sequence = models.IntegerField(default=9999)
    is_published = models.BooleanField(default=False)


    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sequence', '-created_at']

    def __str__(self):
        return self.question
