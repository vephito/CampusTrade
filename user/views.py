from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
# Create your views here.


class CustomloginView(LoginView):
    template_name = 'user/login.html'
    fields = '__all__'
    # redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('listing')

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))


class RegisterPage(FormView):
    template_name = 'user/register.html'
    form_class = RegistrationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)


class CustomLogoutView(LogoutView):
    pass

    # def register(request):
    #     if request.method == "POST":
    #         username = request.POST["username"]
    #         email = request.POST["email"]
    #         password = request.POST["password"]
    #         confirmation = request.POST["confirmation"]
    #         # Check Password
    #         if password != confirmation and password == "":
    #             return render(request, "user/register.html", {
    #                 "message": "Password Do Not Match."
    #             })
    #         # create a new user
    #         try:
    #             user = User.objects.create_user(username, email, password)
    #             user.save()
    #         except IntegrityError:
    #             return render(request, "user/register.html", {
    #                 "message": "Username already taken."
    #             })
    #         except ValueError:
    #             return render(request, "user/register.html", {
    #                 "message": "Enter a Valid input."
    #             })
    #         login(request, user)
    #         return HttpResponseRedirect(reverse("index"))
    #     else:
    #         return render(request, "user/register.html")
