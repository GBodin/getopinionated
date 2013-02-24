from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from models import VotablePost, UpDownVote, Proposal, Comment, ProposalVote
from forms import CommentForm
from proposing.models import Tag
from django.db.models import Count

def index(request):
    first_5_proposals = Proposal.objects.order_by('create_date')[:]#for debugging purposes, results should actually be paginated
    taglist = Tag.objects.annotate(num_props=Count('proposals')).order_by('-num_props')
    return render(request, 'proposal/list.html', {
        'latest_proposal_list': first_5_proposals,
        'taglist': taglist
    })

def detail(request, proposal_slug):
    proposal = get_object_or_404(Proposal, slug=proposal_slug)
    commentform = CommentForm()
    proposal.addView()
    
    if proposal.isFinished:
        if not proposal.merged:
            proposal.initiateVoteCount()
        return render(request, 'proposal/detail.html', {
            'proposal': proposal,
            'commentform': commentform,
        })
    elif proposal.isVoting:
        return render(request, 'proposal/detail.html', {
            'proposal': proposal,
        })
    else:
        if request.method == 'POST':
            commentform = CommentForm(request.POST)
            if commentform.is_valid():
                commentform.save(proposal, request.user)
                messages.success(request, 'Comment added')
                return HttpResponseRedirect(reverse('proposals-detail', args=(proposal_slug,)))
        else:
            commentform = CommentForm()
            proposal.addView()
    return render(request, 'proposal/detail.html', {
        'proposal': proposal,
        'commentform': commentform,
    })

@login_required
def vote(request, proposal_slug, post_id, updown):
    # get vars
    post = get_object_or_404(VotablePost, pk=post_id)
    user = request.user
    proposal_detail_redirect = HttpResponseRedirect(reverse('proposals-detail', args=(proposal_slug,)))
    assert updown in ['up', 'down'], 'illegal updown value'
    # check if upvote can be undone
    if post.user_has_updownvoted(user) != None:
        if post.user_has_updownvoted(user) == updown:
            vote = post.updownvote_from_user(user)
            vote.delete()
            messages.success(request, "Vote removed successfully")
        else:
            messages.error(request, "You already voted on this post")
        return proposal_detail_redirect
    # check if upvote is allowed
    if not post.user_can_updownvote(user):
        messages.error(request, "You can't vote on this post")
        return proposal_detail_redirect
    # create updownvote
    vote = UpDownVote(
        user = user,
        post = post,
        is_up = (updown == 'up'),
    )
    vote.save()
    # redirect
    messages.success(request, "Vote successful")
    return proposal_detail_redirect

@login_required
def proposalvote(request, proposal_slug, updown):
    # get vars
    proposal = get_object_or_404(Proposal, slug=proposal_slug)
    user = request.user
    proposal_detail_redirect = HttpResponseRedirect(reverse('proposals-detail', args=(proposal_slug,)))
    assert updown in ['-5', '-4', '-3', '-2', '-1', '0', '+1', '+2', '+3', '+4', '+5'], 'illegal vote'
    # remove the previous vote of the user
    if proposal.user_has_proposalvoted(user) != None:
        vote = proposal.proposalvote_from_user(user)
        vote.delete()
    # check if upvote is allowed
    if not proposal.user_can_proposalvote(user):
        messages.error(request, "You can't vote on this proposal")
        return proposal_detail_redirect
    # create updownvote
    votevalue = int(float(updown))
    vote = ProposalVote(
        user = user,
        proposal = proposal,
        value = votevalue,
    )
    vote.save()
    # redirect
    messages.success(request, "Vote successful")
    return proposal_detail_redirect
