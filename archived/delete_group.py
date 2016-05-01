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
             
if len(sys.argv) != 3:
    sys.exit("Usage: delete_group.py <personGroupId> <key>")

personGroupId = sys.argv[1]
key = sys.argv[2]

headers = {
'Ocp-Apim-Subscription-Key': key
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
