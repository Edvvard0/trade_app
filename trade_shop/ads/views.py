from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from ads.forms import AdCreateForm, AdUpdateForm
from ads.models import Ad, CATEGORY_CHOICES, CONDITION_CHOICES
from ads.utils import q_search


def all_ads(request):
    all_ads = Ad.objects.all()

    page = request.GET.get("page", 1)
    category = request.GET.get("category", "")
    condition = request.GET.get("condition", "")


    if category:
        all_ads = all_ads.filter(category=category)
    if condition:
        all_ads = all_ads.filter(condition=condition)

    paginator = Paginator(all_ads, 2)
    current_page = paginator.page(page)

    context = {"ads": current_page,
               'page_obj': current_page,
               'category_choices': CATEGORY_CHOICES,
               'condition_choices': CONDITION_CHOICES,
               }

    return render(request, "ads/all_ads.html", context=context)


def current_ad(request, id):
    ad = get_object_or_404(Ad, pk=id)
    user = request.user
    if ad.user != user:
        user = False
    return render(request, "ads/current_ad.html", context={"ad": ad,
                                                           "user": user})

def get_my_ads(request):
    user = request.user.id
    ads = Ad.objects.filter(user=user)
    return render(request, "ads/all_ads.html", context={"ads": ads})


@login_required
def create_ad(request):
    if request.method == "POST":
        form = AdCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd["user"] = request.user
            # print(cd)
            Ad.objects.create(**cd)
            return HttpResponseRedirect(reverse("all_ads"))

    else:
        form = AdCreateForm()

    return render(request, "ads/create_ads.html", context={"form": form})


@login_required
def update_ad(request, id):
    ad = get_object_or_404(Ad, pk=id)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не можете редактировать это объявление")

    if request.method == "POST":
        form = AdUpdateForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("my_ads"))
    else:
        form = AdUpdateForm(instance=ad)

    return render(request, "ads/update_ad.html", {"form": form, "ad": ad})


@login_required
def delete_ad(request, id):
    ad = get_object_or_404(Ad, pk=id)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не можете удалить это объявление")

    ad.delete()
    return HttpResponseRedirect(reverse("my_ads"))


def search(request):
    query = request.GET.get("q")
    ads =  q_search(query)
    return render(request, "ads/all_ads.html", context={"ads": ads})