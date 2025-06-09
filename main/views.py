from django.shortcuts import render
from straw_catalog.models import Dish
from django.db.models import Q
from reviews.models import Review
def home(request):
    query = request.GET.get('q', '')

    popular_dishes = Dish.objects.order_by('-rating')[:4]
    new_dishes = Dish.objects.order_by('-created_at')[:4]

    if query:
        search_results = Dish.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        search_results = None

    return render(request, 'main/home.html', {
        'popular_dishes': popular_dishes,
        'new_dishes': new_dishes,
        'search_results': search_results,
        'query': query
    })

