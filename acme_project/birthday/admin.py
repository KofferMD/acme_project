from django.contrib import admin

from birthday.models import Tag



class TagAdmin(admin.ModelAdmin):
    list_display = (
        'tag',
    )




admin.site.register(Tag, TagAdmin)
