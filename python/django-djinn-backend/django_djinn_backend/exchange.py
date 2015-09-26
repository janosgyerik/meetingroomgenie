from datetime import datetime
import json
from subprocess import Popen, PIPE

from django_djinn_backend import settings


def ready():
    return settings.EXCHANGE_CONNECTOR_READY


def format_date_param(date):
    return date.strftime('%Y%m%d%H%M')


def parse_date(datestr):
    return datetime.strptime(datestr, '%Y-%m-%d %H:%M')


def parse_reservations(jsonstr):
    reservations = {}
    for roomname, values in json.loads(jsonstr).items():
        reservations[roomname] = values

    return reservations


def list_reservations(start, end, *roomnames):
    """
    Get the list of reservations for specified room names.

    :param start: start datetime to search
    :param end: end datetime to search
    :param roomnames: list of room names
    :return: reservations as a dictionary of roomname -> reservations
    """
    reservations = {}

    if not ready() or not roomnames:
        return reservations

    startstr = format_date_param(start)
    endstr = format_date_param(end)

    returncode, out, err = run_cmd(
        'java', '-cp', settings.EXCHANGE_CONNECTOR_JAR, settings.EXCHANGE_LIST_CMD, startstr, endstr, *roomnames)

    if returncode != 0:
        return reservations

    return parse_reservations(out)


def create_reservation(start, end, room):
    if not ready():
        return


def cancel_reservation(start, end, room):
    if not ready():
        return


def run_cmd(*args):
    pipes = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = pipes.communicate()

    return pipes.returncode, out.decode().strip(), err.decode().strip()

