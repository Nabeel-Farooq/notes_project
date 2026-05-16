from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    """
    Form for creating and updating notes.
    """

    class Meta:
        model = Note

        fields = (
            "title",
            "content",
            "is_public",
        )

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter note title",
                    "maxlength": 150,
                }
            ),

            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your note here...",
                    "rows": 6,
                }
            ),

            "is_public": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

        labels = {
            "title": "Title",
            "content": "Content",
            "is_public": "Make Public",
        }

        help_texts = {
            "is_public": "Allow other users to view this note.",
        }

    def clean_title(self):
        """
        Validate and clean title field.
        """

        title = self.cleaned_data["title"].strip()

        if len(title) < 3:
            raise forms.ValidationError(
                "Title must be at least 3 characters long."
            )

        return title

    def clean_content(self):
        """
        Validate and clean content field.
        """

        content = self.cleaned_data["content"].strip()

        if len(content) < 10:
            raise forms.ValidationError(
                "Content must be at least 10 characters long."
            )

        return content
