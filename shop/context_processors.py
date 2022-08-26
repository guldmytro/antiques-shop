from .forms import SearchForm


def search_form(request):
    if request.GET.get('query'):
        global_form = SearchForm(initial={'query': request.GET.get('query')})
    else:
        global_form = SearchForm()
    return {'search_form': global_form}