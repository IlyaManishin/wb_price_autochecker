import requests

HEADERS = {
    "Authorization" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgwZjM4ZTZmLTQ3NjAtNDQ1YS04MjBiLTRkYmY0YjIyNjRjOCJ9.G9ZbrNpqQFFeJM5cSlxTqjucoul1RJToZfyvS1MrPIU"
}

url  = "https://feedbacks-api.wb.ru/api/v1/feedbacks/count-unanswered"
response = requests.get(url, headers=HEADERS)
print(response.status_code)
print(response.text)
url  = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks?isAnswered=false&take=5&skip=0"
response = requests.get(url, headers=HEADERS)
print(response.status_code)
print(response.text)