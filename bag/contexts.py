from .models import Bag

def bag_contents(request):
    """
    Context processor that returns the current user's shopping bag
    and its contents to every template.
    """
    bag = Bag.objects.filter(user=request.user) 
    return {'bag': bag}
