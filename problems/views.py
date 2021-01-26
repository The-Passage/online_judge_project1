from typing import Text
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import problemset, submission
from django.core.exceptions import ObjectDoesNotExist
from .forms import UploadFileForm
from django.urls import reverse
import time
import json
try:
    import requests
except:
    render(request, 'home/404.html')
# Create your views here.

def problem_list(request):
    context = {}

    if request.user.is_authenticated:
        context['username'] = request.user.username

    l = problemset.objects.all()

    context['problemset'] = l

    return render(request, 'problemlist/problem_list.html', context)

def show_problem(request, pk=None):
    try:
        problem = problemset.objects.get(pk=pk)
        context = {}

        if request.user.is_authenticated:
            context['username'] = request.user.username
        
        context['problem'] = problem
        Ac_Languages=requests.get('https://ce.judge0.com/languages/')
        Ac_Languages=Ac_Languages.json()
        context['Ac_Laguages']=Ac_Languages
        if request.method == 'POST':
            form = UploadFileForm(request.FILES['datafile'])
            if form:
                language = request.POST['filetype']
                uploaded_file = request.FILES['datafile']
                problem_id = problem

                ufname = str(uploaded_file)
                x = ufname.split('.')
                file_extension = x[len(x)-1]
                ext=[
                    "asm","sh","bas",
                    "c","cpp","clj",
                    "cs","cob","lisp",
                    "d","exs","erl",
                    "out","fsx","f90",
                    "go","groovy","hs",
                    "java","js","kt",
                    "lua","m","ml",
                    "m","pas","pl",
                    "php","txt","pro",
                    "py","r","rb",
                    "rs","scala","sql",
                    "swift","ts","vb"
                    ]
                if file_extension not in ext:
                    return render(request, 'problemlist/problem_detail.html', context)

                #start api 
                file1= uploaded_file.read()
                #if language=="Python":
                #    ln_id = 71
                #elif language=="C":
                #    ln_id = 50
                #else:
                #    ln_id = 54
                ln_id=language   
                headers = [
                        {
                            "x-rapidapi-key": "80fc940158msh9451a16b61ac5c9p1ed428jsn0854194c0005",
                            "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
                        },
                        {
                            "x-rapidapi-key": "4164c32ed8mshe8f0b4f6d75f9f2p125131jsn2cc72f13689e",
                            "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
                        },
                        {
                            "x-rapidapi-key": "7287064a7amshf61e91dec1454b2p13671cjsn504ff2084e6f",
                            "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
                        }
                    ]
                payload={"source_code": file1,
                    "language_id": ln_id,
                    "number_of_runs": 1,
                    "stdin": problem.problem_input,
                    "expected_output": problem.problem_output,
                    "cpu_time_limit": problem.problem_time_limit,
                    "enable_wait_result":True,
                    "cpu_extra_time": 0.5,
                    "wall_time_limit": 20,
                    "memory_limit": 128000,
                    "stack_limit": 128000,
                    "enable_per_process_and_thread_time_limit": False,
                    "enable_per_process_and_thread_memory_limit": False,
                    "max_file_size": 1024
                }

                url='https://judge0-ce.p.rapidapi.com/submissions/?base64_encoded=false&wait=false'
                
                for i in range(3):
                    r = requests.post(url,headers=headers[i],data=payload)
                    token = r.json()
                    if token['token']:
                        t_id = token['token']
                        break

                while True:
                    url2="https://api.judge0.com/submissions/%s?base64_encoded=false&fields=status_id"%(t_id)
                    r2=requests.get(url2)
                    r2=r2.json()
                    print(r2)
                    st_url='https://api.judge0.com/statuses'
                    url_3=requests.get(st_url)
                    url_3=url_3.json()
                    status_id = r2['status_id']-1
                    judge_result = url_3[status_id]['description']
                    if judge_result != "Processing" and judge_result != "In Queue":
                        break
                if(judge_result == 'Accepted'):
                    problem.total_solve = problem.total_solve + 1
                problem.total_submit = problem.total_submit + 1
                problem.save()
                instance = submission(problem_id=problem_id, user_id=request.user, uploaded_file=uploaded_file, language=language,token_id=t_id,judge_result=judge_result)
                instance.save()
                # redirect to submission page
                return HttpResponseRedirect(reverse('show_submission'))


        return render(request, 'problemlist/problem_detail.html', context)

    except ObjectDoesNotExist:
        return render(request, '404.html')

def show_submission(request):
    context = {}

    if request.user.is_authenticated:
        context['username'] = request.user.username
    l = submission.objects.all().order_by('-submission_time')
    context['submission'] = l

    return render(request, 'problemlist/show_submission.html', context)

def individual_submission(request, pk=None):
    try:
        context = {}
        if request.user.is_authenticated:
            context['username'] = request.user.username

        q = submission.objects.get(pk=pk)
        f = open(str(q.uploaded_file), 'r')

        file_content = f.read()
        f.close()

        context['file_content'] = file_content
        context['submission'] = q
        return render(request, 'problemlist/individual_submission.html', context)
    
    except:
        return render(request, '404.html')

def csrf_failure(request, reason=""):
    return render(request, '404.html')