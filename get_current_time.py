import datetime


def get_time() -> str:
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
