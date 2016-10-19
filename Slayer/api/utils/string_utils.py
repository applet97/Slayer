import re

from django.conf import settings


def empty_to_none(s):
    """
    :param s: String to be converted.
    :return: If string is empty returns None; otherwise returns string itself.
    """
    if s is not None:
        if len(s) == 0:
            return None
    return s


def zero_if_none(s, default=settings.TIMESTAMP_BIG):
    """
    :param s: String to be converted to int.
    :return: If string is empty or None returns 0; otherwise returns integer format.
    """
    s = empty_to_none(s)
    if s is None:
        return default
    return int(s)


def integer_list(arr):
    """
    :param arr: Array of strings to be converted to array of ints.
    :return: array of ints
    """
    result = list()
    for x in arr:
        if len(x) > 0:
            result.append(int(x))
    return result


def fromCamelCase_to_upper_score(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def empty_if_none(s):
    if s is None:
        return ""
    return s
    
