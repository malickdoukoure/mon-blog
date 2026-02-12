from .models import Category


def categories(request):
    try:
        return {'categories': Category.objects.all()}
    except Exception:
        return {'categories': []}
