global dictionary
dictionary = dict()
print(dictionary)
dictionary ['file.py'] = 'running'
print(dictionary)
print(dictionary['file.py'])
currentCheck = dictionary.get('file.py')
if currentCheck == 'running':
    print('here')