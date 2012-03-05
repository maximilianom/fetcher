from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from forms import UploadedFileForm
from models import Request

from utils.fetcher import Fetcher
from utils.uploader import UploaderHandler

@login_required
def index(request):
    form = UploadedFileForm()
    return render_to_response('index.html', {'form': form},
                              context_instance=RequestContext(request))

@login_required
def process(request):
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            motive = form.cleaned_data["motive"]
            instances_used = form.cleaned_data["instance_num"]
            seed_content = request.FILES['file'].read()

            #Could not parse directly from form because of the file
            req_model = Request()
            req_model.motive = motive
            req_model.instances_used = instances_used
            req_model.user = request.user
            req_model.content = seed_content
            req_model.save()

            #fetcher = Fetcher("fetch_queue", instance_num)
            #fetcher.fetch(seed_content)

    if request.method == 'GET':
        req_model = Request.objects.order_by('-created_at')[0:1].get()


    return render_to_response('process.html',
                             {'instance_num': req_model.instances_used,
                              'seed_content': req_model.content},
                              context_instance=RequestContext(request))

@login_required
def add_machine(request):
    #uploader = UploaderHandler()
    #uploader.add_instance()

    req_model = Request.objects.order_by('-created_at')[0:1].get()
    req_model.instances_used += 1
    req_model.save()

    return HttpResponseRedirect('/process')

@login_required
def stop(request):
    uploader = UploaderHandler()
    uploader.stop()
    return HttpResponseRedirect('/')
