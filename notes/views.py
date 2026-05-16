from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST
from django.db import transaction

from markdown import markdown

from .forms import NoteForm
from .models import Note, NoteVersion


@login_required
def dashboard(request):
    """
    User dashboard showing all personal notes.
    """
    notes = (
        Note.objects
        .filter(author=request.user)
        .only("id", "title", "updated_at", "is_public")
    )
    return render(request, "dashboard.html", {"notes": notes})


@login_required
@require_http_methods(["GET", "POST"])
def create_note(request):
    """
    Create a new note.
    """
    form = NoteForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        note = form.save(commit=False)
        note.author = request.user
        note.save()
        return redirect("dashboard")

    return render(request, "form.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def edit_note(request, pk):
    """
    Edit an existing note and store version history.
    """
    note = get_object_or_404(Note, pk=pk, author=request.user)

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)

        if form.is_valid():
            with transaction.atomic():
                # Save previous version before updating
                NoteVersion.objects.create(
                    note=note,
                    content=note.content,
                )

                form.save()

            return redirect("dashboard")
    else:
        form = NoteForm(instance=note)

    return render(request, "form.html", {"form": form, "note": note})


@login_required
@require_POST
def delete_note(request, pk):
    """
    Delete a note (POST only for safety).
    """
    note = get_object_or_404(Note, pk=pk, author=request.user)
    note.delete()
    return redirect("dashboard")


def view_shared_note(request, share_id):
    """
    Public view for shared notes.
    """
    note = get_object_or_404(
        Note,
        share_id=share_id,
        is_public=True,
    )

    html_content = markdown(
        note.content,
        extensions=["fenced_code", "tables"]
    )

    return render(
        request,
        "view.html",
        {
            "note": note,
            "content": html_content,
        },
    )


@login_required
def view_versions(request, pk):
    """
    View version history of a note.
    """
    note = get_object_or_404(Note, pk=pk, author=request.user)

    versions = (
        note.versions
        .only("id", "content", "created_at")
    )

    return render(
        request,
        "versions.html",
        {
            "note": note,
            "versions": versions,
        },
    )
