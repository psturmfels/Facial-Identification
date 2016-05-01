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

def get_people_in_group(personGroupId, key):
    headers = {
        'Ocp-Apim-Subscription-Key': key
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

def name_from_id(personId, personGroupId):
    name = ""
    parsed_data = get_people_in_group(personGroupId, key)
    for person_record in parsed_data:
        if person_record['personId'] == personId:
            name = person_record['name']

    if not personId:
        sys.exit("ID '" + personId + "' was not found!")
    return name


if len(sys.argv) != 4:
    sys.exit("Usage: identify.py <personGroupId> <identification_file> <key>")

personGroupId = sys.argv[1]
filename = sys.argv[2]
key = sys.argv[3]
identification_set = json.load(open(filename))
current_url = 1
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': key
}


for url in identification_set:
    print("Identifying photos in " + url)
    personName = ""
    personId = ""
    faceIds = []
    faceRectangles = []
    body = '{url:"' + url + '"}'

    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/detect/?returnFaceId=true", body, headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        if (response.status != 200):
            print(response.status)
            pretty(json.loads(data))
        data = json.loads(data)
        for item in data:
            faceIds.append(item['faceId'])
            faceRectangles.append(item['faceRectangle'])
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    body = '{faceIds: ' + str(faceIds) + ', personGroupId: "' + personGroupId + '", maxNumOfCandidatesReturned: 3}'

    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/identify/", body, headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        print(response.status)
        data = json.loads(data)

        index = 0
        for result in data:
            faceId = result['faceId']
            if(faceId != faceIds[index]):
                sys.exit(faceId + " != " + faceIds[index])
            print("\n  Face ID: " + faceId)
            pretty(faceRectangles[index], indent=1)
            index = index + 1
            print("  Results for " + faceId + " in order of confidence:")
            for candidate in result['candidates']:
                personId = candidate['personId']
                confidence = candidate['confidence']
                personName = name_from_id(personId, personGroupId)
                print("    This is " + personName + " (" + personId + ") with confidence " + str(confidence))

        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
