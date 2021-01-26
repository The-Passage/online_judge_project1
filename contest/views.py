from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from .models import contest as contest_table
from .models import contest_problemset
from .models import contest_submission
from .models import contestant_point
from .models import contest_upsolve_submission
from django.core import serializers
from .forms import UploadFileForm
from django.urls import reverse
import datetime
from datetime import timezone
import pickle
import json
import os
import time
import math
import traceback
import sys
import subprocess
try:
    import requests
except:
    render(request, 'home/404.html')

# Create your views here.

def contest_list(request):
    try:
        context = {}
        if request.user.is_authenticated:
            context['username'] = request.user.username

        l = contest_table.objects.filter(end_time__gte = datetime.datetime.now())
        context['contest_list'] = l

        m = contest_table.objects.filter(end_time__lte = datetime.datetime.now(), start_time__lte = datetime.datetime.now())
        context['past_contest'] = m
        return render(request, 'contest/contest_list.html', context)
    except:
        return render(request, '404.html')

def contest_info(request, pk=None):
    try:
        context = {}
        if request.user.is_authenticated:
            context['username'] = request.user.username

        l = contest_table.objects.get(pk=pk)
        context['contest_info'] = l

        #calculating contest duration
        tm = l.end_time - l.start_time

        context['contest_duration'] = tm
        context["contest_id"] = pk

        return render(request, 'contest/contest_info.html', context)

    except ObjectDoesNotExist:
        return render(request, 'home/404.html')

def contest_pass_test(request, pk=None):
    try:
        context = {}
        contest_info = contest_table.objects.get(pk=pk)
        context['contest_info'] = contest_info
        if contest_info.is_password_protected:
            if request.user.is_authenticated:
                if request.method=='POST':
                    p1 = request.POST['contest_pass']
                    if p1 == contest_info.contest_password:
                        return HttpResponseRedirect(reverse('contest_dashboard', kwargs={'pk': pk}))
                    else:
                        context['contest_error'] = "incorroect password"
                        return render(request, 'contest/contest_pass.html', context)
                        #return render(request, 'contest/contest_info.html')
                else:
                    return render(request, 'contest/contest_pass.html', context)
            else:
                return render(request, 'contest/contest_info.html')
        else:
            return HttpResponseRedirect(reverse('contest_dashboard', kwargs={'pk': pk}))
    except Exception:
        traceback.print_exc()
        return render(request, '404.html')

def contest_dashboard(request, pk=None):
    #gather contest info
    context = {}
    contest_info = contest_table.objects.get(pk=pk)
    context['contest_info'] = contest_info
    start_time = contest_info.start_time
    current_time = datetime.datetime.now(timezone.utc)
    sub = start_time.timestamp() - current_time.timestamp()

    if sub > 0.0:
        return render(request, '404.html')

    if request.user.is_authenticated:
        context['username'] = request.user.username

    #context['contest_info'] = contest_info

    #gather problem set for this contest
    problemset = contest_problemset.objects.filter(contest_id__id=pk).order_by('problem_title')

    context['problemset'] = problemset

    context['contest_id'] = pk

    return render(request, 'contest/contest_dashboard.html', context)

def contest_show_problem(request, pk=None, problem_id=None):
    try:
        # Gather this problem related data
        problem = contest_problemset.objects.get(pk=problem_id)

        x = contest_table.objects.get(pk=pk)

        start_time = x.start_time
        current_time = datetime.datetime.now(timezone.utc)
        sub = start_time.timestamp() - current_time.timestamp()

        if sub > 0.0:
            return render(request, 'home/404.html')
        left = x.end_time.timestamp() - x.start_time.timestamp()
        context = {}
        
        this_contest = contest_table.objects.get(pk=pk)
        s_time = this_contest.start_time
        e_time = this_contest.end_time
        c_time = datetime.datetime.now(datetime.timezone.utc)
        sub1 = s_time.timestamp() - c_time.timestamp()
        sub2 = e_time.timestamp() - c_time.timestamp()

        if request.user.is_authenticated:
            context['username'] = request.user.username
            
        #Gather contest info
        contest_info = contest_table.objects.get(pk=pk)
        context['contest_info'] = contest_info

        
        context['problem'] = problem
        context['contest_id'] = pk

        Ac_Languages=requests.get('https://ce.judge0.com/languages/')
        Ac_Languages=Ac_Languages.json()
        context['Ac_Laguages']=Ac_Languages

        if request.method=='POST':
            if left > 0.0:
                form = UploadFileForm(request.FILES['datafile'])
                if form:
                    language = request.POST['filetype']
                    uploaded_file = request.FILES['datafile']

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
                        return render(request, 'contest/contest_problem_view.html', context)
                    problem_id = problem

                    #start api 
                    file1= uploaded_file.read()
                    #if language=="Python":
                    #    ln_id = 71
                    #elif language=="C":
                    #    ln_id = 50
                    #elif language=="C++":
                    #    ln_id = 54
                    ln_id = language
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
                    "expected_output": problem.problem_out,
                    "cpu_time_limit": 2,
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

                    if sub1 < 0.0 and sub2 > 0.0:
                        instance = contest_submission(problem_id=problem_id, user_id=request.user, uploaded_file=uploaded_file, language=language, token_id=t_id,judge_result=judge_result)
                        instance.save()
                        
                        #result making for standing
                        submission = contest_submission.objects.get(pk=instance.pk)
                        problem = contest_problemset.objects.get(pk=submission.problem_id.id)
                        problem.total_submit += 1
                        problem.save()

                        penalty = 0
                        solve = 0
                        submission_list = contest_submission.objects.filter(user_id=request.user, problem_id__contest_id__id=submission.problem_id.contest_id.id)
                        is_there_this_contestant = contestant_point.objects.filter(user_id=request.user, contest_id=submission.problem_id.contest_id).count()
                        if is_there_this_contestant==0:
                            instance1 = contestant_point(user_id=request.user, contest_id=submission.problem_id.contest_id)
                            instance1.save()
                        
                        contestant = contestant_point.objects.get(user_id=request.user, contest_id=submission.problem_id.contest_id.id)

                        for i in submission_list:
                            if(i.judge_result == "Accepted"):
                                problem.total_solve += 1
                                problem.save()
                                submission_time = i.submission_time
                                contest_start_time = i.problem_id.contest_id.start_time
                                pnt = submission_time.timestamp() - contest_start_time.timestamp()
                                penalty += math.ceil(pnt/60)
                                solve += 1
                            elif i.judge_result=="Wrong Answer" or i.judge_result=="Run Time Error":
                                ac_count = contest_submission.objects.filter(user_id=submission.user_id, problem_id=i.problem_id, judge_result="Accepted").count()
                                if ac_count != 0:
                                    penalty += 20

                        contestant.penalty = penalty
                        contestant.solve = solve
                        contestant.save()
                    else:
                        instance = contest_upsolve_submission(problem_id=problem_id, user_id=request.user, uploaded_file=uploaded_file, language=language, token_id=t_id,judge_result=judge_result)
                        instance.save()
                    #redirect to submission page
                    rl = reverse('contest_individual_submission', kwargs={'pk': pk})
                    return HttpResponseRedirect(rl)
                else:
                    return render(request, '404.html')
                
        return render(request, 'contest/contest_problem_view.html', context)
    
    except:
        return render(request, '404.html')

def contest_individual_submission(request, pk=None):
    contest_info = contest_table.objects.get(pk=pk)

    start_time = contest_info.start_time
    current_time = datetime.datetime.now(timezone.utc)
    sub = start_time.timestamp() - current_time.timestamp()
    end_time = contest_info.end_time
    if sub > 0.0:
        return render(request, 'home/404.html')

    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
    
    if end_time<current_time:
        context['pass'] = True
    else:
        context['pass'] = False
    
    #Gather submisssion data
    l = contest_submission.objects.filter(user_id=request.user, problem_id__contest_id__id=pk).order_by("-submission_time")
    context['contest_submission'] = l
    l1 = contest_upsolve_submission.objects.filter(user_id=request.user, problem_id__contest_id__id=pk).order_by("-submission_time")
    context['contest_upsolve_submission'] = l1
    #Gather contest related data
    
    context['contest_info'] = contest_info
    context['contest_id'] = pk

    return render(request, 'contest/contest_submission.html', context)


def contest_standing(request, pk=None):
    contest_info = contest_table.objects.get(pk=pk)

    start_time = contest_info.start_time
    current_time = datetime.datetime.now(timezone.utc)
    sub = start_time.timestamp() - current_time.timestamp()

    if sub > 0.0:
        return render(request, 'home/404.html')

    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username

    context = {}
    context['contest_id'] = pk

    if request.user.is_authenticated:
        context['username'] = request.user.username
    #Gather contest info
    

    context['contest_info'] = contest_info

    #Calculate ranklist
    user_list = contestant_point.objects.filter(contest_id=pk).order_by('-solve', 'penalty')
    problems = contest_problemset.objects.filter(contest_id=pk).order_by('problem_title')
    total_problem = problems.count()

    total_standing = []

    for i in user_list:
        user_info = []
        user_info.append(i.user_id.username)
        user_info.append(i.solve)
        user_info.append(i.penalty)

        data = []
        for j in problems:
            ac_count = contest_submission.objects.filter(user_id=i.user_id, problem_id=j.id, problem_id__contest_id__id=pk, judge_result="Accepted").count()
            submisssion_count = contest_submission.objects.filter(user_id=i.user_id, problem_id=j.id, problem_id__contest_id__id=pk).count()
            res = ""
            if ac_count != 0:
                res = "ac"
            elif submisssion_count != 0:
                res = "sub"
            else:
                res = "nosub"
            data.append(res)
        user_info.append(data)
        total_standing.append(user_info)

    context['standing'] = total_standing
    context['number_of_problems'] = total_problem
    context['pk'] = pk
    return render(request,'contest/contest_standing.html', context)
    

def contest_standing_server(request, pk=None):
    context = {}
    context['contest_id'] = pk

    if request.user.is_authenticated:
        context['username'] = request.user.username
    #Gather contest info
    contest_info = contest_table.objects.get(pk=pk)

    #Calculate ranklist
    user_list = contestant_point.objects.filter(contest_id=pk).order_by('-solve', 'penalty')
    problems = contest_problemset.objects.filter(contest_id=pk).order_by('problem_title')
    total_problem = problems.count()

    total_standing = []

    for i in user_list:
        user_info = []
        user_info.append(i.user_id.username)
        user_info.append(i.solve)
        user_info.append(i.penalty)

        data = []
        for j in problems:
            ac_count = contest_submission.objects.filter(user_id=i.user_id, problem_id=j.id, problem_id__contest_id__id=pk, judge_result="Accepted").count()
            submisssion_count = contest_submission.objects.filter(user_id=i.user_id, problem_id=j.id, problem_id__contest_id__id=pk).count()
            res = ""
            if ac_count != 0:
                res = "ac"
            elif submisssion_count != 0:
                res = "sub"
            else:
                res = "nosub"
            data.append(res)
        user_info.append(data)
        total_standing.append(user_info)

    context['standing'] = total_standing
    context['number_of_problems'] = total_problem
    context['pk'] = pk

    return HttpResponse(json.dumps(context))

def csrf_failure(request, reason=""):
    return render(request, '404.html')