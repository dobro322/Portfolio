import requests

data = {
  "date": 1564334951,
  "from_id": 21766756,
  "id": 0,
  "out": 0,
  "peer_id": 2000000100,
  "text": "123",
  "conversation_message_id": 13,
  "fwd_messages": [],
  "random_id": 0,
  "attachments": [],
}
result = requests.post('https://ocheredsut.ru/api/1/conversations/messages', json=data)
print(result.text)
