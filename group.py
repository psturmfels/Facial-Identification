import http.client, urllib.request, urllib.parse, urllib.error, base64, sys, json, collections
def pretty(d, indent=0):
    if isinstance(d, dict):
        for key, value in d.items():
            if isinstance(value, dict):
                print('\t' * (indent) + key + ": ")
                print('\t' * (indent) + '{')
                pretty(value, indent + 1)
                print('\t' * (indent) + '}')
            else:
                print('\t' * (indent) + key + ": " + str(value))
    else:
        for record in d:
          if isinstance(record, collections.Iterable):
             print('\t' * (indent) + '{')
             pretty(record, indent + 1)
             print('\t' * (indent) + '}')
          else:
             print('\t' * (indent) + str(record))

if len(sys.argv) < 2 or (sys.argv[1] != 'create' and sys.argv[1] != 'get' and sys.argv[1] != 'delete' and sys.argv[1] != 'list' and sys.argv[1] != 'patch' and sys.argv[1] != 'train'):
    sys.exit("Usage: group.py <command> (create, get, delete, list, patch, train)")

if sys.argv[1] == 'create':
    if len(sys.argv) != 4:
        sys.exit("Usage: group.py create <personGroupId> <Display name>")

    personGroupId = sys.argv[2]
    name = sys.argv[3]

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'f5d9612fa9744f83b8acea571d232ad9'
    }

    body = '{name: "' + name + '", userData: "someData"}'

    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("PUT", "/face/v1.0/persongroups/" +  personGroupId, body, headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        print(response.status)
        if response.status == 200:
            print("Success! Created group " + personGroupId + " with name " + name)
        else:
            pretty(json.loads(data))
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

if sys.argv[1] == 'delete':
    if len(sys.argv) != 3:
        sys.exit("Usage: group.py delete <personGroupId>")

    personGroupId = sys.argv[2]

    headers = {
    'Ocp-Apim-Subscription-Key': 'f5d9612fa9744f83b8acea571d232ad9'
    }

    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("DELETE", "/face/v1.0/persongroups/" +  personGroupId, "{}", headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        print(response.status)
        if response.status == 200:
            print("Success! Deleted group " + personGroupId)
        else:
            pretty(json.loads(data))
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

if sys.argv[1] == 'get':
    if len(sys.argv) != 3 and (len(sys.argv) != 4 or sys.argv[3] != 't'):
        sys.exit("Usage: group.py get <personGroupId> [t]")

    personGroupId = sys.argv[2]

    headers = {
        'Ocp-Apim-Subscription-Key': 'f5d9612fa9744f83b8acea571d232ad9'
    }

    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        if len(sys.argv) == 3:
            conn.request("GET", "/face/v1.0/persongroups/" +  personGroupId, "{}", headers)
        else:
            conn.request("GET", "/face/v1.0/persongroups/" +  personGroupId + "/training", "{}", headers)
        response = conn.getresponse()
        print(response.status)
        data = response.read().decode('utf-8')
        pretty(json.loads(data))
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

if sys.argv[1] == 'list':
    if len(sys.argv) != 2:
        sys.exit("Usage: group.py list")

    headers = {
        'Ocp-Apim-Subscription-Key': 'f5d9612fa9744f83b8acea571d232ad9'
    }

    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("GET", "/face/v1.0/persongroups/", "{}", headers)
        response = conn.getresponse()
        print(response.status)
        data = response.read().decode('utf-8')
        pretty(json.loads(data))
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

if sys.argv[1] == 'patch':
    if len(sys.argv) != 5:
        sys.exit("Usage: group.py delete <personGroupId> <displayName> <userData>")

    personGroupId = sys.argv[2]
    displayName = sys.argv[3]
    userData = sys.argv[4]
    body = '{ name: "' + displayName + '", userData: "' + userData + '" }'

    headers = {
    'Ocp-Apim-Subscription-Key': 'f5d9612fa9744f83b8acea571d232ad9'
    }

    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("PATCH", "/face/v1.0/persongroups/" +  personGroupId, body, headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        print(response.status)
        if response.status == 200:
            print("Success! Patched group " + personGroupId + " with name " + displayName + " and userData " + userData)
        else:
            print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

if sys.argv[1] == 'train':
    if len(sys.argv) != 3:
        sys.exit("Usage: group.py train <personGroupId>")

    personGroupId = sys.argv[2]

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'f5d9612fa9744f83b8acea571d232ad9'
    }

    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/persongroups/" +  personGroupId + "/train", "{}", headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        print(response.status)
        if response.status == 202:
            print("Success! Began training group " + personGroupId)
        else:
            pretty(json.loads(data))
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
