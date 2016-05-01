import http.client, urllib.request, urllib.parse, urllib.error, base64, sys, json, pprint, collections

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

def get_people_in_group(personGroupId):
    headers = {
        'Ocp-Apim-Subscription-Key': 'f5d9612fa9744f83b8acea571d232ad9'
    }

    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("GET", "/face/v1.0/persongroups/" +  personGroupId + "/persons?", "{}", headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        conn.close()
        return json.loads(data)
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def personId_from_name(name, personGroupId):
    personId = ""
    parsed_data = get_people_in_group(personGroupId)
    for person_record in parsed_data:
        if person_record['name'] == name:
            personId = person_record['personId']

    if not personId:
        sys.exit("Person '" + name + "' was not found. Use create to create a new person")
    return personId


if len(sys.argv) < 2 or (sys.argv[1] != 'create' and sys.argv[1] != 'list' and sys.argv[1] != 'get' and sys.argv[1] != 'add_face' and sys.argv[1] != 'delete' and sys.argv[1] != 'patch'):
    sys.exit("Usage: person.py <command> (create, get, list, add_face, delete, patch)")

if sys.argv[1] == 'create':
    if len(sys.argv) != 4:
        sys.exit("Usage: person.py create <personGroupId> <personName>")

    personGroupId = sys.argv[2]
    name = sys.argv[3]

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'f5d9612fa9744f83b8acea571d232ad9'
    }

    body = '{name: "' + name + '", userData: "someData"}'

    parsed_data = get_people_in_group(personGroupId)
    for person_record in parsed_data:
        if person_record['name'] == name:
            sys.exit("Error: Person '" + name + "' already exists in the database")

    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/persongroups/" +  personGroupId + "/persons", body, headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        if response.status == 200:
            data = json.loads(data)
            print(str(response.status) + " Success! Created " + name + " with id " + data['personId'])
        else:
            pretty(json.loads(data))
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

if sys.argv[1] == 'list':
    if len(sys.argv) != 3:
        sys.exit("Usage: person.py list <personGroupId>")

    personGroupId = sys.argv[2]
    pretty(get_people_in_group(personGroupId))

if sys.argv[1] == 'get':
    if len(sys.argv) != 4:
        sys.exit("Usage: person.py get <personGroupId> <personName>")

    personGroupId = sys.argv[2]
    personName = sys.argv[3]
    personId = personId_from_name(personName, personGroupId)

    headers = {
        'Ocp-Apim-Subscription-Key': 'f5d9612fa9744f83b8acea571d232ad9'
    }

    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("GET", "/face/v1.0/persongroups/" +  personGroupId + "/persons/" + personId, "{}", headers)
        response = conn.getresponse()
        print(response.status)
        data = response.read().decode('utf-8')
        pretty(json.loads(data))
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

if sys.argv[1] == 'add_face':
    if len(sys.argv) != 5:
        sys.exit("Usage: person.py add_face <personGroupId> <personName> <url>")

    personGroupId = sys.argv[2]
    personName = sys.argv[3]
    url = sys.argv[4]

    headers = {
        'Ocp-Apim-Subscription-Key': 'f5d9612fa9744f83b8acea571d232ad9'
    }
    
    personId = personId_from_name(personName, personGroupId)

    body = '{"url":"' + url + '"}'

    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/persongroups/" +  personGroupId + "/persons/" + personId + "/persistedFaces", body, headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        if response.status == 200:
            data = json.loads(data)
            print(str(response.status) + " Success! Added faceId " + data['persistedFaceId'] + " to " + personName + " in " + personGroupId)
        else:
            pretty(json.loads(data))
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


if sys.argv[1] == 'delete':
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        sys.exit("Usage: person.py delete <personGroupId> <personName> [faceId]")
    
    personGroupId = sys.argv[2]
    personName = sys.argv[3]
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'f5d9612fa9744f83b8acea571d232ad9'
    }

    personId = personId_from_name(personName, personGroupId)

    if len(sys.argv) == 4:
        try:
            conn = http.client.HTTPSConnection('api.projectoxford.ai')
            conn.request("DELETE", "/face/v1.0/persongroups/" +  personGroupId + "/persons/" + personId, "{}", headers)
            response = conn.getresponse()
            data = response.read().decode('utf-8')
            if response.status == 200:
                print(str(response.status) + " Success! Deleted " + personName + " (" + personId + ") from " +personGroupId)
            else:
                pretty(json.loads(data))
    
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
    else:
        faceId = sys.argv[4]
        try:
            conn = http.client.HTTPSConnection('api.projectoxford.ai')
            conn.request("DELETE", "/face/v1.0/persongroups/" +  personGroupId + "/persons/" + personId + "persistedFaces/" + faceId, "{}", headers)
            response = conn.getresponse()
            data = response.read().decode('utf-8')
            if response.status == 200:
                print(str(response.status) + " Success! Deleted " + faceId + " from " +personName + " in group " + personGroupId)
            else:
                pretty(json.loads(data))
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))


if sys.argv[1] == 'patch':
    if len(sys.argv) != 5:
        sys.exit("Usage: person.py patch <personGroupId> <personName> <new_name>")

    personGroupId = sys.argv[2]
    name = sys.argv[3]
    new_name = sys.argv[4]

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'f5d9612fa9744f83b8acea571d232ad9'
    }

    body = '{name: "' + new_name + '", userData: "someData"}'

    personId = personId_from_name(name, personGroupId)

    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("PATCH", "/face/v1.0/persongroups/" +  personGroupId + "/persons/" + personId, body, headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        if response.status == 200:
            print(str(response.status) + " Success! Changed " + name + " to " + new_name)
        else:
            pretty(json.loads(data))
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

