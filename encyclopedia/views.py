from django.shortcuts import render
from random import randint
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_entry(request, title):
    data = util.get_entry(title)
    if not data:
        return render(request, "encyclopedia/404.html", {
            "title": title
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": data
    })
    
def search_entries(request):
    query = request.GET.get('q', '')
    entry = util.get_entry(query)
    
    if not entry:
        return render(request, "encyclopedia/search.html", {
            "title": "Search Results",
            "entries": util.search_entries(query)
        })
    else:
        return get_entry(request, query)

def add_new(request, action):
    method = request.method
    if  method == 'GET' and action == 'new':
        return render(request, "encyclopedia/add_new.html", {
            "title": "Create New Page",
            "action": action,
            "content": ''
        })
    elif method == 'GET' and action == 'edit':
        title = request.GET.get('title')
        content = util.get_entry(title, False)

        if not content:
            return render(request, "encyclopedia/404.html", {
                "title": title,
                
            })
        return render(request, "encyclopedia/add_new.html", {
            "content": content,
            "title": title,
            "action": action
        })
    else:
        title = request.POST.get("title") or request.GET.get("title")
        content = request.POST.get("content", "")
        entry = util.get_entry(title)

        if method == 'POST' and action == 'new':
            if entry:
                return render(request, "encyclopedia/add_new.html", {
                    "error": f"Page with title {title.title()} already exits."
                })
        else:
            if not entry:
                return render(request, "encyclopedia/404.html", {
                    "title": title
                })

        util.save_entry(title, content)
        return get_entry(request, title)

def get_random_page(request):
    entries = util.list_entries()
    title = entries[randint(0, len(entries))]
    return HttpResponseRedirect(reverse('wiki:entry', args=[title]))
    

