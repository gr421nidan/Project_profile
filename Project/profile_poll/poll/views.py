from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.views import generic
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistrationForm
from .models import *
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from django.utils.timezone import now
from datetime import datetime


def index(request):
    return render(request, 'base.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            surname = form.cleaned_data['surname']
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = CustomUser.objects.create_user(username, email, password)
            user.first_name = name
            user.last_name = surname
            user.save()

            return redirect('base')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('base')


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registration/log_out.html'
    success_url = reverse_lazy('base')


class UserDelete(DeleteView):
    model = CustomUser
    success_url = reverse_lazy('base')
    context_object_name = 'application'


class UserUpdate(UpdateView):
    model = CustomUser
    fields = ('first_name', 'last_name', 'email', 'username', 'photo_profile')
    success_url = reverse_lazy('cabinet')


class CabinetView(generic.ListView):
    model = CustomUser
    template_name = 'cabinet.html'
    context_object_name = 'cabinet'

    def get_queryset(self):
        queryset = CustomUser.objects.filter(username=self.request.user.username)

        return queryset


class IndexView(ListView):
    model = Question
    template_name = 'polls/polls.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(end_date__gte=now())


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/polls_detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/result_polls.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if Vote.objects.filter(question_id=question_id, user_id=request.user.id).exists():
        messages.error(request, "Вы уже голосовали в этом опросе.")
        return HttpResponseRedirect(reverse('result', args=(question.id,)))
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/polls_detail.html', {
            'question': question,
            'error_message': 'Вы не сделали выбор'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        voter = Vote(user=request.user, question=question)
        voter.save()
        return HttpResponseRedirect(reverse('result', args=(question.id,)))
