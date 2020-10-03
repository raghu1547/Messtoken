from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.admin import User
from django.core.exceptions import ObjectDoesNotExist


class UserRegForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.RegexField(
        regex="^[1-9][0-9]{5}$", error_messages={'invalid': 'Enter Proper Username'})
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput(), validators=[
                                RegexValidator('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).{8,}$')], error_messages={'invalid': "Enter valid password"})
    password2 = forms.CharField(widget=forms.PasswordInput(),)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = None
        try:
            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist as e:
                pass
            except Exception as e:
                raise e
            if not user:
                pass
            else:
                # print("jris")
                raise forms.ValidationError("Username Already Exists")
        except Exception as e:
            raise e
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = None
        try:
            try:
                user = User.objects.get(email=email)
            except ObjectDoesNotExist as e:
                pass
            except Exception as e:
                raise e
            if not user:
                pass
            else:
                raise forms.ValidationError(
                    "User with the email ID Already Exists")
        except Exception as e:
            raise forms.ValidationError(
                "User with the email ID Already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Passwords doesn't Match")
        return password2
