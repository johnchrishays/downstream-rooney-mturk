import boto3
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db import transaction
import json
import logging
import numpy as np
import time
from urllib.parse import urlencode

from .forms import ConsentForm
from .candidate_selection import SelectionProcess
from .models import SelectionProcess as SelectionProcessDBEnt
from .models import ResultHIT
from .models import QueuedHitParams
from .models import InProgressHits

from .submit_hit import USING_SANDBOX

logger = logging.getLogger(__name__)

MTURK_SANDBOX_ENDPOINT_URL = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
MTURK_ENDPOINT_URL = 'https://mturk-requester.us-east-1.amazonaws.com'

MTURK_SANDBOX_EXTERNAL_SUBMIT = 'https://workersandbox.mturk.com/mturk/externalSubmit'
MTURK_EXTERNAL_SUBMIT = 'https://www.mturk.com/mturk/externalSubmit'

mturk = boto3.client(
   'mturk',
   aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
   region_name='us-east-1',
   endpoint_url=MTURK_SANDBOX_ENDPOINT_URL if USING_SANDBOX else MTURK_ENDPOINT_URL
)

@xframe_options_exempt
@csrf_exempt
def index(request):
    """ GET and POST requests for the consent requests. """
    if request.method != 'POST':
        assignment_id = request.GET.get('assignmentId', 'ASSIGNMENT_ID_NOT_AVAILABLE')
        worker_id = request.GET.get('workerId', 'WORKER_ID_NOT_AVAILABLE')
        hit_id = request.GET.get('hitId', "HIT_ID_NOT_AVAILABLE")
        if (assignment_id == 'ASSIGNMENT_ID_NOT_AVAILABLE'):
            return HttpResponseRedirect('iteration/')
        else:
            if (InProgressHits.objects.filter(pk=assignment_id)):
                obj = InProgressHits.objects.get(pk=assignment_id)
                context = {
                    "assignment_id": obj.assignment_id, "worker_id": obj.worker_id, "hit_id": obj.hit_id,
                    "n_x": obj.n_x,
                    "n_y": obj.n_y,
                    "k": obj.k,
                    "l": obj.l,
                    "n_iterations": obj.n_iterations,
                    "bias": obj.bias,
                    "base_reward": obj.base_reward,
                    "avg_bonus_reward": obj.avg_bonus_reward,
                    "avg_n_minutes_to_complete": obj.avg_n_minutes_to_complete,
                    "pts_per_dollar": obj.pts_per_dollar,
                    "is_restore": True,
                    "selected_restore": obj.selected,
                    "db_entry_id_restore": obj.db_entry_id,
                    "true_utility_restore": obj.true_utility,
                    "round_completion_time_restore": obj.round_completion_time
                }
                return HttpResponseRedirect(f'iteration/?{urlencode(context)}')
            if (not USING_SANDBOX):
                next_token = ""
                while True:
                    # get list
                    hit_list = mturk.list_hits(NextToken=next_token) if next_token != "" else mturk.list_hits()
                    if ('NextToken' in hit_list):
                        next_token = hit_list['NextToken']
                    # process list
                    if (hit_list['NumResults'] > 0):  
                        for hit in hit_list["HITs"]:
                            hit_id = hit['HITId']
                            worker_results = mturk.list_assignments_for_hit(HITId=hit_id, AssignmentStatuses=['Approved', 'Submitted', 'Rejected'])
                            for assignment in worker_results['Assignments']:
                                if (assignment["WorkerId"] == worker_id):
                                    return HttpResponseRedirect('goodbye/')
                    else:
                        break
            with transaction.atomic():
                params = QueuedHitParams.objects.order_by("?").first()
                if (type(params) == type(None)):
                    return HttpResponseRedirect('nomorehits/')
                form = ConsentForm()
                context = {
                    'assignment_id': assignment_id,
                    'worker_id': worker_id,
                    'hit_id': hit_id,
                    'n_x': params.n_x, 'n_y': params.n_y, 'k': params.k, 'l': params.l,
                    'n_iterations': params.n_iterations,
                    'bias': params.bias,
                    'base_reward': params.base_reward,
                    'avg_bonus_reward': params.avg_bonus_reward,
                    'avg_n_minutes_to_complete': params.avg_n_minutes_to_complete,
                    'pts_per_dollar': params.pts_per_dollar,
                    'start_time': int(time.time()*1000),
                    'last_update_time': int(time.time()*1000)
                    
                }
                InProgressHits(**context).save()
                context.update({
                    'form': form, 
                    'external_submit_url': MTURK_SANDBOX_EXTERNAL_SUBMIT if USING_SANDBOX else MTURK_EXTERNAL_SUBMIT
                })
                params.delete()
            response = render(request, 'experiment/index.html', context)
            return response
    else:
        form = ConsentForm(request.POST)
        if form.is_valid():
            assignment_id = request.POST.get('assignment_id')
            hit_id = request.POST.get('hit_id')
            worker_id = request.POST.get('worker_id')
            over_18 = form.cleaned_data["over_18"]
            willing_to_participate = form.cleaned_data["willing_to_participate"]
            if (over_18 == "Yes" and willing_to_participate == "Yes"):
                context = {
                    "assignment_id": assignment_id, "worker_id": worker_id, "hit_id": hit_id,
                    "n_x": request.POST.get("n_x"),
                    "n_y": request.POST.get("n_y"),
                    "k": request.POST.get("k"),
                    "l": request.POST.get("l"),
                    "n_iterations": request.POST.get("n_iterations"),
                    "bias": request.POST.get("bias"),
                    "base_reward": request.POST.get("base_reward"),
                    "avg_bonus_reward": request.POST.get("avg_bonus_reward"),
                    "avg_n_minutes_to_complete": request.POST.get("avg_n_minutes_to_complete"),
                    "pts_per_dollar": request.POST.get("pts_per_dollar"),
                    "is_restore": False
                }
                return HttpResponseRedirect(f'iteration/?{urlencode(context)}')
            else:
                return HttpResponseRedirect('goodbye/')

@xframe_options_exempt
@csrf_exempt
def goodbye(request):
    return render(request, 'experiment/goodbye.html')

@xframe_options_exempt
@csrf_exempt
def nomorehits(request):
    return render(request, 'experiment/nomorehits.html')


@xframe_options_exempt
@csrf_exempt
def demo(request):
    cands_demo = [192, 190, 146, 150, 136, 126,  70,  44,  30,  34]
    noise = [ 4, -6,  8, -4,  0,  8, 12,  2, 2,  -2]
    pts_per_dollar = request.GET.get("pts_per_dollar")
    k = request.GET.get("k")
    l = request.GET.get("l")
    if (request.GET.get("page") == "-1"):
        n_iterations = request.GET.get("n_iterations")
        context = {
            'n_iterations': n_iterations,
            'pts_per_dollar': pts_per_dollar,
            'k': k,
            'l': l,
            'true_demo': [f"{round(x, 0):.0f}" for x in cands_demo],
            'perc_demo': [f"{round(x+y, 0):.0f}" for x, y in zip(cands_demo, noise)],
            'n_demo': len(cands_demo),
            'page': -1
        }
    elif (request.GET.get("page") == "0"):
        context = {
            'pts_per_dollar': pts_per_dollar,
            'k': k,
            'l': l,
            'cands_demo': [(i, f"{round(x+y, 0):.0f}") for x, y, i in zip(cands_demo, noise, list(range(len(cands_demo))))],
            'true_demo': [f"{round(x, 0):.0f}" for x in cands_demo],
            'perc_demo': [f"{round(x+y, 0):.0f}" for x, y in zip(cands_demo, noise)],
            'n_demo': len(cands_demo),
            'page': 0
        }
    return render(request, 'experiment/demo.html', context)


def __iteration_helper(json_is_x, n_x, n_y, k, l, n_iterations, bias):
    sp = SelectionProcess(n_x=n_x, n_y=n_y, k=k, l=l, bias=bias)

    perc_utils = np.concatenate((sp.xx_perceived, sp.yy_perceived))
    order = np.argsort(perc_utils)
    order = order[::-1]
    perc_utils = [perc_utils[i] for i in order]

    cand_strs = [f"{round(num*100,0):.0f}" for num in perc_utils]

    true_utils = np.concatenate((sp.xx, sp.yy))
    true_utils = [true_utils[i] for i in order]

    is_x = [1 for _ in range(n_x)] + [0 for _ in range(n_y)]
    is_x = [is_x[i] for i in order]

    sp_db_entry = SelectionProcessDBEnt(
        n_x=n_x, n_y=n_y, k=k, l=l, bias=bias,
        is_x=json.dumps(is_x), true_utils=json.dumps(true_utils),
        perc_utils=json.dumps(perc_utils))

    sp_db_entry.save()

    context = {
        'n_iterations': n_iterations,
        'n_x': n_x, 'n_y': n_y, 'k': k, 'l': l, 'bias': bias,
        'cands': "" if json_is_x else zip(list(range(n_x + n_y)), cand_strs, is_x, perc_utils),
        'cand_strs': json.dumps(cand_strs),
        'db_entry_id': sp_db_entry.id,
        'is_x': json.dumps(is_x) if json_is_x else is_x,
    }
    return context


@xframe_options_exempt
@csrf_exempt
def iteration(request):

    assignment_id = request.GET.get('assignment_id', 'ASSIGNMENT_ID_NOT_AVAILABLE')
    hit_id = request.GET.get('hit_id', 'HIT_ID_NOT_AVAILABLE')
    worker_id = request.GET.get('worker_id', 'WORKER_ID_NOT_AVAILABLE')

    if (request.method == "GET"):
        if (assignment_id != 'ASSIGNMENT_ID_NOT_AVAILABLE'):
            n_x = int(request.GET.get("n_x"))
            n_y = int(request.GET.get("n_y"))
            k = int(request.GET.get("k"))
            l = int(request.GET.get("l"))
            n_iterations = int(request.GET.get("n_iterations"))
            bias = float(request.GET.get("bias"))
            base_reward = request.GET.get("base_reward")
            avg_bonus_reward = request.GET.get("avg_bonus_reward")
            avg_n_minutes_to_complete = request.GET.get("avg_n_minutes_to_complete")
            pts_per_dollar = int(request.GET.get("pts_per_dollar"))
            is_restore = request.GET.get("is_restore")
        else:
            n_x = 50
            n_y = 50
            k = 10
            l = 0
            n_iterations = 24
            bias = 2/3
            base_reward = f"{1.00:0.2f}"
            avg_bonus_reward = f"{1.20:0.2f}"
            avg_n_minutes_to_complete = 20
            pts_per_dollar = 15000
            is_restore = False
        context = __iteration_helper(False, n_x, n_y, k, l, n_iterations, bias)
        context.update({
            'assignment_id': assignment_id,
            'worker_id': worker_id,
            'hit_id': hit_id,
            'base_reward': base_reward,
            'avg_bonus_reward': avg_bonus_reward,
            'avg_n_minutes_to_complete': avg_n_minutes_to_complete,
            'pts_per_dollar': pts_per_dollar,
            'external_submit_url': MTURK_SANDBOX_EXTERNAL_SUBMIT if USING_SANDBOX else MTURK_EXTERNAL_SUBMIT,
            'is_restore': is_restore
        })
        if (assignment_id != 'ASSIGNMENT_ID_NOT_AVAILABLE'):
            context.update({
                "selected_restore": request.GET.get("selected_restore"),
                "db_entry_id_restore": request.GET.get("db_entry_id_restore"),
                "true_utility_restore": request.GET.get("true_utility_restore"),
                "round_completion_time_restore": request.GET.get("round_completion_time_restore"),
            })
        return render(request, 'experiment/iteration.html', context)


@xframe_options_exempt
def iteration_json(request):
    if request.method == "GET":
        n_x = int(request.GET.get("n_x"))
        n_y = int(request.GET.get("n_y"))
        k = int(request.GET.get("k"))
        l = int(request.GET.get("l"))
        n_iterations = int(request.GET.get("n_iterations"))
        bias = float(request.GET.get("bias"))
        context = __iteration_helper(True, n_x, n_y, k, l, n_iterations, bias)
        return JsonResponse(context)


@xframe_options_exempt
def submit(request):
    db_entry_id = json.loads(request.GET.get("db_entry_id"))
    sp_db_entry = SelectionProcessDBEnt.objects.get(pk=db_entry_id)
    selected_array = json.loads(request.GET.get("selected_array"))
    round_completion_time = json.loads(request.GET.get("round_completion_time"))
    # Update in progress db entry
    in_progress_hit = InProgressHits.objects.get(pk=request.GET.get('assignment_id'))
    # Selected items
    selected_db = json.loads(in_progress_hit.selected)
    selected_db.append(selected_array)
    in_progress_hit.selected = json.dumps(selected_db)
    # DB entry
    db_entry_id_db = json.loads(in_progress_hit.db_entry_id)
    db_entry_id_db.append(db_entry_id)
    in_progress_hit.db_entry_id = json.dumps(db_entry_id_db)
    # Round completion ties
    round_completion_time_db = json.loads(in_progress_hit.round_completion_time)
    round_completion_time_db.append(round_completion_time)
    in_progress_hit.round_completion_time = json.dumps(round_completion_time_db)
    # Last update time
    in_progress_hit.last_update_time = int(time.time()*1000)

    if (len(selected_array) > sp_db_entry.k):
        raise ValueError(f"More than {sp_db_entry.k} items were selected.")
    true_utils = np.array(json.loads(sp_db_entry.true_utils))[selected_array]
    perc_utils = np.array(json.loads(sp_db_entry.perc_utils))[selected_array]
    
    # True utility
    true_utility = json.loads(in_progress_hit.true_utility)
    true_utility.append(sum([round(float(num)*100,0) for num in true_utils]))
    in_progress_hit.true_utility = true_utility
    in_progress_hit.save()
    true_utils = [f"{round(float(num)*100,0):.0f}" for num in true_utils]
    perc_utils = [f"{round(float(num)*100,0):.0f}" for num in perc_utils]

    response = JsonResponse({
        "true": json.dumps(true_utils),
        "perc": json.dumps(perc_utils)
    })
    return response


@xframe_options_exempt
def indep_submit(request):
    true_utility = request.GET.getlist("true_utility[]", "")
    true_utility = list(map(float, true_utility))
    perc_utility = request.GET.getlist("perc_utility[]", "")
    perc_utility = list(map(float, perc_utility))
    num_selected_x_cands = request.GET.getlist("num_selected_x_cands[]", "")
    num_selected_x_cands = list(map(int, num_selected_x_cands))
    sp_entry_id = request.GET.getlist("db_entry_id[]", "")
    sp_entry_id = list(map(int, sp_entry_id))

    result_hit_db_entry = ResultHIT(
        true_utility=json.dumps(true_utility),
        perc_utility=json.dumps(perc_utility),
        num_selected_x_cands=json.dumps(num_selected_x_cands),
        sp_entry_id=sp_entry_id)
    result_hit_db_entry.save()

    return JsonResponse({"success": "true"})
