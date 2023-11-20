# Integrantes:
# Juergen Pérez Céspedes
# Hillary Cruz Valenzuela
# Andrés Vega Hidalgo

from openai import OpenAI
import gradio as gr
import os

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)

messages = [
    {"role": "system", "content": "Este chat gpt solo responde preguntas referentes a animales. Para preguntas no "
                                  "relacionadas a animales, el bot responde con No entiendo"},

    {"role": "user", "content": "¿Qué es un animal?"},

    {"role": "assistant", "content": "Un animal es un ser vivo perteneciente al reino animalia, que constituye un "
                                     "grupo biológico que incluye una amplia variedad de organismos. Los animales son "
                                     "organismos multicelulares, lo que significa que están formados por más de una "
                                     "célula, y son heterótrofos, lo que implica que obtienen su alimento consumiendo "
                                     "otros organismos o sustancias orgánicas. Los animales presentan una diversidad "
                                     "increíble en términos de forma, tamaño, comportamiento y hábitat. Pueden "
                                     "clasificarse en diferentes grupos, como mamíferos, aves, reptiles, anfibios, "
                                     "peces e invertebrados. Cada grupo tiene características únicas que los "
                                     "distinguen. Además, los animales desempeñan roles importantes en los "
                                     "ecosistemas, ya que participan en cadenas alimentarias, contribuyen a la "
                                     "polinización de las plantas, ayudan en la descomposición de materia orgánica y "
                                     "desempeñan numerosas funciones en los diversos hábitats de la Tierra."}
]

def is_animal_related(input_text):
    animal_keywords = ["animal", "mamífero", "ave", "reptil", "anfibio", "pez", "invertebrado", "hola"]
    return any(keyword in input_text.lower() for keyword in animal_keywords)

def generate_response(prompt):
    if prompt:
        if is_animal_related(prompt):
            messages.append({"role": "user", "content": prompt})
            chat = client.chat.completions.create(
                model="gpt-3.5-turbo", messages=messages
            )
            reply = chat.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})
        else:
            reply = "No entiendo. Por favor, hazme preguntas relacionadas con animales."

    return reply

def my_chatbot(input, history):
    history = history or []
    my_history = list(sum(history, ()))
    my_history.append(input)
    my_input = ' '.join(my_history)
    output = generate_response(my_input)
    history.append((input, output))
    return history, history


with gr.Blocks() as bot:
    gr.Markdown("""
            <div style="background-color: #f0f0f0; padding: 20px;">
                <h1 style="color: #008000; font-family: Arial; text-align: center;">
                    Chat sobre Animales
                </h1>
            </div>
        """)
    chatbot = gr.Chatbot()
    state = gr.State()
    text = gr.Textbox(placeholder="Hola, pregúntame algo animales. -> DALE ENTER PARA ENVIAR PREGUNTA", label="Pregunta -> DALE ENTER PARA ENVIAR PREGUNTA")
    text.submit(fn=my_chatbot, inputs=[text, state], outputs=[chatbot, state])

    submit = gr.Button("ENVIAR RESPUESTA")
    submit.click(my_chatbot, inputs=[text, state], outputs=[chatbot, state])


def main():
    bot.launch(share=True)


if __name__ == '__main__':
    main()
