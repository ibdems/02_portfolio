from django import forms

from .models import Blog, Comment, Contact, Testimonial


class BlogForm(forms.ModelForm):
    new_tags = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "python, dev, portfolio, ..."}),
        label="Tags (Separer par des virgules)",
    )

    class Meta:
        models = Blog
        fields = ["title", "content", "image", "date_published", "new_tags"]


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widget = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Votre nom"}),
            "content": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Votre commentaire"}
            ),
        }


class TemoignageForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["content", "position", "company", "photo"]
