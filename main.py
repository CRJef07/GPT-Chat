# Integrantes:
# Juergen Pérez Céspedes
# Hillary Cruz Valenzuela
# Andrés Vega Hidalgo

from openai import OpenAI
import os

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


def main():
    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
        ]
    )

    print(completion.choices[0].message)


if __name__ == '__main__':
    main()
