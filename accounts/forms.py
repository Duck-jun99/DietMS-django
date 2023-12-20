from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import User

class CustomUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = '__all__'
        
class CustomUserChangeForm(UserChangeForm):
    
    class Meta(UserChangeForm.Meta):
        #model = get_user_model()
        model = User
        #fields = '__all__'
        fields = ('useremail','weight','diabetes','blood_pressure')