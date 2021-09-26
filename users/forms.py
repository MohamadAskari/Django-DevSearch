from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Message, Profile, Skill

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name':'Full name',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class':'input'})
        self.fields['email'].widget.attrs.update({'class':'input'})
        self.fields['username'].widget.attrs.update({'class':'input'})
        self.fields['password1'].widget.attrs.update({'class':'input'})
        self.fields['password2'].widget.attrs.update({'class':'input'})

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'location', 'profile_picture', 'bio',
        'intro', 'github_link', 'twitter_link', 'linkedin_link', 'website_link']


    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class':'input'})
        self.fields['email'].widget.attrs.update({'class':'input'})
        self.fields['username'].widget.attrs.update({'class':'input'})
        self.fields['location'].widget.attrs.update({'class':'input'})
        self.fields['profile_picture'].widget.attrs.update({'class':'input'})
        self.fields['bio'].widget.attrs.update({'class':'input'})
        self.fields['intro'].widget.attrs.update({'class':'input'})
        self.fields['github_link'].widget.attrs.update({'class':'input'})
        self.fields['twitter_link'].widget.attrs.update({'class':'input'})
        self.fields['linkedin_link'].widget.attrs.update({'class':'input'})
        self.fields['website_link'].widget.attrs.update({'class':'input'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class':'input'})
        self.fields['description'].widget.attrs.update({'class':'input'})

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class':'input'})
        self.fields['email'].widget.attrs.update({'class':'input'})
        self.fields['subject'].widget.attrs.update({'class':'input'})
        self.fields['body'].widget.attrs.update({'class':'input'})