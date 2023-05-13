import openai
from openai import ChatCompletion
openai.api_key="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"
response=ChatCompletion.create(model="gpt-3.5-turbo")