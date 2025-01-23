from .end_list_resource import EndList
from .first_page_resource import First
from .hint_resource import Hint
from .list_name_resource import ListName
from .create_list_resource import CreateList
from .created_list_resource import CreatedList
from .question_resource import Question
from .select_list_resource import SelectList
from .list_name_select_resource import NameSelectList
from .ready_resource import Ready
from .plug import Plug

print('init texts')
first = First()
list_name_res = ListName()
create_list = CreateList()
plug = Plug()
created_list = CreatedList()
name_select = NameSelectList()
select_list = SelectList()
ready = Ready()
question = Question()
hint = Hint()
end_list = EndList()

sources = [
    first,          # INIT
    first,          # START
    list_name_res,  # REQUEST_NAME
    create_list,    # CREATE_LIST
    select_list,    # SELECT_LIST
    ready,          # IS_READY
    question,       # QUESTION
    end_list,       # END_LIST
    created_list,   # CREATED_LIST
    name_select,    # NAME_SELECT
    hint            # HINT
]
