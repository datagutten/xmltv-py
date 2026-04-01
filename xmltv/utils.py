import datetime
from typing import List

from .program import Program


def merge_days(date: datetime.datetime, *days: List[Program]) -> List[Program]:
    """
    Combine XMLTV files for multiple days to get a complete listing for the given day
    :param date: Date
    :param days: Lists of Program objects, first day first
    :return: List of Program objects
    """
    day_start = datetime.datetime.combine(date, datetime.time(tzinfo=date.tzinfo))
    day_end = datetime.datetime.combine(date, datetime.time(23, 59, 59, tzinfo=date.tzinfo))

    programs_out = []
    for day in days:
        for program in day:
            if program.start < day_start:
                continue
            if program.start > day_end:
                break
            programs_out.append(program)
    return programs_out
