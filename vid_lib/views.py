from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from . import models, forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import urllib, requests

YOUTUBE_API_KEY = 'AIzaSyAgIOeV6Z6nhglm4HNFYP_3dWMHnGhD2As'

def home(request):
    recent_vid = models.video.objects.order_by('-id')[:3]
    return render(request, 'vid_lib/home.html',{'recent_vid':recent_vid})


class signup_view(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username,password=password)
        login(self.request, user)
        return redirect('home')


class group_crt(LoginRequiredMixin, generic.CreateView):
    model = models.group
    login_url = '/login/'
    template_name = 'vid_lib/group_form_crt_updt.html'
    fields = ['title']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class group_dtl(LoginRequiredMixin, generic.DetailView):
    model = models.group
    login_url = '/login/'

    def get_object(self):
        group = super().get_object()
        if not group.user == self.request.user:
            raise Http404
        return group

class group_updt(LoginRequiredMixin, generic.UpdateView):
    model = models.group
    fields = ['title']
    login_url = '/login/'
    template_name = 'vid_lib/group_form_crt_updt.html'

    def get_object(self):
        group = super().get_object()
        if not group.user == self.request.user:
            raise Http404
        return group

class group_dlt(LoginRequiredMixin, generic.DeleteView):
    model = models.group
    login_url = '/login/'
    template_name = 'vid_lib/confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        group = super().get_object()
        if not group.user == self.request.user:
            raise Http404
        return group

@login_required(login_url='/login/')
def add_video(request, pk):
    form = forms.video_form()
    search_form = forms.search_form()
    group = get_object_or_404(models.group ,pk=pk, user=request.user)
    if request.method == 'POST':
        form = forms.video_form(request.POST)
        if form.is_valid():
            form.instance.group = group
            parsed_url = urllib.parse.urlparse(request.POST['url'])
            u_tube_id = urllib.parse.parse_qs(parsed_url.query).get('v')
            form.instance.u_tube_id = u_tube_id[0]
            responce = requests.get(f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={ u_tube_id[0] }&key={YOUTUBE_API_KEY}')
            json = responce.json()
            form.instance.title = json['items'][0]['snippet']['title']
            form.save()
            return redirect('grp_dtl', pk=pk)

    return render(request, 'vid_lib/add_vid.html', {'form':form, 'search_form':search_form})


def video_search(request):
    search_form = forms.search_form(request.GET)
    if search_form.is_valid():
        search = request.GET['search_term']
        responce = requests.get(f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q={search}&key={ YOUTUBE_API_KEY }')
        json = responce.json()
        return JsonResponse(json)
    return JsonResponse({'rsp_data':'not working'})


class video_dlt(LoginRequiredMixin, generic.DeleteView):
    model = models.video
    login_url = '/login/'
    template_name = 'vid_lib/confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        video = super().get_object()
        if not video.group.user == self.request.user:
            raise Http404
        return video

@login_required(login_url='/login/')
def dashboard(request):
    groups = models.group.objects.filter(user=request.user)
    return render(request, 'vid_lib/dashboard.html', {'groups':groups})
