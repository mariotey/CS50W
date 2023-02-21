from django.shortcuts import render, redirect
from django import forms
from . import util
import markdown as md
from markupsafe import Markup
import random

class NewResultTitle(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Title', 'size': '177'}))

class NewResultText(forms.Form):
    textarea = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Description'}))

class NoEditTitle(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Title', 'size': '177', 'readonly':'readonly'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    return render(request, "encyclopedia/entry.html", {
        "entries": util.list_entries(),
        "entry_content": Markup(md.markdown(util.get_entry(name)))
    })

def get_result(request):
    query = request.POST["q"]

    list_entries = util.list_entries()

    if query.lower() in [x.lower() for x in list_entries]:
        return redirect(f"/wiki/{query}")
    else:
        new_listentries = [entry for entry in list_entries if query in entry]
        if new_listentries:
            return render(request, "encyclopedia/index.html", {
                "entries": new_listentries
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "Requested page is not found!"
            })
    
def new_result(request):
    new_title = NewResultTitle()
    new_text = NewResultText()

    return render(request, "encyclopedia/newpage.html", {
        "title": new_title,
        "textarea": new_text
    })

def save_result(request):
    query = request.POST["title"]
    list_entries = util.list_entries()
    
    if query.lower() in [x.lower() for x in list_entries]:    
         return render(request, "encyclopedia/error.html", {
                "message": "Requested page has already been created!"
            })
    else:
        with open(f"entries/{query}.md", "w") as f:
            f.write("#" + request.POST["title"])
            f.write("\n\n")
            f.write(request.POST["textarea"])

        return redirect(f"/wiki/{query}")
    
def save_edit(request):
    query = request.POST["title"]

    with open(f"entries/{query}.md", "w") as f:
        f.write(request.POST["textarea"])

    return redirect(f"/wiki/{query}")

def edit_result(request):
    last_url = request.META.get('HTTP_REFERER')
    url_exten = last_url.split("/wiki/", 1)[1]
    
    new_title = NoEditTitle({"title": url_exten.lower()})
    new_text = NewResultText({"textarea": md.markdown(util.get_entry(url_exten))})

    return render(request, "encyclopedia/editpage.html", {
        "title": new_title,
        "textarea": new_text
    })

def random_result(request):
    list_entries = util.list_entries()
    query = random.choice(list_entries)

    return redirect(f"/wiki/{query}")