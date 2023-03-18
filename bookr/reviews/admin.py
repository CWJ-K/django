from django.contrib import admin

from reviews.models import Publisher, Contributor, Book, BookContributor, Review


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('last_names', 'first_names')
    list_filter = ('last_names',)
    search_fields = ('last_names__startswith', 'first_names')


class BookAdmin(admin.ModelAdmin):
    model = Book
    date_hierarchy = 'publication_date'
    list_display = ('title', 'isbn13', 'get_publisher', 'publication_date')  # replace __str__
    list_filter = ('publisher', 'publication_date')
    search_fields = ('title', 'isbn__exact', 'publisher__name')

    def get_publisher(self, obj):
        return obj.publisher.name


class ReviewAdmin(admin.ModelAdmin):
    exclude = ('date_edited',)
    # fields = ('content', 'rating', 'creator', 'book')
    fieldsets = (
        (None, {'fields': ('creator', 'book')}),
        ('Review content', {'fields': ('content', 'rating')}),
    )


# Register your models here.
admin.site.register(Publisher)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Book, BookAdmin)  # reference the model use the new admin
admin.site.register(BookContributor)
admin.site.register(Review, ReviewAdmin)
