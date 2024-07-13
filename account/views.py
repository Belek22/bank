from django.shortcuts import render
from account.models import User

def banker_status(request, banker_id):
    banker = User.objects.get(pk=banker_id)
    context = {
        'banker': banker,
        'booking_status': banker.get_booking_status()
    }
    return render(request, 'banker_status.html', context)
