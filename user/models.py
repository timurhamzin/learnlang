from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from catalog.models import Language

class UserSettings(models.Model):
    default_translation_language = models.ForeignKey(
        Language, help_text='Enter your default translation target language.', on_delete=models.SET_NULL, null=True,
        )

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(f'{self.user} settings')

    def get_object(self):
        return UserSettings.objects.filter(user=self.request.user).first()

    # def get_absolute_url(self):
    #     return reverse('user:user_settings_update', args=[str(self.user.id)])
