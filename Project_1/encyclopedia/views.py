from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import util

# class NewTaskForm(forms.Form):
#     task = forms.CharField(label="New Task")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    return render(request, "encyclopedia/entry.html", {
        "entries": util.list_entries(),
        "entry_content": util.get_entry(name)
    })

def get_result(request):
    return entry(request, "css")

# def add(request):
#     if request.method == "POST":
#         form = NewTaskForm(request.POST)
#         if form.is_valid():
#             task = form.cleaned_data["task"]

#     return render(request, "tasks/add.html", {
#         "form": NewTaskForm()
#     })