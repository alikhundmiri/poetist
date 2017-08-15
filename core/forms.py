from django import forms
from .models import all_authors, all_poems, all_riddles, all_stories, taggers
from pagedown.widgets import PagedownWidget

class PoemForm(forms.ModelForm):
    poem = forms.CharField(widget = PagedownWidget(show_preview=False))
    tags = forms.ModelMultipleChoiceField(required=False, queryset = taggers.objects.all(), widget=forms.CheckboxSelectMultiple())
    # poet = forms.ModelChoiceField(required=False, queryset = all_authors.objects.all(), widget=forms.RadioSelect())
    class Meta:
        model = all_poems
        fields = [
            "title",
            "poem",
            "show_poem",
            "tags",
            # "poet",
        ]

class StoryForm(forms.ModelForm):
    story = forms.CharField(widget = PagedownWidget(show_preview=False))
    tags = forms.ModelMultipleChoiceField(required=False, queryset = taggers.objects.all(), widget=forms.CheckboxSelectMultiple())
    related_story = forms.ModelMultipleChoiceField(required=False, queryset = all_stories.objects.all(), widget=forms.CheckboxSelectMultiple())
    # author = forms.ModelMultipleChoiceField(required=False, queryset = all_authors.objects.all(), widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = all_stories
        fields = [
            "title",
            "story",
            "show_story",
            "tags",
            "related_story",
            # "author",
        ]

class RiddleForm(forms.ModelForm):
    riddle = forms.CharField(widget = PagedownWidget(show_preview=False))
    explanation = forms.CharField(widget = PagedownWidget(show_preview=False))
    # riddler = forms.ModelMultipleChoiceField(required=False, queryset = all_authors.objects.all(), widget=forms.CheckboxSelectMultiple())
    tags = forms.ModelMultipleChoiceField(required=False, queryset = taggers.objects.all(), widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = all_riddles
        fields = [
            "title",
            "riddle",
            "answer",
            "explanation",
            "show_riddle",
            "tags",
            # "riddler",

        ]