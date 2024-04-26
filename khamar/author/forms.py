from django.contrib.auth.forms import UserCreationForm
from django import forms
from .constants import GENDER_TYPE
from django.contrib.auth.models import User
from .models import UserAccount,UserAddress


class UserRegistrationForm(UserCreationForm):
    gender=forms.ChoiceField(choices=GENDER_TYPE)
    street_address=forms.CharField(max_length=100)
    city=forms.CharField(max_length=100)
    country=forms.CharField(max_length=100)
    phone=forms.CharField(max_length=20)

    class Meta:
        model=User
        fields=['username','password1','password2','first_name','last_name',
                'email','gender','phone','city','country','street_address',]
        
    
    def save(self, commit=True):
        our_user=super().save(commit=False)    
        if commit==True:
            our_user.save()
            gender=self.cleaned_data.get('gender')
            country=self.cleaned_data.get('country')
          
            city = self.cleaned_data.get('city')
            street_address = self.cleaned_data.get('street_address')
            phone=self.cleaned_data.get('phone')
            UserAddress.objects.create(
                user = our_user,
                country = country,
                city = city,
                street_address = street_address,
                
            )
            UserAccount.objects.create(
                user = our_user,
                gender = gender,
                
                account_no = 100000+ our_user.id
            )
        return our_user
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                    
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                    ) 
                })    


class UserUpdateForm(forms.ModelForm):
    birth_date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender=forms.ChoiceField(choices=GENDER_TYPE)
    street_address=forms.CharField(max_length=100)
    city=forms.CharField(max_length=100)
    country=forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    

    class Meta:
        model=User
        fields=['first_name','last_name','email','password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                    
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                    ) 
                })
            if self.instance:
                try:
                    user_account = self.instance.account
                    user_address = self.instance.address
                except UserAccount.DoesNotExist:
                    user_account = None
                    user_address = None

                if user_account:
                    self.fields['gender'].initial = user_account.gender
                    self.fields['street_address'].initial = user_address.street_address
                    self.fields['city'].initial = user_address.city
                    self.fields['country'].initial = user_address.country
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account, created = UserAccount.objects.get_or_create(user=user) 
            user_address, created = UserAddress.objects.get_or_create(user=user) 
            user_account.gender = self.cleaned_data['gender']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()

            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.country = self.cleaned_data['country']
            user_address.save()
            password = self.cleaned_data.get('password')
            if password:
                user.set_password(password)
                user.save()

        return user

        
