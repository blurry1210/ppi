from django import forms
from main.models import Author,Category
from django.core.exceptions import ValidationError

class UpdateForm(forms.ModelForm):
    
    class Meta:
        model = Author
        fields = ("fullname", "bio", "profile_pic")



class UpdateProfileForm(forms.ModelForm):
    chosen_categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter(id__in=[7,8,9,10,11,12,13,14,15,16]),  # IDs of optional categories
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Author
        fields = ['fullname', 'bio', 'profile_pic', 'chosen_categories']

    def clean_chosen_categories(self):
        categories = self.cleaned_data.get('chosen_categories')
        if categories and categories.count() != 2:
            raise ValidationError("Please select exactly 2 categories.")
        return categories

    def save(self, commit=True):
        author = super().save(commit=False)
        if commit:
            author.save()
            self.instance.chosen_categories.set(self.cleaned_data['chosen_categories'])
            mandatory_categories = Category.objects.filter(id__in=[4,5,6])  # IDs of the mandatory categories
            self.instance.chosen_categories.add(*mandatory_categories)
        return author