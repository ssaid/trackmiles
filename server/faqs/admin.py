from django.contrib import admin

from .models import Faq

# admin.site.register(Faq)

class FaqAdmin(admin.ModelAdmin):
    list_display = ["question", "sequence", "created_at", "is_published"]

admin.site.register(Faq, FaqAdmin)
