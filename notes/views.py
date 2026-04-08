from django.shortcuts import render, get_object_or_404, redirect
from .models import Note, NoteVersion
from .forms import NoteForm
from django.contrib.auth.decorators import login_required
from markdown import markdown

@login_required
def dashboard(request):
    notes = Note.objects.filter(author=request.user)
    return render(request, 'dashboard.html', {'notes': notes})


@login_required
def create_note(request):
    form = NoteForm(request.POST or None)
    if form.is_valid():
        note = form.save(commit=False)
        note.author = request.user
        note.save()
        return redirect('dashboard')
    return render(request, 'form.html', {'form': form})


@login_required
def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk, author=request.user)

    # Save version before editing
    NoteVersion.objects.create(note=note, content=note.content)

    form = NoteForm(request.POST or None, instance=note)
    if form.is_valid():
        form.save()
        return redirect('dashboard')

    return render(request, 'form.html', {'form': form})


@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk, author=request.user)
    note.delete()
    return redirect('dashboard')


def view_shared_note(request, share_id):
    note = get_object_or_404(Note, share_id=share_id, is_public=True)
    html_content = markdown(note.content)
    return render(request, 'view.html', {'note': note, 'content': html_content})


@login_required
def view_versions(request, pk):
    note = get_object_or_404(Note, pk=pk, author=request.user)
    versions = note.versions.all()
    return render(request, 'versions.html', {'versions': versions})