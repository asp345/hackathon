import openai
with open('openai_key.txt') as f:
    openai.api_key=f.read().strip()
A_val=0
B_val=0
A='사람 A는'+A_val+' 한 사람이다.'
B='사람 B는'+B_val+' 한 사람이다.'

content_merged=A+'\n'+B+'\n'+'이 두 사람이 만났을 때 대화하기 좋은 주제를 설명 없이 키워드로만 추천해줘'
response=openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=[{"role":"user","content":content_merged}])
print(response)