from django.forms import ModelForm
from .models import Post
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ["types_post", "author", "category", "heading_post", "text_post"]




class BasicSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': ('First name')}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': ('Last name')}))

    GENDERS = (('man', ('Man')), ('woman', ('Woman')))
    gender = forms.ChoiceField(label=('Gender'), choices=GENDERS, widget=forms.Select())

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.gender = self.cleaned_data['gender']

        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user