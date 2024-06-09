from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import CoverLetter
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import json
from decouple import config
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
import PyPDF2

HUGGINGFACE_HUB_API_TOKEN = config("huggingface_api_key")


@login_required
def index(request):
    return render(request, "index.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            error_message = "Invalid Username or Password"
            return render(request, "login.html",
                          {"error_message": error_message})
    return render(request, "login.html")


def user_signup(request):
    error_message = None
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repeatpassword = request.POST["repeatpassword"]

        if password == repeatpassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect("/")
            except Exception as e:
                error_message = f"Error creating account: {str(e)}"
                return render(request, "signup.html",
                              {"error_message": error_message})
        else:
            error_message = "Password do not match"
    return render(request, "signup.html", {"error_message": error_message})


def user_logout(request):
    logout(request)
    return redirect("/")


def generate_cover_from_description(Description: str, UserProfil: str) -> str:
    llm = HuggingFaceHub(
        repo_id="mistralai/MixTraL-8x7B-Instruct-v0.1",
        model_kwargs={
            "temperature": 0.12,
            "max_length": 10000,
            "max_new_tokens": 5000,
        },
        huggingfacehub_api_token=HUGGINGFACE_HUB_API_TOKEN,
    )

    prompt_template = PromptTemplate(
        template="""Make me an cover letter like an professionelle of the
        field with only the follow job description
        @Description: {Description} and my profil
        @UserProfil: {UserProfil} @CoverLetter:""",
        input_variables=["Description", "UserProfil"],
    )

    model_input = {"Description": Description, "UserProfil": UserProfil}

    response = llm(prompt_template.format(**model_input)
                   ).split("@CoverLetter:")
    content = response[-1].strip()
    return content


def generate_title_from_description(Description: str) -> str:
    llm = HuggingFaceHub(
        repo_id="mistralai/MixTraL-8x7B-Instruct-v0.1",
        model_kwargs={
            "temperature": 0.12,
            "max_length": 5000,
            "max_new_tokens": 30,
        },
        huggingfacehub_api_token=HUGGINGFACE_HUB_API_TOKEN,
    )

    prompt_template = PromptTemplate(
        template="""
                Extract the job title from the following job offer description:

                {Description}

                Job Title:
                """,
        input_variables=["Description"],
    )

    model_input = {"Description": Description}

    response = llm(prompt_template.format(**model_input)).split("Job Title:")
    content = response[-1].strip()
    return content


@csrf_exempt
def generate_cover(request):
    if request.method == "POST":
        try:
            description_text = request.POST.get('Description')
            profil_file = request.FILES.get('profil_pdf')

            if not profil_file:
                return JsonResponse({'error': 'Profile PDF not provided'},
                                    status=400)

            jobdescription = description_text
            user_profil = extract_text_from_pdf(profil_file)

        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data sent'},
                                status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        title = generate_title_from_description(jobdescription)

        if not user_profil:
            # Check if the user has a previously saved user profile
            try:
                user_profil = CoverLetter.objects.filter(
                    user=request.user
                    ).latest('created_at').user_profil
            except CoverLetter.DoesNotExist:
                user_profil = f"I'm a specialist in the field of {title}"

        Cover_content = generate_cover_from_description(
                                    Description=jobdescription,
                                    UserProfil=user_profil)

        new_cover_letter = CoverLetter.objects.create(
            user=request.user,
            user_profil=user_profil,
            job_title=title,
            job_description=jobdescription,
            generated_content=Cover_content
        )
        new_cover_letter.save()
        return JsonResponse({"content": Cover_content})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(reader.pages)
    text = []
    for i in range(num_pages):
        text.append(reader.pages[i].extract_text())
    return ' '.join(text)


def cover_details(request, pk):
    cover_letter_detail = CoverLetter.objects.get(id=pk)
    if request.user == cover_letter_detail.user:
        if request.method == "POST" and "download_pdf" in request.POST:
            # Handle PDF download
            template = get_template("cover-detail.html")
            html = template.render({"cover_letter_detail":
                                    cover_letter_detail})
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = '''attachment;
                                              filename="cover_letter.pdf"'''
            pisa_status = pisa.CreatePDF(html, dest=response)
            if pisa_status.err:
                return HttpResponse("Error generating PDF: {}".format(
                    pisa_status.err
                    ))
            return response
        return render(
            request, "cover-detail.html",
            {"cover_letter_detail": cover_letter_detail}
        )
    else:
        return redirect("/")


def cover_list(request):
    cover_letters = CoverLetter.objects.filter(user=request.user)
    return render(request, "all-cover.html", {"cover_letters": cover_letters})
