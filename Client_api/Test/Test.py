import json
with open('Test/a.json') as data_file:
            dataJson = json.load(data_file)
# a=(dataJson['request']['intent']['slots']['Commands']['resolutions']['resolutionsPerAuthority'])
intent=dataJson['request']['intent']['slots']['commands']['value']
for i in intent:
    print(i)
            # for i in a:
                # value=i['value']['name']