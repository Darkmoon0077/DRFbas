from django.contrib import admin
from .models import User, Post, Feedback, Profile


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Feedback)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'slug')
    list_display_links = ('user', 'slug')