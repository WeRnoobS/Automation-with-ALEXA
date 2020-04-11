import requests

def getting_Device_location():
    url=requests.get("https://alexautomation.herokuapp.com/read?id=url")
    with open('url.txt', 'w') as file:
        file.write(url.text)
    return url.text
def getting_device_location_form_tmp():
    try:
        with open('url.txt','r') as file:
            gobal=file.readline()
        if gobal!="":
            print(gobal)    
            return gobal
        else :
            getting_Device_location()        
    except:
        print("identifier")

getting_Device_location()
url=getting_device_location_form_tmp()
print("this is "+url)