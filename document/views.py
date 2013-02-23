# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from common.shortcuts import render_to_response
from forms import ProposalForm
from django.contrib.auth.decorators import login_required
from models import FullDocument

def documentView(request, document_slug, document_version=None):
    ## get the document
    if document_version == None:
        fulldocument = FullDocument.getFinalVersionFromSlug(document_slug)
    else:
        fulldocument = FullDocument.objects.get(slug=document_slug, version=document_version)
    ## Initialize the form either fresh or with the appropriate POST data as the instance
    if request.method == 'POST':
        form = ProposalForm(request.POST, instance=fulldocument)
        if form.is_valid():
            proposal = form.save(user = request.user)
            return HttpResponseRedirect(reverse('proposals-detail', args=(proposal.slug, )))
        else:
            pass
    else:
        form = ProposalForm(instance=fulldocument)

    return render_to_response(request, 'document/detail.html', {
        'form': form,
        'fulldocument': fulldocument
    })
