from django.shortcuts import render
from .models import ChaiVarity, Store, StoreReview
from django.shortcuts import get_object_or_404




# Create your views here.
def all_chai(request):
    chais = ChaiVarity.objects.all()
    return render(request, 'chai/all_chai.html', {'chais': chais})

def chai_detail(request, chai_id):
    chai = get_object_or_404(ChaiVarity, pk=chai_id)
    return render(request, 'chai/chai_detail.html', {'chai': chai})

def store_detail(request):
    stores = Store.objects.all()
    return render(request, 'chai/store_detail.html', {'stores': stores})


def store_reviews(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    return render(request, 'chai/store_reviews.html', {'store': store})

