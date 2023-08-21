from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.


class Faq(models.Model):

    question = RichTextField()
    answer = RichTextField()
    is_published = models.BooleanField(default=False)


    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
