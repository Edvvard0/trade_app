from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from ads.models import Ad
from exchange.forms import ExchangeProposalForm
from exchange.models import ExchangeProposal


@login_required
def get_my_proposals(request):
    user = request.user
    proposals = ExchangeProposal.objects.filter(ad_receiver__user=user)

    return render(request, "exchange/my_proposal.html", context={"proposals": proposals})

@login_required
def get_proposals_sent_me(request):
    user = request.user
    proposals = ExchangeProposal.objects.filter(ad_sender__user=user)

    return render(request, "exchange/my_proposal.html", context={"proposals": proposals})


@login_required
def get_current_proposal(request, id):
    proposal = ExchangeProposal.objects.get(id=id)
    return render(request, "exchange/current_proposal.html", context={"proposal": proposal})


@login_required
def accept_proposal(request, id):
    proposal = ExchangeProposal.objects.get(id=id)
    proposal.status = "принята"
    proposal.save()

    return HttpResponseRedirect(reverse("my_proposals"))


@login_required
def reject_proposal(request, id):
    proposal = ExchangeProposal.objects.get(id=id)
    proposal.status = "отклонена"
    proposal.save()

    return HttpResponseRedirect(reverse("my_proposals"))


@login_required
def create_proposal(request):
    user = request.user
    my_ads = Ad.objects.filter(user=user)
    other_ads = Ad.objects.exclude(user=user)

    if request.method == "POST":
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            ExchangeProposal.objects.create(**cd)
            return HttpResponseRedirect(reverse("all_ads"))

    else:
        form = ExchangeProposalForm()

    return render(request,
                  "exchange/create_change_proposal.html",
                  context={"form": form,
                          "my_proposals_change": my_ads,
                          "other_proposals_change": other_ads,})


@login_required
def update_proposal(request, id):
    user = request.user

    proposal = get_object_or_404(ExchangeProposal, pk=id)
    my_ads = Ad.objects.filter(user=user)
    other_ads = Ad.objects.exclude(user=user)

    if proposal.ad_sender.user != user:
        return HttpResponseForbidden("Вы не можете редактировать это объявление")

    if request.method == "POST":
        form = ExchangeProposalForm(request.POST, instance=proposal)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("my_proposals"))
    else:
        form = ExchangeProposalForm()

    return render(request,
                  "exchange/create_change_proposal.html",
                  context={"form": form,
                          "my_proposals_change": my_ads,
                          "other_proposals_change": other_ads,
                           "proposal": proposal})


# @login_required
# def update_ad(request, id):
#     ad = get_object_or_404(Ad, pk=id)
#     if ad.user != request.user:
#         return HttpResponseForbidden("Вы не можете редактировать это объявление")
#
#     if request.method == "POST":
#         form = AdUpdateForm(request.POST, instance=ad)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("my_ads"))
#     else:
#         form = AdUpdateForm(instance=ad)
#
#     return render(request, "ads/update_ad.html", {"form": form, "ad": ad})


@login_required
def delete_proposal(request, id):
    proposal = ExchangeProposal.objects.get(id=id)
    if proposal.ad_sender.user != request.user:
        return HttpResponseForbidden("Вы не можете удалить это объявление")

    proposal.delete()
    return HttpResponseRedirect(reverse("my_ads"))

