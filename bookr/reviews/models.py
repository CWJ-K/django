from django.db import models
from django.contrib import auth

# Create your models here.

class Publisher(models.Model):
    """A company that publishes books."""

    name = models.CharField(max_length=50, help_text='The name of the Publisher.')
    website = models.URLField(help_text='The Publisher"s website')
    email = models.EmailField(help_text='The Publisher"s email address')

    def __str__(self):
        return self.name

class Book(models.Model):
    """A published book."""
    title = models.CharField(max_length=70, help_text="The title of the book.")
    publication_date = models.DateField(verbose_name="Date the book was published.")
    isbn = models.CharField(max_length=20, verbose_name="ISBN number of the book.")
    # CASCADE: if a publisher is deleted, all books referenced by the publisher are all deleted
    # Many (publisher) to One (book)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    # through: a intermediary table/bridge to connect two tables
    contributors = models.ManyToManyField('Contributor', through='BookContributor')

    def __str__(self):
        return title

class Contributor(models.Model):
    """A contributor to a book, e.g. author, editor, co-author"""
    first_names = models.CharField(max_length=50, help_text="The contributor's first name or names")
    last_names = models.CharField(max_length=50, help_text="The contributor's last name or names.")
    email = models.EmailField(help_text="The contact email for the contributor.")

    def __str__(self):
        return self.first_names

# if the intermediary is not built, Django will automatically build it
class BookContributor(models.Model):
    # define a set of choices
    class ContributionRole(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CO_AUTHOR = "CO_AUTHOR", "Co-Author"
        EDITOR = "EDITOR", "Editor"

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)

    # intermediary model, stores the extra information about the relationship b/w book and contributor
    role = models.CharField(
        verbose_name="The role this contributor had in the book.",
        choices=ContributionRole.choices,
        max_length=20
    )


class Review(models.Model):
    content = models.TextField(help_text='The Review text.')
    rating = models.IntegerField(help_text='The rating the reviewer has given.')
    date_created = models.DateTimeField(
        auto_now_add=True,
        help_text='The date and time the review was created.'
    )
    date_edited = models.DateTimeField(null=True, help_text='The date and time the review was last edited.')
    # User model from Django's built=in authentication module
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, help_text='The Book that this review is for.')

