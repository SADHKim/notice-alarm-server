import requests

response = requests.get('http://127.0.0.1:5000/api/websites')

print(response.json())


data = {'user' : 'seongah', 'email' : 'kimsa0322@gmail.com', 'website' : '한양대 컴소 졸프게시판'}
response = requests.post('http://127.0.0.1:5000/api/email', json=data)
print(response.json())

