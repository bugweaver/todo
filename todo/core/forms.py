from django import forms
from .models import List, Task


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'style': 'width: 300px;'})
        }

    def __init__(self, *args, **kwargs):
        super(ListForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ''


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Task', 'style': 'width: 300px;'})
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = ''
        self.fields['text'].required = False