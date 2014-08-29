Logstash Index Cleaner
=======================


Clean your old logstash elasticsearch indices.

Project uses vpython for virtualenv management.
See [https://github.com/tbug/vpython][vpython].

You can execute `python logstash_clean.py` if you don't want to use [vpython][vpython].

Dependencies are listed in `requirements.txt` file.
Install with `vpip install -r requirements.txt` or
`pip install -r requirements` if you don't want to use vpython. (you might need to prepend `sudo` to pip depending on your setup).




```
$> ./logstash_clean.py --help

Usage:
    logstash_clean.py [--host <host>] [--port <port>] [--format <format>] [--max-days-old <days>]

Options:
    -h, --host <host>          Elasticsearch host [default: 127.0.0.1]
    -p, --port <port>          Elasticsearch port [default: 9200]
    -f, --format <format>      Logstash index format [default: logstash-%Y.%m.%d]
    -d, --max-days-old <days>  Indices older than given days will be deleted [default: 30]
    --force <flag>             Don't ask for confirmation before deleting [default: false]


$>
```

[vpython]: https://github.com/tbug/vpython  "tbug/vpython"
