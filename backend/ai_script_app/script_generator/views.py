from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from pytube import YouTube
from .models import ScriptsList, CustomUser
from decouple import config
import assemblyai as aai
# import openai
from cohere import Client
import cohere
import json
import os

# Create your views here.

def index(request):
    return render(request, 'index.html')

def user_login(request):
    """
    Logs the user in.
    """
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user != None:
            try:
                login(request, user)
                return redirect('/')
            except:
                error_message = 'Error Server Down'
                return render(request, 'login.html', {'error_message': error_message})
            
        else:
            error_message = "Invalid Username or Password"
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')

def activate(request, uidb64, token):
    try:
        # Decode uidb64 to get user ID
        uid = force_str(urlsafe_base64_decode(uidb64))
        User = get_user_model()
        user = User.objects.get(pk=uid)

        # Check if the token is valid
        if user.personal_token == token:
            # Activate the user's account
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated successfully.')
            return redirect('/')  # Redirect to login page after activation
        else:
            messages.error(request, 'Invalid activation link. Please try again.')
            return redirect('/')  # Redirect to login page with error message
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Invalid activation link. User does not exist.')
        return redirect('/')  # Redirect to login page with error message

def send_verification_email(request, user):
    token_generator = default_token_generator
    uid = urlsafe_base64_encode(str(user.pk).encode())
    token = token_generator.make_token(user)
    # Save the generated token on the user profile.
    user.personal_token = token
    verification_link = reverse('verify_account', kwargs={'uidb64': uid, 'token': token})
    verification_url = request.build_absolute_uri(verification_link)
    
    subject = 'Verify Your Account on AI Scripts'
    message = f'Hi {user.username},\n\nPlease click on the following link to verify your account:\n{verification_url}'
    sender_email = settings.DEFAULT_FROM_EMAIL
    recipient_email = user.email
    
    send_mail(subject, message, sender_email, [recipient_email])

def user_signup(request):
    """
    Creates a new user
    """
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repPassword = request.POST['repeatPassword']

        if password == repPassword and CustomUser.objects.filter(username=username).exists() == False and CustomUser.objects.filter(email=email).exists() == False:
            try:
                # Validate the password using Django's built-in validators
                validate_password(password)
                
                user = CustomUser.objects.create_user(username, email, password)
                send_verification_email(request, user)
                user.is_active = False
                user.save()
                login(request, user)
                messages.success(request, "A verification mail has been sent to your Email (Check your spam inbox if you don't see it!), be sure to verify your mail to keep using our services!")
                return redirect('/')
            
            except ValidationError as e:
                # Password is invalid, handle the error
                error_message = e.messages[0]  # Get the first error message
                return render(request, 'signup.html', {'error_message': error_message})
                
        elif password != repPassword:
            error_message = "Passwords do not match"
            return render(request, 'signup.html', {'error_message': error_message})
        elif CustomUser.objects.filter(username=username).exists():
            error_message = "Username already in use"
            return render(request, 'signup.html', {'error_message': error_message})
        elif CustomUser.objects.filter(email=email).exists():
            error_message = "An account with that email is already in use"
            return render(request, 'signup.html', {'error_message': error_message})

    return render(request, 'signup.html')

@login_required
def all_scripts(request):
    scripts = ScriptsList.objects.filter(user=request.user)
    return render(request, 'all-scripts.html', {'scripts': scripts})

def script_details(request,pk):
    """
    Given an ID it sends the user to the details page.
    """
    script_details = ScriptsList.objects.get(id=pk)

    if request.user == script_details.user:
        return render(request, 'script-details.html', {'script_details': script_details})
    else:
        redirect('/')
        return JsonResponse({'error': 'Not allowed to see that'}, status=405)
    
def delete_script(request,pk):
    """
    Given an ID it deletes that item from the database.
    """
    if request.method == 'POST':
        script = ScriptsList.objects.get(id=pk)
        script.delete()
        return render(request, 'index.html')

    scripts = ScriptsList.objects.filter(user=request.user)

    return render(request, 'all-scripts.html', {'scripts': scripts})

def get_video_title(link):
    """
    Returns the title of the video if it has one.
    """
    yt = YouTube(link)
    title = yt.title
    return title

def get_audio(link):
    """
    Creates the needed audio file for its transcription.
    """
    # r"^\$*\w+\W" to put on the regex in pytube/cipher.py
    yt = YouTube(link)
    audioFile = yt.streams.filter(only_audio=True).first()
    outFile = audioFile.download(output_path=settings.MEDIA_ROOT)
    # Make the new audio file
    base, ext = os.path.splitext(outFile)
    newFile = base + '.mp3'
    os.rename(outFile, newFile)
    return newFile

# def generate_metrics(transcript):
#     """
#     This one uses open AI to transform the given transcript text into whatever we prompt it to do.
#     Still not sure what to use it for and it costs money for each use.
#     """
#     openai.api_key = config('OPENAI_API_KEY')

#     prompt = f"Based on the following script I need you to count each word and tell me the amount of the most used ones\n"

#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=prompt,
#         max_tokens=1000
#     )

#     generated_content = response.choices[0].text.strip()

#     return generated_content

def cohere_summary(transcript):
    """
    This one uses Cohere to transform the given transcript text into whatever we prompt it to do.
    It will return a summary for our transcription.
    """
    # Initialize the Cohere client with your API key.
    client = Client(api_key=config('COHERE_API_KEY'))

    # Define the task (prompt for text generation)
    prompt = "Please tell me what this text is about and make a summary of it.\n\n" + transcript

    # Make an API request to generate text based on the prompt
    response = client.generate(prompt=prompt)
    
    # Handle the response
    generated_content = response.generations[0].text

    return generated_content

def get_transcript(link):
    """
    Makes thre transcription from an audio file.
    """
    audio_file = get_audio(link)

    aai.settings.api_key = config('AAI_API_KEY')
    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(audio_file)

    # Deletes the audio file once the transcript has been done.
    os.remove(audio_file)

    if transcript:
        return transcript.text
    else:
        return ("Not recognizable voices")
    
@csrf_exempt
def generate_script(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            videoLink = data['link']
            
            # Check is the Link is already in the database for this user.
            if request.user.is_authenticated:
                if ScriptsList.objects.filter(videoLink=videoLink).exists():
                    return JsonResponse({'error': 'The script for this video is already saved on "Your Scripts"'}, status=500)

        except(KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data sent'}, status=400)
        
        # Gets the video title if it has one.
        title = get_video_title(videoLink)

        # Makes a transcription of the given video.
        transcription = get_transcript(videoLink)
        if not transcription:
            return JsonResponse({'error': 'Invalid video file'}, status=500)
        
        # Gives the transcription to openAI to make the metrics.
        # openai_content = generate_metrics(transcription)
        # if not openai_content:
        #     return JsonResponse({'error': 'Failed to get the metrics'}, status=500)
        
        # print(openai_content)

        # Gives the transcription to cohere.
        cohere_content = cohere_summary(transcription)
        if not cohere_content:
            return JsonResponse({'error': 'Failed to get the summary'}, status=500)
        
        # Save the content on the database if the user is authenticated.
        if request.user.is_authenticated:  
            newScriptsList = ScriptsList.objects.create(
                user = request.user,
                videoTitle = title,
                videoLink = videoLink,
                generatedScript = transcription,
                generatedSummary = cohere_content,
            )
            newScriptsList.save()

        # Send the result to JS so the user can see it.
        return JsonResponse({'script-content': transcription.strip(), 'summary': cohere_content})

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

def error_404_view(request, exception):
    return render(request, '404.html')