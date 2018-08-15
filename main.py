"""For GCP Usage"""

from controller import handle_request

def webhook(request):
    return handle_request(request)
    
