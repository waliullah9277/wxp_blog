from django.shortcuts import render,redirect
from .forms import RegisterForm, ChangeUserForm, AuthorProfileForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate,login, update_session_auth_hash, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from posts.models import Post, Favorite
from .models import AuthorProfile
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

# create class based view all import files
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

# Create your views here.

#transactions send email start here
# def confirm_registration_email(conform_link, subject, template):
#     message = render_to_string(template, 
#         {"conform_link": conform_link}
#     )
#     to_email = conform_link.email
#     send_eamil = EmailMultiAlternatives(subject, ' ', to=[to_email])
#     send_eamil.attach_alternative(message, 'text/html')
#     send_eamil.send()

#transactions send email end here

def register(request):
    if request.user.is_authenticated:
        return redirect("profile")
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # register_form.save()

            username = register_form.cleaned_data.get("username")
            first_name = register_form.cleaned_data.get("first_name")
            last_name = register_form.cleaned_data.get("last_name")
            email = register_form.cleaned_data.get("email")
            password = register_form.cleaned_data.get("password")

            user = User.objects.create(username = username, first_name = first_name, last_name = last_name, email = email)

            user.set_password(password)
            user.is_active = False
            user.save()
            user = User.objects.get(username = username)
           
            token = default_token_generator.make_token(user)
            print('token ', token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print('uid ', uid)

            conform_link = f"https://wxp-blog.onrender.com//author/activate/{uid}/{token}"
            # messages.success(request, 'Account Created Successfully')

            mail_subject = "Account Verification Mail"
            message = render_to_string("author/confirm_register_email.html", {"conform_link": conform_link})
            # to_email = email
            send_message = EmailMultiAlternatives(mail_subject, "", to = [user.email])
            send_message.attach_alternative(message, 'text/html')
            send_message.send()
            
            messages.success(request, "Registration Complete. Please Check your email for conformation email")

            return redirect('user_login')
    else:
        register_form = RegisterForm()
    return render(request, 'author/register.html', {'form': register_form , 'type': 'Register'})


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk = uid)
    except(User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True 
        user.save()
        messages.success(request,'Successfully Activate your Account. Now you can login your account')
        return redirect("user_login")
    else:
        messages.error(request, "Something is wrong.")
        return redirect("register")

def user_login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_pass = form.cleaned_data['password']
            user = authenticate(username=user_name, password=user_pass)
            if user is not None:
                if user.is_active:
                    messages.success(request, 'Logged in Successfully')
                    login(request, user)
                    return redirect('profile')
        else:
            messages.warning(request, 'Login information is incorrect. Please provide valid information or create a new account.')
            return redirect('register')
    else:
        form = AuthenticationForm()
    return render(request, 'author/register.html', {'form': form, 'type': 'Login'})

# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data = request.POST)
#         if form.is_valid():
#             user_name = form.cleaned_data['username']
#             user_pass = form.cleaned_data['password']
#             user = authenticate(username = user_name, password = user_pass)
#             if user is not None:
#                 if user.is_active:
#                     messages.success(request, 'Logged in Successfully')
#                     login(request, user)
#                     return redirect('profile')
#         else:
#             messages.warning(request, 'Login information is Incorrect, please valid information or create a new account')
#             return redirect('register')
#     else:
#         form = AuthenticationForm()
#         return render(request, 'author/register.html', {'form' : form, 'type' : 'Login'})

# user login class based views 
class UserLoginView(LoginView):
    template_name = 'author/register.html'
    # success_url = reverse_lazy('profile')

    def get_success_url(self):
        return reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'Logged in successfully')
        return super().form_valid(form)
    
    
    def form_invalid(self, form):
        messages.warning(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
        # return reverse_lazy('register')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AuthenticationForm()
        context['type'] = 'Login'
        return context
    

@login_required
def profile(request):
    data = Post.objects.filter(author = request.user)
    # author = AuthorProfile.objects.get(user = request.user)
    return render(request, 'author/profile.html', {'data' : data})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = ChangeUserForm(request.POST, instance = request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Acoount Updated Successfully')
            return redirect('profile')
    else:
        profile_form = ChangeUserForm(instance= request.user)
    return render(request, 'author/update_profile.html', {'form': profile_form})

@login_required
def create_author_profile(request):
    if request.method == 'POST':
        form = AuthorProfileForm(request.POST, request.FILES,)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = AuthorProfileForm()

    return render(request, 'author/create_author_profile.html', {'form': form})

# @login_required
# def upload_profile(request):
#     if request.method == 'POST':
#         upload_profile_form = ProfileForm(request.POST)
#         print(upload_profile_form, "$$$")
#         if upload_profile_form.is_valid():
#             # upload_profile_form.instance.user = request.user
#             upload_profile_form.save()
#             messages.success(request, 'Successfully Uploaded profile Picture')
#             return redirect('profile')
#     else:
#         upload_profile_form = ProfileForm()
#         print(upload_profile_form, '@@@')
#     return render(request, 'author/upload_profile.html', {'form': upload_profile_form})


@login_required
def view_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('post')
    return render(request, 'author/favorite_list.html', {'favorites': favorites})

def pass_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data = request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Updated Successfully')
            update_session_auth_hash(request, form.user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'author/pass_change.html', {'form': form})

# def user_logout(request):
#     logout(request)
#     return redirect('user_login')

# class UserLogoutView(LogoutView):
#     next_page = reverse_lazy('login')

#     def dispatch(self, request, *args, **kwargs):
#         messages.success(self.request, 'Your Account has been Logged out Successfully !')
#         return super().dispatch(request, *args, **kwargs)

# class based views 
class UserLogoutView(LogoutView):
    def get_success_url(self):
        messages.success(self.request, 'Logged Out successfully')
        return reverse_lazy('user_login')


