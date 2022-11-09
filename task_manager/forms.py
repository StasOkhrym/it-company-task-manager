from django import forms


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by task name"}),
    )
    is_completed = forms.BooleanField(
        required=False
    )


class WorkerSearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Find worker"}),
    )