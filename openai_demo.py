import openai
with open('key.txt') as f:
    openai.api_key=f.read().strip()
response=openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=[{"role":"user","content":"Who are you?"}])
print(response)