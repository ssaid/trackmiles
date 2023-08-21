from django.contrib import admin

from .models import Faq

admin.site.register(Faq)

class FaqAdmin(admin.TabularInline):
    model = Faq
    fields = ["question", "created_at", "is_published"]
    ordering = ("-created_at",)


# admin.site.register(Faq, FaqAdmin)
