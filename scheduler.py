"""Schedules the tasks to run"""
import croniter
import asyncio
from asyncio import ensure_future
from datetime import datetime
from functools import wraps
from math import ceil
from traceback import format_exception
from typing import Any, Callable, Coroutine, Union
from starlette.concurrency import run_in_threadpool

NoArgsNoReturnFuncT = Callable[[], None]
NoArgsNoReturnAsyncFuncT = Callable[[], Coroutine[Any, Any, None]]
NoArgsNoReturnDecorator = Callable[
    [Union[NoArgsNoReturnFuncT, NoArgsNoReturnAsyncFuncT]], NoArgsNoReturnAsyncFuncT
]
def cron_exc(**kwargs):

    every = "*/"if kwargs.get("interval") else '' 
    if kwargs.get('cron_expression'):
        return kwargs.get('cron_expression')
    cron_list = []
    for i in ['minutes','hour','date','week','day'] :
        cron_list.append(f"{every}{kwargs.get(i)}" if isinstance(kwargs.get(i) , int) else '*')
    if kwargs.get("seconds"):
        cron_list.append(f"{every}{kwargs.get('seconds')}" if isinstance(kwargs.get('seconds') , int) else '*')
    return ' '.join( cron_list)

def scheduler_cron(**kwargs):
    """Schedules a job based on cron expression"""
    logger = kwargs.get('logger',None)
    raise_exceptions = kwargs.get('raise_exceptions',True)
    cron_expression = cron_exc(**kwargs)
    print(cron_expression)
    def decorator(
        func: Union[NoArgsNoReturnAsyncFuncT, NoArgsNoReturnFuncT]
    ) -> NoArgsNoReturnAsyncFuncT:
        """
        Converts the decorated function into a repeated, periodically-called version of itself.
        """
        is_coroutine = asyncio.iscoroutinefunction(func)

        @wraps(func)
        async def wrapped() -> None:
            async def loop() -> None:
                curr_loop = asyncio.get_running_loop()
                if cron_expression:
                    cron = croniter.croniter(cron_expression, datetime.now())
                    interval = cron.get_next(datetime)
                print(interval - datetime.now().replace(microsecond=0))
                while True:
                    try:
                        if (
                            ceil(
                                (
                                    interval - datetime.now().replace(microsecond=0)
                                ).total_seconds()
                            )
                            == 0
                        ):
                            interval = cron.get_next(datetime)
                            print(interval - datetime.now().replace(microsecond=0))
                            print(f"Executing function: {func._name_}")
                            if is_coroutine:
                                curr_loop.create_task(func())
                            else:
                                curr_loop.create_task(run_in_threadpool(func))
                            print("Executing in background..")
                        print("Sleeping now...")
                        await asyncio.sleep((interval - datetime.now()).total_seconds())
                    except Exception as exc:
                        if logger is not None:
                            formatted_exception = "".join(
                                format_exception(type(exc), exc, exc._traceback_)
                            )
                            logger.error(formatted_exception)
                        if raise_exceptions:
                            raise exc
            ensure_future(loop())
        return wrapped
    return decorator
