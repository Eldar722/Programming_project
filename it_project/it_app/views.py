from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Job, Guide
from django.contrib.auth import login, authenticate, logout
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm

def home_page(request):
    categories = Category.objects.all()
    jobs = Job.objects.all().order_by('-created_at')[:4]

    context = {
        'categories' : categories,
        'jobs' : jobs
    }
    return render(request, "./home.html", context)

def categories_page(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories
    }
    return render(request, "./categories.html", context)

def guides_page(request):
    guides = Guide.objects.all().order_by('-created_at')
    context = {
        'guides' : guides
    }
    return render(request, "./guides.html", context)

def jobs_page(request):
    jobs = Job.objects.all().order_by('-created_at')
    context = {
        'jobs' : jobs
    }
    return render(request, "./jobs.html", context)

def job_detail_page(request, pk):
    job = get_object_or_404(Job, pk=pk)
    context = {
        'job' : job
    }

    return render(request, "./job-detail.html", context)

def guide_detail_page(request, pk):
    guide = get_object_or_404(Guide, pk=pk)
    context = {
        'guide' : guide
    }

    return render(request, "./guide_detail.html", context)

def jobs_by_category_page(request, slug):
    category = get_object_or_404(Category, slug=slug)
    jobs = Job.objects.filter(category=category)
    context = {
        'category' : category,
        'jobs' : jobs
    }

    return render(request, "jobs-by-category.html", context)

def sign_up_page(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            custom_choice = form.cleaned_data.get('custom_choice')
            user.save()
            return redirect('login_page')
    else:
        form = NewUserForm()
    context ={
        'form' : form
    }
    return render(request, "./sign-up.html", context)

def login_page(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home_page')
    else:
        form = AuthenticationForm(request)

    context = {
        'form': form
    }
    return render(request, "login.html", context)

def logout_action(request):
    logout(request)
    return redirect('home_page')

@login_required
def leave_review(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.employer = request.user
            review.save()
            return redirect('home_page')
    else:
        form = MessageForm()
    return render(request, 'messages/leave_review.html', {'form': form})

@login_required
def user_reviews(request):
    reviews = Message.objects.filter(employee=request.user).order_by('-created_at')
    return render(request, 'messages/user_reviews.html', {'reviews': reviews})