import json
import re
from copy import copy

from flask import Flask
from flask import request

from db_lib import get_db, query_db

app = Flask(__name__)


@app.route("/logs")
def logs():

    # pdb.set_trace()
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    page_number = int(request.args.get('page', 0))
    item_size = int(request.args.get('items', 10))

    path_to_logs = './db/logs.db'
    cur = get_db(path_to_logs).cursor()

    log_query = f"SELECT * FROM logs " \
                f"WHERE dt >= {date_from} and dt <= {date_to} " \
                f"LIMIT {item_size} " \
                f"OFFSET {item_size * page_number}"
    log_list = query_db(cur, log_query)

    user_ids = set()
    pattern = r"<p=(?P<user_id>\d*)>"
    for item in log_list:
        event = item[1]
        finded_ids = re.findall(pattern, event)
        if finded_ids:
            user_ids = user_ids | set(finded_ids)

    user_query = f"SELECT * FROM people WHERE id in ({','.join(user_ids)})"
    path_to_people = './db/people.db'
    cur = get_db(path_to_people).cursor()
    user_list = query_db(cur, user_query)

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

    return json.dumps(result)


if __name__ == '__main__':
    app.run()
