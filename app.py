import json
import re
from copy import copy

from flask import Flask
from flask import request

from db_lib import get_db, query_db


def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    return app


app = create_app()


def prepare_sql_query_log(date_from, date_to, page_number, item_size):
    log_query = "SELECT * FROM logs"

    if date_from and not date_to:
        log_query = f"{log_query} WHERE dt >= {date_from} "
    elif date_to and not date_from:
        log_query = f"{log_query} WHERE dt <= {date_to} "
    elif date_from and date_to:
        log_query = f"{log_query} WHERE dt >= {date_from} and dt <= {date_to} "

    log_query = f"{log_query} LIMIT {item_size} OFFSET {item_size * page_number}"

    return log_query


def extract_ids_from_logs(log_list: list):
    user_ids = set()
    pattern = r"<p=(?P<user_id>\d*)>"
    for item in log_list:
        event = item[1]
        finded_ids = re.findall(pattern, event)
        if finded_ids:
            user_ids = user_ids | set(finded_ids)

    return user_ids


def enrich_logs(log_list: list, user_list: list):
    result = []

    log_list = [list(copy(l)) for l in log_list]
    for user in user_list:
        full_name = f"{user[1]} {user[2]}"
        slug = f"<p={user[0]}>"
        for idx, val in enumerate(log_list):
            if slug in log_list[idx][1]:
                log_list[idx][1] = log_list[idx][1].replace(slug, full_name)

    for log in log_list:
        result.append({'date': log[0], 'event': log[1]})

    return result


@app.route("/logs")
def logs():
    date_from = float(request.args.get('from', 0))
    date_to = float(request.args.get('to', 0))
    page_number = int(request.args.get('page', 0))
    item_size = int(request.args.get('items', 10))

    path_to_logs = './db/logs.db'
    cur = get_db(path_to_logs).cursor()
    log_list = query_db(cur, prepare_sql_query_log(date_from, date_to, page_number, item_size))

    user_query = f"SELECT * FROM people WHERE id in ({','.join(extract_ids_from_logs(log_list))})"
    path_to_people = './db/people.db'
    cur = get_db(path_to_people).cursor()
    user_list = query_db(cur, user_query)

    result = enrich_logs(log_list, user_list)
    return json.dumps(result, indent=4, sort_keys=True)


if __name__ == '__main__':
    app.run()
