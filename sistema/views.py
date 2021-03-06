from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from sistema.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views import View
from .filters import NegocioFilter, UsuarioFilter
import time
from django.contrib import messages
from django.db.models import Count, Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import (
    Usuario,
    Negocio,
    Photo,
    Comentario
)

from .forms import (
    UsuarioForm,
    NegocioForm,
    PhotoForm,
    ComentarioForm
)


class BasicUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'photos/basic_upload/index.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name,
                    'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class ProgressBarUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.filter(user=request.user.pk)
        return render(self.request, 'photos/progress_bar_upload/index.html', {'photos': photos_list})

    def post(self, request):
        # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        time.sleep(2)
        form = PhotoForm(self.request.POST, self.request.FILES)
        form.instance.user = request.user
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name,
                    'url': photo.file.url}

        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def search(request):
    negocio_list = Negocio.objects.all()
    negocio_filter = NegocioFilter(request.GET, queryset=negocio_list)
    return render(request, 'search/negocio_list.html', {'filter': negocio_filter})


def search_usuario(request):
    usuario_list = Usuario.objects.all()
    usuario_filter = UsuarioFilter(request.GET, queryset=usuario_list)
    return render(request, 'search/usuario_list.html', {'filter': usuario_filter})


def profile_detail(request, username):
    if User.objects.get(username__iexact=username):
        user_details = User.objects.get(username__iexact=username)
        photos_list = Photo.objects.filter(user=user_details)
        page = request.GET.get('page', 1)
        paginator = Paginator(photos_list, 12)
        try:
            photos = paginator.page(page)
        except PageNotAnInteger:
            photos = paginator.page(1)
        except EmptyPage:
            photos = paginator.page(paginator.num_pages)

        comentarios_list = Comentario.objects.filter(empresa=user_details)
        page = request.GET.get('page', 1)
        paginator = Paginator(comentarios_list, 10)
        try:
            comentarios = paginator.page(page)
        except PageNotAnInteger:
            comentarios = paginator.page(1)
        except EmptyPage:
            comentarios = paginator.page(paginator.num_pages)
        media = Comentario.objects.filter(empresa=user_details).annotate(Count('comentario')).aggregate(Avg=Avg('nota'))['Avg']
       
        

        return render(request, "profile.html", {
            "user_details": user_details, 'photos': photos_list, 'comentarios': comentarios_list, 'media': media, 'photos': photos, 'comentarios':comentarios
        })
    else:
        return render("User not found")


def delete(request, id):
    photos = Photo.objects.get(pk=id)
    photos.delete()
    return redirect('sistema_perfil')


def delete_comentario(request,  id):

    comentario_delete = Comentario.objects.get(pk=id)
    comentario_delete.delete()
    return redirect('sistema_perfil')


def index(request):
    negocio_list = Negocio.objects.all()
    negocio_filter = NegocioFilter(request.GET, queryset=negocio_list)
    return render(request, 'search/negocio_list.html', {'filter': negocio_filter})


def perfil(request):
    photos_list = Photo.objects.filter(user=request.user.pk)
    page = request.GET.get('page', 1)
    paginator = Paginator(photos_list, 12)
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)
    comentarios_list = Comentario.objects.filter(empresa=request.user.username)
    page = request.GET.get('page', 1)
    paginator = Paginator(comentarios_list, 10)
    try:
        comentarios = paginator.page(page)
    except PageNotAnInteger:
        comentarios = paginator.page(1)
    except EmptyPage:
        comentarios = paginator.page(paginator.num_pages)
    usuario = Usuario.objects.all()
    form = UsuarioForm()
    media = Comentario.objects.filter(empresa=request.user).annotate(Count('comentario')).aggregate(Avg=Avg('nota'))['Avg']
    data = {'usuario': usuario, 'form': form,
            'photos': photos_list, 'comentarios': comentarios_list, 'media': media,  'photos': photos, 'comentarios':comentarios}
    return render(request, 'perfil.html', data)


# Cadastros de usúarios


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def cadastro(request):
    usuario = Usuario.objects.all()
    form = UsuarioForm()
    data = {'usuario': usuario, 'form': form}
    return render(request, 'cadastro.html', data)


def comentario_form_empresa(request, username):
    User.objects.get(username__iexact=username)
    user_details = User.objects.get(username__iexact=username)
    comentario = Comentario.objects.all()
    form = ComentarioForm()
    data = {'comentario': comentario,
            'form': form, "user_details": user_details}
    return render(request, 'profile_negocio/comentario.html', data)


def cadastro_comentario_empresa(request, username):

    if request.method == 'POST':
        form = ComentarioForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.empresa = username
            form = form.save()
            return redirect('sistema_perfil')
    else:
        form = ComentarioForm()
    return render(request, 'profile_negocio/comentario.html', {'form': form})


def comentario_form(request, username):
    User.objects.get(username__iexact=username)
    user_details = User.objects.get(username__iexact=username)
    comentario = Comentario.objects.all()
    form = ComentarioForm()
    data = {'comentario': comentario,
            'form': form, "user_details": user_details}
    return render(request, 'profile/comentario.html', data)


def cadastro_comentario(request, username):

    if request.method == 'POST':
        form = ComentarioForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.empresa = username
            form = form.save()
            return redirect('http://127.0.0.1:8000/profile/' + username)
    else:
        form = ComentarioForm()
    return render(request, 'profile/comentario.html', {'form': form})


def cadastro_novo(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.is_staff = True
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.usuario.nome = form.cleaned_data.get('nome')
            user.usuario.sobrenome = form.cleaned_data.get('sobrenome')
            user.usuario.email = form.cleaned_data.get('email')
            user.usuario.telefone = form.cleaned_data.get('telefone')
            user.usuario.cidade = form.cleaned_data.get('cidade')
            user.usuario.endereco = form.cleaned_data.get('endereco')
            user.usuario.cpf = form.cleaned_data.get('cpf')
            user.usuario.numero = form.cleaned_data.get('numero')
            user.usuario.bairro = form.cleaned_data.get('bairro')
            user.usuario.cep = form.cleaned_data.get('cep')
            user.usuario.password1 = form.cleaned_data.get('password1')
            user.usuario.data_nascimento = form.cleaned_data.get(
                'data_nascimento')
            user.usuario.gallery_usuario = form.cleaned_data.get(
                'gallery_usuario')
            user.usuario.pet = form.cleaned_data.get('pet')
            user.usuario.foto = form.cleaned_data.get('foto')
            user.usuario.sexo = form.cleaned_data.get('sexo')
            user.usuario.estado = form.cleaned_data.get('estado')
            user.usuario.about = form.cleaned_data.get('about')
            username = form.cleaned_data.get('username')
            user.username = username.lower()
            user.save()
            current_site = get_current_site(request)
            subject = 'Ative seu registro no PetAqui'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = UsuarioForm()
    return render(request, 'cadastro.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


class PhotoUpdate(LoginRequiredMixin, UpdateView):
    model = Usuario
    fields = ['foto']
    template_name = 'profile/change-photo.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()   # This should help to get current user

        # Next, try looking up by primary key of Usario model.
        queryset = queryset.filter(pk=self.request.user.usuario.pk)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No user matching this query")
        return obj

    def get_success_url(self):
        return reverse('sistema_perfil')


class UserNameUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username']
    template_name = 'profile/change-username.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()   # This should help to get current user

        # Next, try looking up by primary key of Usario model.
        queryset = queryset.filter(pk=self.request.user.usuario.pk)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No user matching this query")
        return obj

    def get_success_url(self):
        return reverse('sistema_perfil')


class EmailUpdate(LoginRequiredMixin, UpdateView):
    model = Usuario
    fields = ['email']
    template_name = 'profile/change-email.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()   # This should help to get current user

        # Next, try looking up by primary key of Usario model.
        queryset = queryset.filter(pk=self.request.user.usuario.pk)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No user matching this query")
        return obj

    def get_success_url(self):
        return reverse('sistema_perfil')


class PetUpdate(LoginRequiredMixin, UpdateView):
    model = Usuario
    fields = ['pet']
    template_name = 'profile/change-pet.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()   # This should help to get current user

        # Next, try looking up by primary key of Usario model.
        queryset = queryset.filter(pk=self.request.user.usuario.pk)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No user matching this query")
        return obj

    def get_success_url(self):
        return reverse('sistema_perfil')


class DataUpdate(LoginRequiredMixin, UpdateView):
    model = Usuario
    fields = ['nome', 'sobrenome', 'cpf', 'telefone', 'data_nascimento', 'sexo',
              'endereco', 'numero', 'bairro', 'cidade', 'estado', 'cep', 'about']
    template_name = 'profile/change-data.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()   # This should help to get current user

        # Next, try looking up by primary key of Usario model.
        queryset = queryset.filter(pk=self.request.user.usuario.pk)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No user matching this query")
        return obj

    def get_success_url(self):
        return reverse('sistema_perfil')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.usuario.email_confirmed = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request, 'account_activation.html')
    else:
        return render(request, 'account_activation_invalid.html')

 # Altera senha tando de usuarios quanto de negocios, pois lida direto no user


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Sua senha foi alterada com sucesso!!!')
            return redirect('sistema_perfil')
        else:
            messages.error(request, 'Corriga os erros.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })

 # Cadastros de Negócios


def cadastro_negocio(request):
    negocio = Negocio.objects.all()
    form = NegocioForm()
    data = {'negocio': negocio, 'form': form}
    return render(request, 'cadastro_negocio.html', data)


def cadastro_negocio_novo(request):
    if request.method == 'POST':
        form = NegocioForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.negocio.empresa = form.cleaned_data.get('empresa')

            user.negocio.cnpj = form.cleaned_data.get('cnpj')
            user.negocio.telefone = form.cleaned_data.get('telefone')
            user.negocio.whatsapp = form.cleaned_data.get('whatsapp')
            user.negocio.email = form.cleaned_data.get('email')
            user.negocio.site = form.cleaned_data.get('site')
            user.negocio.foto = form.cleaned_data.get('foto')

            user.negocio.tipo = form.cleaned_data.get('tipo')
            user.negocio.pet_aceitos = form.cleaned_data.get('pet_aceitos')
            user.negocio.endereco = form.cleaned_data.get('endereco')
            user.negocio.numero = form.cleaned_data.get('numero')
            user.negocio.bairro = form.cleaned_data.get('bairro')
            user.negocio.cep = form.cleaned_data.get('cep')
            user.negocio.cidade = form.cleaned_data.get('cidade')
            user.negocio.estado = form.cleaned_data.get('estado')
            user.negocio.horario_segunda1 = form.cleaned_data.get(
                'horario_segunda1')
            user.negocio.horario_segunda2 = form.cleaned_data.get(
                'horario_segunda2')
            user.negocio.horario_segunda3 = form.cleaned_data.get(
                'horario_segunda3')
            user.negocio.horario_segunda4 = form.cleaned_data.get(
                'horario_segunda4')
            user.negocio.horario_terca1 = form.cleaned_data.get(
                'horario_terca1')
            user.negocio.horario_terca2 = form.cleaned_data.get(
                'horario_terca2')
            user.negocio.horario_terca3 = form.cleaned_data.get(
                'horario_terca3')
            user.negocio.horario_terca4 = form.cleaned_data.get(
                'horario_terca4')
            user.negocio.horario_quarta1 = form.cleaned_data.get(
                'horario_quarta1')
            user.negocio.horario_quarta2 = form.cleaned_data.get(
                'horario_quarta2')
            user.negocio.horario_quarta3 = form.cleaned_data.get(
                'horario_quarta3')
            user.negocio.horario_quarta4 = form.cleaned_data.get(
                'horario_quarta4')
            user.negocio.horario_quinta1 = form.cleaned_data.get(
                'horario_quinta1')
            user.negocio.horario_quinta2 = form.cleaned_data.get(
                'horario_quinta2')
            user.negocio.horario_quinta3 = form.cleaned_data.get(
                'horario_quinta3')
            user.negocio.horario_quinta4 = form.cleaned_data.get(
                'horario_quinta4')
            user.negocio.horario_sexta1 = form.cleaned_data.get(
                'horario_sexta1')
            user.negocio.horario_sexta2 = form.cleaned_data.get(
                'horario_sexta2')
            user.negocio.horario_sexta3 = form.cleaned_data.get(
                'horario_sexta3')
            user.negocio.horario_sexta4 = form.cleaned_data.get(
                'horario_sexta4')
            user.negocio.horario_sabado1 = form.cleaned_data.get(
                'horario_sabado1')
            user.negocio.horario_sabado2 = form.cleaned_data.get(
                'horario_sabado2')
            user.negocio.horario_sabado3 = form.cleaned_data.get(
                'horario_sabado3')
            user.negocio.horario_sabado4 = form.cleaned_data.get(
                'horario_sabado4')
            user.negocio.horario_domingo1 = form.cleaned_data.get(
                'horario_domingo1')
            user.negocio.horario_domingo2 = form.cleaned_data.get(
                'horario_domingo2')
            user.negocio.horario_domingo3 = form.cleaned_data.get(
                'horario_domingo3')
            user.negocio.horario_domingo4 = form.cleaned_data.get(
                'horario_domingo4')
            user.negocio.sobre = form.cleaned_data.get('sobre')
            user.negocio.password1 = form.cleaned_data.get('password1')
            username = form.cleaned_data.get('username')
            user.username = username.lower()
            user.save()
            current_site = get_current_site(request)
            subject = 'Ative seu registro no PetAqui'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = NegocioForm()
    return render(request, 'cadastro_negocio.html', {'form': form})

# alterar dados da empresa


class DataUpdateNegocio(LoginRequiredMixin, UpdateView):
    model = Negocio
    fields = ['empresa', 'cnpj', 'telefone', 'whatsapp', 'site', 'tipo', 'pet_aceitos',
              'endereco', 'numero', 'bairro', 'cep', 'cidade', 'estado', 'sobre']
    template_name = 'profile_negocio/change-data.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()   # This should help to get current user

        # Next, try looking up by primary key of Usario model.
        queryset = queryset.filter(pk=self.request.user.negocio.pk)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No user matching this query")
        return obj

    def get_success_url(self):
        return reverse('sistema_perfil')

# alterar dados de horario da empresa


class HoraUpdateNegocio(LoginRequiredMixin, UpdateView):
    model = Negocio
    
    fields = ['horario_segunda1', 'horario_segunda2', 'horario_segunda3', 'horario_segunda4',
              'horario_terca1', 'horario_terca2', 'horario_terca3', 'horario_terca4',
              'horario_quarta1', 'horario_quarta2', 'horario_quarta3', 'horario_quarta4',
              'horario_quinta1', 'horario_quinta2', 'horario_quinta3', 'horario_quinta4',
              'horario_sexta1', 'horario_sexta2', 'horario_sexta3', 'horario_sexta4',
              'horario_sabado1', 'horario_sabado2', 'horario_sabado3', 'horario_sabado4',
              'horario_domingo1', 'horario_domingo2', 'horario_domingo3', 'horario_domingo4',
              ]
    template_name = 'profile_negocio/change-hour.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()   # This should help to get current user

        # Next, try looking up by primary key of Usario model.
        queryset = queryset.filter(pk=self.request.user.negocio.pk)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No user matching this query")
        return obj

    def get_success_url(self):
        return reverse('sistema_perfil')

# alterando Pet da Empresa


class PetEmpresaUpdate(LoginRequiredMixin, UpdateView):
    model = Negocio
    fields = ['pet_aceitos']
    template_name = 'profile_negocio/change-pet-empresa.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()   # This should help to get current user

        # Next, try looking up by primary key of Usario model.
        queryset = queryset.filter(pk=self.request.user.negocio.pk)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No user matching this query")
        return obj

    def get_success_url(self):
        return reverse('sistema_perfil')

# alterando a foto de perfil da empresa


class PhotoEmpresaUpdate(LoginRequiredMixin, UpdateView):
    model = Negocio
    fields = ['foto']
    template_name = 'profile_negocio/change-foto-empresa.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()   # This should help to get current user

        # Next, try looking up by primary key of Usario model.
        queryset = queryset.filter(pk=self.request.user.negocio.pk)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No user matching this query")
        return obj

    def get_success_url(self):
        return reverse('sistema_perfil')


# alterando email da empresa


class EmailEmpresaUpdate(LoginRequiredMixin, UpdateView):
    model = Negocio
    fields = ['email']
    template_name = 'profile_negocio/change-email-empresa.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()   # This should help to get current user

        # Next, try looking up by primary key of Usario model.
        queryset = queryset.filter(pk=self.request.user.negocio.pk)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No user matching this query")
        return obj

    def get_success_url(self):
        return reverse('sistema_perfil')
