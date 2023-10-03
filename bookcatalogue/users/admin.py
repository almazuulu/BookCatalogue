from django.contrib import admin
from .models import BookUser

@admin.register(BookUser)
class BookUserAdmin(admin.ModelAdmin):
    list_display = ['email']
