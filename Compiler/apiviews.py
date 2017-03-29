import signal
from rest_framework.decorators import api_view
import subprocess,os
import json
from models import *

from django.contrib.auth import authenticate
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
import time
import operator


import pytz

local_tz = pytz.timezone('Asia/Kolkata') # use your local timezone name here
# NOTE: pytz.reference.LocalTimezone() would produce wrong result here

## You could use `tzlocal` module to get local timezone on Unix and Win32
# from tzlocal import get_localzone # $ pip install tzlocal

# # get local timezone
# local_tz = get_localzone()

def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt) # .normalize might be unnecessary


def date_time_milliseconds(date_time_obj):
   return int(time.mktime(date_time_obj.timetuple()) * 1000)

@api_view(['GET', 'POST'])
def startTimer(request,pk) :
    prob = Problem.objects.filter(pk=pk)
    TimerProblem.objects.get_or_create(question=prob[0],user=request.user)
    return Response({'id' : pk})


@api_view(['GET', 'POST'])
def getTimer(request,pk) :
    prob = Problem.objects.filter(pk=pk)
    time = TimerProblem.objects.get(question=prob[0],user=request.user)
    tt = time.time_init
    tt = utc_to_local(tt)

    # return Response({'hr' : tt.hour,'min':tt.minute,'sec':tt.second})
    ret_time =date_time_milliseconds(tt)
    return Response({'tt':ret_time})

@api_view(['GET', 'POST'])
def results(request):
    users = User.objects.all()
    res ={}

    for user in users :
        marks =0
        solved =0
        sol = Solution.objects.filter(user=user)
        for s in sol :
            in_time = TimerProblem.objects.get(user=user,question=s.question)
            t =date_time_milliseconds(s.submission_time) - date_time_milliseconds(in_time.time_init)
            t = t/1000
            t = t/60
            factor = 0
            if t < 5000:
                factor = 3
            elif t > 5000 and t < 10000:
                factor = 2
            else :
                factor = 1
            solved +=1
            marks = marks + 1000 + ((marks*factor)/10)

        res[user.username] = [marks,solved]

    # sorted_x = sorted(res.items(), key=operator.itemgetter(1))
    sorted_x = sorted(res.items(), key=lambda  e: -e[1][0])

    return Response({'results' :sorted_x})


# @csrf_exempt
@api_view(['GET', 'POST'])
def compile(request) :
    # prog = str(request.POST['program'])
    lang = str(request.POST['language'])
    prog = request.POST['program']
    # lines = prog.split('/')
    inp_name = str(request.POST['prog_name']) + request.user.username
    if lang=='C':
        inp_fname = inp_name+'.c'
        inp_file = open(inp_fname,'w')
        # for line in lines :
        inp_file.writelines(prog )

        inp_file.close()
        output = open(inp_name+'output.txt','w')
        error_op = open(inp_name+'error.txt','w')
        p =subprocess.Popen(['gcc',inp_fname,'-o',inp_name+'.exe'],stdout=output, stderr=error_op)
        p.wait()
        # output.flush()
        p.kill()
        output.close()
        error_op.close()
        output = open(inp_name+'output.txt')
        error_op = open(inp_name+'error.txt')
        out = ''
        errors =''
        for l in output:
            out +=l
        for l in error_op :
            errors += l
        #
        # output.flush()
        # error_op.flush()
        output.close()
        error_op.close()
        os.remove(inp_name+'output.txt')
        os.remove(inp_name+'error.txt')
        os.remove(inp_fname)
        state = False
        if errors=='':
            state = True



    return Response({'typeOp':'compile','compiled' : state,'output':out,'errors' : errors })

from time import sleep
@api_view(['GET', 'POST'])
def run(request) :
    lang = str(request.POST['language'])
    prog = request.POST['program']
    # lines = prog.split('/')
    fname = str(request.POST['prog_name'])+ request.user.username
    input_data = request.POST['prog_input']
    aux_name = fname +'r'
    inp_file = open(aux_name+'input.txt', 'w')
    inp_file.writelines(input_data)
    inp_file.close()
    inp_file = open(aux_name + 'input.txt')
    output = open(aux_name + 'output.txt', 'w')
    error_op = open(aux_name + 'error.txt', 'w')

    if lang == 'C':
        if os.path.isfile(fname+'.exe') :
            p = subprocess.Popen(fname+'.exe',stdin=inp_file, stdout=output, stderr=error_op)
            # p.wait()
            for t in xrange(4):
                sleep(1)
                if p.poll() is not None:
                    x= p.communicate()
                    break

            # p.kill()
            # os.kill(p.pid,signal.SIGINT)

            output.close()
            error_op.close()

            # pid = p.pid
            p.terminate()

            # Check if the process has really terminated & force kill if not.
            try:
                # os.kill(p.pid, 0)
                p.kill()
                print "Forced kill"
            except OSError, e:
                print "Terminated gracefully"

            # sleep(5)
            output = open(aux_name + 'output.txt')
            error_op = open(aux_name + 'error.txt')
            out = ''
            errors = ''
            if(os.stat(aux_name + 'output.txt').st_size < 1000 ) and t<3:
                for l in output:
                    out += l+'<br>'
                for l in error_op:
                    errors += l
            else :
                errors += 'TLE'
                out += 'Too much o/p to display'

            # output.flush()
            # error_op.flush()
            output.close()
            error_op.close()
            inp_file.close()

            # os.remove(inp_fname)

            state = False
            if errors == '':
                state = True
            # p.kill()
            os.remove(aux_name + 'output.txt')
            os.remove(aux_name + 'error.txt')
            os.remove(aux_name + 'input.txt')
        else :
            output.close()
            error_op.close()
            inp_file.close()
            os.remove(aux_name + 'output.txt')
            os.remove(aux_name + 'error.txt')
            os.remove(aux_name + 'input.txt')

            return Response({'typeOp': 'run', 'executed': False, 'compiled': False})

    return Response({'typeOp':'run','executed':state, 'output':out, 'errors':errors})

@api_view(['GET', 'POST'])
@login_required()
def submit(request) :
    lang = str(request.POST['language'])
    prog = request.POST['program']
    # lines = prog.split('/')
    prob = int(request.POST['prob'])
    prob = Problem.objects.get(pk=prob)
    tests = prob.tests.all()
    fname = str(request.POST['prog_name'])+ request.user.username
    all_pass = True

    sub_status ={}
    for test in tests :
        input_data = request.POST['prog_input']
        aux_name = fname + test.test_name
        inp_file = open(aux_name +'input.txt', 'w')
        for line in test.prog_input.split('\\n'):
            inp_file.write(line+'\n')
        inp_file.close()
        inp_file = open(aux_name + 'input.txt')
        output = open(aux_name + 'output.txt', 'w')
        error_op = open(aux_name + 'error.txt', 'w')

        if lang == 'C':
            if os.path.isfile(fname+'.exe') :
                p = subprocess.Popen(fname+'.exe',stdin=inp_file, stdout=output, stderr=error_op)
                # p.wait()
                for t in xrange(4):
                    sleep(1)
                    if p.poll() is not None:
                        x= p.communicate()
                        break
                # p.kill()

                output.close()
                error_op.close()
                # pid = p.pid
                p.terminate()
                try:
                    # os.kill(p.pid, 0)
                    p.kill()
                    print "Forced kill"
                except OSError, e:
                    print "Terminated gracefully"

                sleep(5)
                output = open(aux_name + 'output.txt', 'r')
                error_op = open(aux_name + 'error.txt', 'r')
                out = ''
                errors = ''
                if(os.stat(aux_name + 'output.txt').st_size < 1000 ) and t<3:
                    for l in output:
                        out += l
                    for l in error_op:
                        errors += l
                else :
                    errors += 'TLE'
                    out += 'Too much o/p to display'

                inp_file.close()
                output.flush()
                error_op.flush()
                output.close()
                error_op.close()
                os.remove(aux_name + 'output.txt')
                os.remove(aux_name + 'error.txt')
                os.remove(aux_name + 'input.txt')
                # os.remove(inp_fname)
                state = False
                if errors == '':
                    state = True
                # p.kill()
                correctness = False
                if out.split('\n') == test.output.split('\\n'):
                    correctness = True
                else:
                    all_pass = False

                sub_status[test.test_name] = {'executed' : state,'match' : correctness,'errors' : errors }
                # return Response({'typeOp':'run','executed' : state,'output':out,'errors' : errors })
            else :
                os.remove(aux_name + 'output.txt')
                os.remove(aux_name + 'error.txt')
                inp_file.close()
                return Response({'typeOp': 'submit', 'executed': False, 'compiled': False})

    if all_pass:
        try:
            sol = Solution.objects.get( question=prob,user=request.user)
            if sol:
                pass
        except Solution.DoesNotExist as e:

            sol = Solution.objects.create( question=prob, program=prog, user=request.user)
        # sol = Solution.objects.create(submission_name= str(request.user) +fname, question=prob, program =prog, user=request.user)
            sol.save()

    return Response({'typeOp':'submit','executed':True, 'cases' : sub_status})