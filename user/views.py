from django.shortcuts import render
from user.models import UserSettings
from django.views import generic


class UserSettingsDetailView(generic.DetailView):
    model = UserSettings

    def get_context_data(self, **kwargs):
        us = UserSettings.objects.filter(user=self.request.user).first()
        obj = kwargs['object']
        context = super(UserSettingsDetailView, self).get_context_data(**kwargs)
        context.update({'user_settings': us})
        return context


from django.contrib.auth.decorators import login_required


@login_required
def user_settings(request):
    us = UserSettings.objects.filter(user=request.user).first()
    if us == None:
        us = UserSettings.objects.create(user=request.user)
        us.save()
    context = {
        'user_settings': us,
    }

    return render(request, 'user/user_settings.html', context)


from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse


class UserSettingsUpdate(LoginRequiredMixin, UpdateView):
    model = UserSettings
    fields = '__all__'

    def get_success_url(self):
        # No need for reverse_lazy here, because it's called inside the method
        return reverse('user:user_settings')