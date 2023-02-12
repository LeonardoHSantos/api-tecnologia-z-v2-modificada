from dateutil import tz
from datetime import datetime, timedelta


def datetime_now(tzone):
    return datetime.now(tz=tz.gettz(tzone))

def convert_to_timestamp(datetime):
    return int(datetime.timestamp())

def timestemp_converter_to_local(timestamp, local_tz, local):
    timestamp_convert = datetime.strptime(datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    timestamp_convert = timestamp_convert.replace(tzinfo=tz.gettz(local_tz))
    return str(timestamp_convert.astimezone(tz.gettz(local)))[:-6]

def expiration_operation_M5():
    dt = datetime_now(tzone="America/Sao Paulo")
    minute = dt.minute
    expiration = None

    if   minute >= 0 and minute < 5:
        expiration = dt.replace(microsecond=0, second=0, minute=10)
    elif minute >= 5 and minute < 10:
        expiration = dt.replace(microsecond=0, second=0, minute=15)
    elif minute >= 10 and minute < 15:
        expiration = dt.replace(microsecond=0, second=0, minute=20)
    elif minute >= 15 and minute < 20:
        expiration = dt.replace(microsecond=0, second=0, minute=25)
    elif minute >= 20 and minute < 25:
        expiration = dt.replace(microsecond=0, second=0, minute=30)
    elif minute >= 25 and minute < 30:
        expiration = dt.replace(microsecond=0, second=0, minute=35)
    elif minute >= 30 and minute < 35:
        expiration = dt.replace(microsecond=0, second=0, minute=40)
    elif minute >= 35 and minute < 40:
        expiration = dt.replace(microsecond=0, second=0, minute=45)
    elif minute >= 40 and minute < 45:
        expiration = dt.replace(microsecond=0, second=0, minute=50)
    elif minute >= 45 and minute < 50:
        expiration = dt.replace(microsecond=0, second=0, minute=55)
    elif minute >= 50 and minute < 55:
        dt = dt + timedelta(hours=+1)
        expiration = dt.replace(microsecond=0, second=0, minute=0)
    elif minute >= 55:
        dt = dt + timedelta(hours=+1)
        expiration = dt.replace(microsecond=0, second=0,  minute=5)
    return {
        "expiration": expiration,
        "expiration_timestamp": int(expiration.timestamp())
        }

def check_expiration_operation_M5():
    dt = datetime_now(tzone="America/Sao Paulo")
    minute = dt.minute
    expiration = None

    if minute == 5:
        expiration = dt.replace(microsecond=0, second=0, minute=5)
    elif minute == 20:
        expiration = dt.replace(microsecond=0, second=0, minute=20)
    elif minute == 35:
        expiration = dt.replace(microsecond=0, second=0, minute=35)
    elif minute == 50:
        expiration = dt.replace(microsecond=0, second=0, minute=50)

    return {
        "expiration": expiration,
        "expiration_timestamp": expiration.timestamp()
        }


