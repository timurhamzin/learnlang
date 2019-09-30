from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances
from datetime import date
from django.utils.safestring import mark_safe

# Create your models here.
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book',
                               null=True, blank=True)
    isbn = models.CharField('ISBN', max_length=13, help_text=
            '13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>',
                            null=True, blank=True)

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    source_language = models.ForeignKey('Language', on_delete=models.SET_NULL,
                                        related_name='source_language', blank=True, null=True)
    translation_language = models.ForeignKey('Language', on_delete=models.SET_NULL,
                                                related_name='translation_language', blank=True, null=True)

    text = models.TextField(help_text='Enter the original book text', null=True)
    text_with_translation = models.TextField(help_text='Source text with interjected translations.',
                                             blank=True, null=True)
    translation_problems = models.TextField(help_text='Problems encountered during translation (code, source, result).',
                                            blank=True, null=True)

    translate_on_update = models.BooleanField(help_text=mark_safe(
        'Update translation. ' +
        '<span class="text-danger">Any changes made to translation manually will be discarded</span>'),
        default=False)

    def book_path(instance, filename):
        import os
        _, file_extension = os.path.splitext(filename)
        return f'catalog/book/{instance.id}/joint/{instance.title}{file_extension}'

    sound = models.FileField(upload_to=book_path, blank=True)
    lrc_archive = models.FileField(upload_to=book_path, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200, blank=True)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.book.title}' # ' ({self.id})'


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'


class Language(models.Model):
    """Language in which a Book is written"""
    name = models.CharField(max_length=100, help_text="Enter language name (e.g. English, French, Japanese etc.)")
    language_code = models.CharField(max_length=20, help_text="Enter language code (e.g. en, fr, ru etc.")

    def __str__(self):
        """String for representing the Model object."""
        return self.name

