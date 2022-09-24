from distutils.archive_util import make_archive
from django.shortcuts import render, HttpResponseRedirect
from django import forms
import random

from . import util
from markdown2 import markdown

def index(request):
    entry = util.search(request.GET.get("q"))
    if entry:
        if type(entry) == list:
            return render(request, "encyclopedia/index.html", {
                "entries": entry,
                "title_h1": "Search Results"
            })
        else:
            return render(request, "encyclopedia/entry.html", {
                "entry": util.get_entry(entry),
                "title": entry
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "title_h1": "All Pages"
        })


def get_entry(request, entry):
    title_entry = entry
    try:
        entry = markdown(util.get_entry(entry))
    except:
        entry = None
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "title": title_entry,
    })

def random_entry(request):
    entries = util.list_entries()
    entry = entries[random.randint(0, len(entries) - 1)]
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown(util.get_entry(entry)),
        "title": entry
    })


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", required=True)
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'style':'height:400px; width:500px'}), required=True)

def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            if util.get_entry(form.cleaned_data["title"]):
                return render(request, "encyclopedia/new_entry.html", {
                    "form": form,
                    "error": "Entry already exists",
                    "title": "New Entry",
                    "title_h1": "New Entry"
                })
            title = form.cleaned_data["title"]
            content = "# " + form.cleaned_data["title"] + "\n\n" + form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(f"wiki/{title}")
        else:
            return render(request, "encyclopedia/new_entry.html", {
                "form": NewEntryForm(),
                "title": "New Entry",
                "title_h1": "New Entry"
            })
    
    return render(request, "encyclopedia/new_entry.html", {
        "form": NewEntryForm(),
        "title": "New Entry",
        "title_h1": "New Entry"
    })


# Write a function to edit an entry.

def edit_entry(request, entry):
    form = NewEntryForm()
    content = util.get_entry(entry)
    form.initial = {"title": entry, "content": content}
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = "# " + form.cleaned_data["title"] + "\n\n" + form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}")
    return render(request, "encyclopedia/edit_entry.html", {
        "form": form,
        "title": f"Edit {entry}",
        "title_h1": f"Edit {entry}"
    })
