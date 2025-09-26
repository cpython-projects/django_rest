from django.contrib import admin
from .models import Publisher, Author, Book, BookAuthor


class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('pk', "title", "publisher", "published_date", "is_bestseller")
    list_filter = ("is_bestseller", "publisher", 'is_banned')
    search_fields = ("title",)
    date_hierarchy = "published_date"
    inlines = [BookAuthorInline]  # ✅ вместо добавления authors в fieldsets


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "birth_date")
    search_fields = ("first_name", "last_name")


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name", "established_date")
    search_fields = ("name",)
