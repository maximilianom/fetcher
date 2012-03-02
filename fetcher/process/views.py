from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import UploadedFileForm
from django.http import HttpResponseRedirect

from utils.fetcher import Fetcher

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
            instance_num = form.cleaned_data["instance_num"]
            seed_content = request.FILES['file'].read()

            fetcher = Fetcher("fetch_queue", instance_num)
            fetcher.fetch(seed_content)

            return HttpResponseRedirect('/')
