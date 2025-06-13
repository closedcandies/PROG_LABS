import sys
import functools
import json
import sqlite3
from datetime import datetime

def trace(func=None, *, handle=sys.stdout):
    if func is None:
        return lambda f: trace(f, handle=handle)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        func_name = func.__name__
        params = list(map(str, args)) + [f"{k}={v}" for k, v in kwargs.items()]
        log_entry = {
            "datetime": timestamp,
            "func_name": func_name,
            "params": params,
            "result": str(result)
        }

        if handle in (sys.stdout, sys.stderr):
            print(f"[{timestamp}] {func_name}({params}) → {result}", file=handle)

        elif isinstance(handle, str) and handle.endswith('.json'):
            try:
                with open(handle, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []

            data.append(log_entry)
            with open(handle, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

        elif isinstance(handle, sqlite3.Connection):
            con = handle
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS logtable (
                datetime TEXT,
                func_name TEXT,
                params TEXT,
                result TEXT
            )""")
            cur.execute("INSERT INTO logtable VALUES (?, ?, ?, ?)", (
                timestamp,
                func_name,
                json.dumps(params),
                str(result)
            ))
            con.commit()

        else:
            raise ValueError("Unsupported handle type")

        return result

    return wrapper


def showlogs(con: sqlite3.Connection):
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM logtable")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print("Ошибка при выводе логов:", e)


deco = trace
