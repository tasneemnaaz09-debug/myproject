from django.shortcuts import render, redirect
from .forms import ProfileForm
from .models import Job, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random


# ---------------- HOME ----------------
@login_required(login_url='/login/')
def home(request):
    companies = [
        {
            "name": "Google",
            "desc": "Google is a global technology leader focusing on search, artificial intelligence, cloud computing, and digital advertising."
        },
        {
            "name": "Microsoft",
            "desc": "Microsoft develops software, services, and cloud solutions like Windows, Azure, and Office."
        },
        {
            "name": "Amazon",
            "desc": "Amazon is a global e-commerce and cloud computing company."
        },
        {
            "name": "Infosys",
            "desc": "Infosys is an Indian IT services company offering consulting and technology solutions."
        },
        {
            "name": "TCS",
            "desc": "Tata Consultancy Services (TCS) provides consulting and business solutions globally."
        }
    ]

    return render(request, 'home.html', {'companies': companies})


# ---------------- CREATE JOB ----------------
@login_required(login_url='/login/')
def create_job(request):
    if request.method == 'POST':
        Job.objects.create(
            title=request.POST['title'],
            company=request.POST['company'],
            location=request.POST['location'],
            salary=request.POST['salary'],
            description=request.POST['description']
        )
        return redirect('/')

    return render(request, 'create.html')


# ---------------- LOGIN ----------------
def login_user(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['email'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('/')
    return render(request, 'login.html')


# ---------------- REGISTER ----------------
def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            return render(request, "register.html", {"error": "All fields required"})

        if User.objects.filter(username=email).exists():
            return render(request, "register.html", {"error": "User already exists"})

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        profile, created = Profile.objects.get_or_create(user=user)

        profile.mobile = request.POST.get("mobile")
        profile.dob = request.POST.get("dob")

        if request.FILES.get("photo"):
            profile.photo = request.FILES.get("photo")

        profile.save()

        return redirect("login")   # safer than "/login/"

    return render(request, "register.html")
# ---------------- PROFILE ----------------
@login_required(login_url='/login/')
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {
        'profile': profile,
        'form': form
    })


# ---------------- STATIC PAGES ----------------
def about(request):
    return render(request, 'about.html')

from django.shortcuts import render, redirect

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # store success in session
        request.session['success'] = "Message sent successfully!"
        return redirect('/contact/')

    success = request.session.pop('success', None)
    return render(request, "contact.html", {"success": success})


# ---------------- LOGOUT ----------------
def logout_user(request):
    logout(request)
    return redirect('/login/')


# ---------------- JOBS PAGE (FINAL ONE ONLY) ----------------
@login_required(login_url='/login/')
def jobs_page(request):

    companies = [
        {"name": "Google", "link": "https://careers.google.com"},
        {"name": "Microsoft", "link": "https://careers.microsoft.com"},
        {"name": "Amazon", "link": "https://amazon.jobs"},
        {"name": "Infosys", "link": "https://www.infosys.com/careers"},
        {"name": "TCS", "link": "https://www.tcs.com/careers"},
        {"name": "Wipro", "link": "https://careers.wipro.com"},
        {"name": "Accenture", "link": "https://www.accenture.com/careers"},
        {"name": "IBM", "link": "https://www.ibm.com/careers"},
        {"name": "Capgemini", "link": "https://www.capgemini.com/careers"},
        {"name": "Deloitte", "link": "https://www2.deloitte.com/global/en/careers.html"},
        {"name": "Flipkart", "link": "https://www.flipkartcareers.com"},
        {"name": "Zomato", "link": "https://www.zomato.com/careers"},
        {"name": "Swiggy", "link": "https://careers.swiggy.com"},
        {"name": "Reliance", "link": "https://careers.ril.com"},
        {"name": "L&T", "link": "https://careers.larsentoubro.com"}
    ]

    roles = [
        "Software Engineer", "Frontend Developer", "Backend Developer",
        "Full Stack Developer", "Data Analyst", "AI Engineer",
        "Cyber Security Analyst", "Mechanical Engineer", "Civil Engineer",
        "Electrical Engineer", "HR Executive", "Marketing Manager",
        "Sales Executive", "Business Analyst", "Accountant",
        "Customer Support Executive", "Operations Manager",
        "UI/UX Designer", "Product Manager", "Teacher",
        "Content Writer", "Graphic Designer", "Pharmacist",
        "Nurse", "Hotel Manager"
    ]

    locations = [
        "Bangalore", "Hyderabad", "Chennai", "Mumbai",
        "Delhi", "Pune", "Kolkata", "Remote"
    ]

    jobs = []
    seen = set()

    while len(jobs) < 150:
        company = random.choice(companies)
        role = random.choice(roles)
        location = random.choice(locations)

        title = f"{role} - {location}"
        key = (title, company["name"])

        if key not in seen:
            seen.add(key)
            jobs.append({
                "title": title,
                "company": company["name"],
                "location": location,
                "applyLink": company["link"]
            })

    # 🔍 SEARCH
    query = request.GET.get('search')
    if query:
        jobs = [
            job for job in jobs
            if query.lower() in job["title"].lower()
            or query.lower() in job["company"].lower()
            or query.lower() in job["location"].lower()
        ]

    return render(request, 'jobs.html', {'jobs': jobs})