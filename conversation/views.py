from T2S_Backend.decorators import *
from T2S_Backend.globals import *
from T2S_Backend.utils import *


@ get_required
@ login_required
def get_message(request):
    # TODO
    pass


@ get_required
@ login_required
def get_new_messages(request):
    # TODO
    pass


@ get_required
@ login_required
def get_all_messages(request):
    # TODO
    pass


@ get_required
@ login_required
def get_message_detail(request):
    # TODO
    pass


@ post_required
@ login_required
def send_message(request):
    # TODO
    pass
