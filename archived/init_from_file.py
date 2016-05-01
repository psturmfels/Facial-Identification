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

if len(sys.argv) != 4:
    sys.exit("Usage: init_from_file.py <personGroupId> <training_file> <key>")

personGroupId = sys.argv[1]
filename = sys.argv[2]
key = sys.argv[3]
training_set = json.load(open(filename))

headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'f5d9612fa9744f83b8acea571d232ad9'
}

body = '{name: "' + personGroupId + '", userData: "someData"}'

try:
    conn = http.client.HTTPSConnection('api.projectoxford.ai')
    conn.request("PUT", "/face/v1.0/persongroups/" +  personGroupId, body, headers)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    print(response.status)
    if response.status == 200:
        print("Created group " + personGroupId)
    else:
        pretty(json.loads(data))
        sys.exit()
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

for person in training_set:
    name = person['name']
    userData = person['userData']
    body = '{name: "' + name + '", userData: "someData"}'
    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/persongroups/" +  personGroupId + "/persons", body, headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        personId = ""
        if response.status == 200:
            data = json.loads(data)
            print("  Created " + name + " with id " + data['personId'])
            personId = data['personId']
        else:
            pretty(json.loads(data))
            sys.exit()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    faces = person['faces']
    for url in faces:
        body = '{"url":"' + url + '"}'
        try:
            conn = http.client.HTTPSConnection('api.projectoxford.ai')
            conn.request("POST", "/face/v1.0/persongroups/" +  personGroupId + "/persons/" + personId + "/persistedFaces", body, headers)
            response = conn.getresponse()
            data = response.read().decode('utf-8')
            if response.status == 200:
                data = json.loads(data)
                print("     Added faceId " + data['persistedFaceId'] + " to " + name)
            else:
                pretty(json.loads(data))
                sys.exit()
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

try:
    conn = http.client.HTTPSConnection('api.projectoxford.ai')
    conn.request("POST", "/face/v1.0/persongroups/" +  personGroupId + "/train", "{}", headers)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    print(response.status)
    if response.status == 202:
        print("Began training group " + personGroupId)
    else:
        pretty(json.loads(data))
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
