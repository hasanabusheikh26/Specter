#API SECRET OPENAI =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
from django.shortcuts import render ,redirect
from django.contrib import messages
import openai
from .models import Past
from django.core.paginator import Paginator
from django.contrib.auth import authenticate , login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm

# Create your homepagehere.
def home(request):
    past_questions = Past.objects.all()  # Fetch all past questions from the database
    
    if request.method == "POST":
        question = request.POST['question']
        past_responses = request.POST['past_responses']
        
        # API Stuff
        openai.api_key = "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"
        openai.Model.list()
        
        try:
            # Make a completion or a request
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Respond only with law terms for {question}",
                temperature=0,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
            
            # Parse Response
            response = (response["choices"][0]["text"]).strip()
            
            # Logic for passing the response
            if "41oance31" in past_responses:
                past_responses = response
            else:
                past_responses = f"{past_responses}<br/><br/>{response}"
            
            # Save to Database
            record = Past(question=question, answer=response, user=request.user)
            record.save()
            
            return render(request, 'home.html', {"question": question, "response": response, "past_responses": past_responses, "past_questions": past_questions})
        
        except:
            error_message = "An error occurred while processing your request."
            return render(request, 'home.html', {"error_message": error_message, "past_questions": past_questions})
    
    else:
        return render(request, 'home.html', {"past_questions": past_questions})
    



    
def past(request):
    if request.user.is_authenticated:
        past=Past.objects.filter(user_id=request.user.id)
        p=Paginator(Past.objects.filter(user_id=request.user.id),5)
        page=request.GET.get('page')
        pages=p.get_page(page)
        nums = "a"*pages.paginator.num_pages
        return render(request, 'past.html', {"past":past , "pages":pages , "nums":nums})
    else:
        messages.success(request, "You Must Be Logged In To View this page")
        return redirect('home')
    
    
    return render(request ,'past.html', {"past":past , "pages":pages , "nums":nums})  
#pass a request and pass a pk a primary key
def delete_past(request , Past_id):
    past = Past.objects.get(pk=Past_id)
    past.delete()
    messages.success(request, ("That Question and answer has been deleted"))
    return redirect('past')


def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!  Woohoo!")
			return redirect('home')
		else:
			messages.success(request, "Error Logging In. Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out... Have A Nice Day!")
	return redirect('home')


def register_user(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Registered...Congrats!!")
			return redirect('home')
	else:
		form = SignUpForm()

	return render(request, 'register.html', {"form": form}) 
