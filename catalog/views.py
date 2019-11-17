from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from catalog.forms import BookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Book, Author, BookInstance, Genre, Language
from catalog.init_db import make_lrc_files
import datetime
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookModelForm
import os
from django.conf import settings
from text_parse import deconjugate
from django.views import generic
from django.urls import resolve

    # @login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    num_authors_j = Author.objects.filter(first_name__contains='J').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 20
    # context_object_name = 'my_book_list'   # your own name for the list as a template variable
    # queryset = Book.objects.all()[:5] # Get 5 books containing the title war
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location


class BookDetailView(generic.DetailView):
    model = Book
    fields = ['title', 'author', 'isbn', 'source_language', 'translation_language',
              'genre', 'text']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lrc_archive = 'no subtitles'
        if self.object.lrc_archive:
            lrc_archive = os.path.basename(self.object.lrc_archive.path)
        context['lrc_archive'] = lrc_archive
        return context


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 1
    # context_object_name = 'my_book_list'   # your own name for the list as a template variable
    # queryset = Book.objects.all()[:5] # Get 5 books containing the title war
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location


class LanguageListView(generic.ListView):
    model = Language


class AuthorDetailView(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        obj = kwargs['object']
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context.update({'next': Author.objects.filter(id__gt=obj.id).order_by('id').first()})
        context.update({'previous': Author.objects.filter(id__lt=obj.id).order_by('id').last()})
        # context.update({'next': Author.get_next_by_id(obj)})
        return context


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    # context_object_name = 'my_book_list'   # your own name for the list as a template variable

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'
    # context_object_name = 'my_book_list'   # your own name for the list as a template variable

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            # book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        # form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


def app_name(request):
    return request.resolver_match._func_path.split('.')[0]


@permission_required('catalog.can_mark_returned')
def book_deconjugated(request, pk):
    book = get_object_or_404(Book, pk=pk)
    parse_js = f'<script src="{settings.STATIC_URL + app_name(request) + "/js/parse.js"}"></script>'
    context = {
        'book': book,
        'scripts': [settings.JQUERY_URL, settings.VUE_URL, parse_js],
    }
    print(book.text_deconjugated)
    return render(request, 'catalog/book_deconjugated.html', context=context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    success_url = reverse_lazy('authors')


from django.utils.safestring import mark_safe


def form_valid_bookupdate(self, form):
    self.object = Book(sound=self.get_form_kwargs().get('files').get('sound', None))
    self.object = form.save(commit=True)
    book = self.object
    book.text_deconjugated = deconjugate(book.text, book.source_language)
    if book.translate_on_update:
        from catalog.init_db import translate_book
        book.text_with_translation, translate, book.translation_problems, book.sound = \
            translate_book(book, self.request.user, True)
    lrc_archive = make_lrc_files(book)
    lrc_archive = lrc_archive.replace(os.path.join(settings.MEDIA_ROOT, ''), '')
    book.lrc_archive = lrc_archive
    book.save()
    return super(type(self), self).form_valid(form)


class BookCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    form_class = BookForm

    def form_valid(self, form):
        return form_valid_bookupdate(self, form)


class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    form_class = BookForm

    def form_valid(self, form):
        return form_valid_bookupdate(self, form)


class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

