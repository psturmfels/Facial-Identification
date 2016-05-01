# Facial-Identification
A convenience wrapper for the Microsoft Cognitive Services API.

Usage: 
```python
import iden
```
This library provides a convient three-function flow to: 
    Set up a group of people with training face data
    Input an arbitrary photo and identify if that photo belongs to someone in the group – and if so, to which member within the group

Step 1: Initialize a training set from a json file

```python
iden.init_from_file(personGroupId, training_file, key)
```
    
The above function initializes a training data set from a json file. 
    
personGroupId: A unique ID to reference a group of people (training set) by. Valid characters include numbers, english letters in lower case, '-' and '_'. The maximum length of personGroupId is 64.
    
training_file: a json file containing an array of person objects. Each person object has three fields:
    name: The name of the person.
    userData: User-specified data for any purpose. The maximum length is 1KB.
    faces: An array of urls; each url should be a frontal photo of the person in question. No other faces should appear in the photo. Valid image size is from 1KB to 4MB. See the provided file for more/ 
    
key: A valid Microsoft Cognitive Services subscription key authenticated for the face API. See https://www.microsoft.com/cognitive-services/en-US/subscriptions to acquire a key.

 
Step 2: Identify identities of arbitrary photos matched against a group

```python
iden.identify(personGroupId, identification_file, key):
```
    
The above function accepts a set of photos and assigns confidence parameters to each photo for the people in the group that the photo most likely represents.
    
    personGroupId: The same unique ID used above.
    
    identification_file: a json file containing an array of string urls. Each url should depict between 1 and 10 faces. Each face within each url will be attempted to be identified as a member within the group. The faces within a photo will be specified using pixel coordinates.
    
    key: The same key used above.
    
Step 3: Clear groups

```python
iden.delete_group(personGroupId, key):
```
    
Deletes the group associated with a personGroupId.
    
Example call:
```python
import iden
iden.init_from_file('test_group', 'training_data.json', 'XXXXXXXXXXXXXXXXXXXXXXXXXXX')
iden.identify('test_group', 'identification_data.json', 'XXXXXXXXXXXXXXXXXXXXXXXXXXX')
iden.delete_group('test_group', 'XXXXXXXXXXXXXXXXXXXXXXXXXXX')
```



