
import openai


openai.api_key = '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'



def chat_with_gpt3(prompt):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": prompt}
      ]
    )
    return response.choices[0].message.content



