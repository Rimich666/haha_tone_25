import inspect
import time
import grpc
from ydb import BadSession


TIMEOUT_SECONDS = 0.002


def exception(attempt=5, ret_count=1):
    def exception_inner(func):
        def wrapper(*args, **kwargs):
            need_exec = True
            result = tuple([None for _ in range(ret_count)])
            exec_count = 0
            while need_exec:
                exec_count += 1
                try:
                    result = func(*args, **kwargs)
                    need_exec = False
                    if exec_count > 1:
                        print('\033[34m', 'Всё таки помогает:', exec_count, '\033[0m')
                except (grpc.RpcError, BadSession) as e:
                    if e.code() == grpc.StatusCode.RESOURCE_EXHAUSTED:
                        if exec_count > attempt:
                            print('\033[35m', 'И снова грёбаный Экибастуз.', exec_count)
                            print('\033[33m', inspect.currentframe().f_back.f_code.co_name)
                            print(f'{func.__name__}', '\033[0m')
                        time.sleep(TIMEOUT_SECONDS)
                    else:
                        print('\033[36m', 'Необработанная ошибка', e)
                if exec_count > attempt:
                    break
            return result
        return wrapper
    return exception_inner
