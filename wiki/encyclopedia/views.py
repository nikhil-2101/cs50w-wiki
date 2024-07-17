from random import choice
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django import forms
from markdown2 import Markdown

from. import util

def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {"entries": entries})

def wiki(request, entry):
    content = util.get_entry(entry)
    if content is None:
        raise Http404("Entry not found")
    return render(request, "encyclopedia/wiki.html", {"title": entry, "content": Markdown().convert(content)})

def search(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return render(request, "encyclopedia/search.html", {"found_entries": [], "query": query})

    entries = util.list_entries()
    found_entries = [entry for entry in entries if query.lower() in entry.lower()]

    if len(found_entries) == 1:
        return redirect("wiki", found_entries[0])

    return render(request, "encyclopedia/search.html", {"found_entries": found_entries, "query": query})

def random_entry(request):
    entries = util.list_entries()
    entry = choice(entries)
    return redirect("wiki", entry)

def entry_form(request, entry=None):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if not title or not content:
            messages.warning(request, "Both title and content are required.")
        else:
            if entry:
                util.save_entry(title, content)
                return redirect("wiki", entry=title)
            elif util.get_entry(title): 
                messages.warning(request, f'An entry with the title "{title}" already exists.')
                return redirect("edit_entry", entry=title)
            else:  
                content_with_title = f"# {title}\n\n{content}"
                util.save_entry(title, content_with_title)
                return redirect("wiki", entry=title)

    else: 
        if entry:
            content = util.get_entry(entry)
            if content is None:
                raise Http404("Entry not found")
            initial_data = {"title": entry, "content": content}
        else:
            initial_data = {}

        form = forms.Form()
        form.fields["title"] = forms.CharField(
            required=True,
            label="Title",
            widget=forms.TextInput(attrs={"placeholder": "Title", "class": "mb-4"}),
            initial=initial_data.get("title", "")
        )
        form.fields["content"] = forms.CharField(
            required=True,
            label="Content",
            widget=forms.Textarea(attrs={"placeholder": "Content (markdown)", "class": "form-control mb-4", "id": "new_content"}),
            initial=initial_data.get("content", "")
        )

    context = {"form": form}
    if entry:
        context["title"] = entry
    return render(request, "encyclopedia/entry_form.html", context)
