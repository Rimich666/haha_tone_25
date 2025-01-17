from .a_first_page import First
from .b_list_name import ListName
from .create_list import CreateList
from .created_list import CreatedList
from .plug import Plug

print('init texts')
first = First()
list_name_res = ListName()
create_list = CreateList()
plug = Plug()
created_list = CreatedList()

sources = [
    first,          # INIT
    first,          # START
    list_name_res,  # REQUEST_NAME
    create_list,    # CREATE_LIST
    plug,           # SELECT_LIST
    plug,           # IS_LOADED
    plug,           # QUESTION
    plug,           # END_LIST
    created_list    # CREATED_LIST
]
