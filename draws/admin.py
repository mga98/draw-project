from django.contrib import admin
from .models import Draw, DrawComment


@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'is_published')
    list_dispay_links = ('id', 'title')
    search_fields = ('title', 'id', 'description', 'slug', 'author__username')
    list_filter = ('author', 'is_published')
    list_per_page = 10
    list_editable = ('is_published',)
    ordering = ('-id', '-created_at')
    prepopulated_fields = {
        'slug': ('title',)
    }


@admin.register(DrawComment)
class DrawCommentAdmin(admin.ModelAdmin):
    list_display = ('draw', 'user', 'created_at')
    list_display_links = ('draw',)
