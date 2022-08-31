from .forms import SearchForm
from .models import Contact


def search_form(request):
    if request.GET.get('query'):
        global_form = SearchForm(initial={'query': request.GET.get('query')})
    else:
        global_form = SearchForm()
    return {'search_form': global_form}


def contacts(request):
    contact = Contact.objects.first()
    if contact:
        return {
            'phone': contact.phone,
            'email': contact.email,
            'telegram': contact.telegram,
        }
