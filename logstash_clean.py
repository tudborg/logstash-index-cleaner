#!/usr/bin/env vpython
'''
Remove indexes older than a given number of days (default is 30)

Usage:
    logstash_clean.py [--host <host>] [--port <port>] [--format <format>] [--max-days-old <days>]

Options:
    -h, --host <host>          Elasticsearch host [default: 127.0.0.1]
    -p, --port <port>          Elasticsearch port [default: 9200]
    -f, --format <format>      Logstash index format [default: logstash-%Y.%m.%d]
    -d, --max-days-old <days>  Indices older than given days will be deleted [default: 30]
    --force <flag>             Don't ask for confirmation before deleting [default: false]
'''

from docopt import docopt
import requests
import datetime
import sys

def get_logstash_indices(index_list, match_format):
    """return list of tuple (date, raw_index_name)"""
    logstash_indices = []
    for index_name in index_list:
        try:
            match = datetime.datetime.strptime(index_name, match_format).date()
        except ValueError as e:
            print("Skipping {}".format(index_name))
            continue
        else:
            logstash_indices.append((match, index_name))
    return logstash_indices

def split_by_date(index_tuple_list, keep_if_newer_than_days):
    """return tuple with two lists, (to_delete, to_keep)"""
    # Detect what indices to delete
    deletion_date = datetime.date.today() - datetime.timedelta(days=keep_if_newer_than_days)
    deleting = []
    keeping = []
    for index in index_tuple_list:
        if index[0] <= deletion_date:
            deleting.append(index)
        else:
            keeping.append(index)
    return (deleting, keeping)

def get_alias_list(host, port):
    # Base host
    base = "http://{}:{}".format(host, port)
    # Get list of indices
    r = requests.get(base+"/_aliases")
    r.raise_for_status()
    return r.json()

def delete_indices(index_tuple_list, host, port):
    base = "http://{}:{}".format(host, port)
    name_list = sorted([i[1] for i in index_tuple_list])

    for name in name_list:
        addr = base+"/"+name
        print("DELETE "+addr+":", end=' ')
        r = requests.delete(addr)
        if r.status_code == 200:
            print ("OK")
        else:
            print ("Failed")

def main(args):
    host  = args.get("--host")
    port  = args.get("--port")
    fmt   = args.get("--format")
    days  = int(args.get("--max-days-old"))
    force = bool(args.get('--force'))

    assert(days > 0)  # Sanity check


    # Detech logstash indices
    indices = get_logstash_indices(
        map(lambda kv: kv[0], get_alias_list(host, port).items()),
        fmt)
    (deleting, keeping) = split_by_date(indices, days)

    if len(deleting) < 1:
        print("No indices to delete")
        return 0
    else:
        # Ask user
        print("keeping {}, deleting {}".format( len(keeping), len(deleting) ))
        print("Indices to delete:\n  - {}".format( "\n  - ".join(map(lambda i: i[1], deleting)) ))


        if not force:
            #ask for confirmation or abort
            answer = ""
            while answer not in ("y", "n"):
                answer = input("Delete {} indices? [y/n]: ".format(len(deleting))).lower()
            if answer == "n":
                return 2
            else:
                if delete_indices(deleting, host, port):
                    return 0
                else:
                    return 1


if __name__ == "__main__":
    args = docopt(__doc__)
    sys.exit(main(args))

