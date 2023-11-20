# Integrantes:
# Juergen Pérez Céspedes
# Hillary Cruz Valenzuela
# Andrés Vega Hidalgo

from openai import OpenAI
import gradio as gr
import os


class AnimalChatbot:
    def __init__(self):
        self.OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.OPENAI_API_KEY)
        self.messages = [
            {"role": "system", "content": "Este chat gpt solo responde preguntas referentes a animales. Para preguntas no "
                                          "relacionadas a animales, el bot responde con No entiendo"}
        ]

    def is_animal_related(self, input_text):
        animal_keywords = ["animal", "mamífero", "ave", "reptil", "anfibio", "pez", "invertebrado", "hola"]
        return any(keyword in input_text.lower() for keyword in animal_keywords)

    def generate_response(self, prompt):
        if prompt:
            if self.is_animal_related(prompt):
                self.messages.append({"role": "user", "content": prompt})
                chat = self.client.chat.completions.create(
                    model="gpt-3.5-turbo-1106", messages=self.messages
                )
                reply = chat.choices[0].message.content
                self.messages.append({"role": "assistant", "content": reply})
            else:
                reply = "No entiendo. Por favor, hazme preguntas relacionadas con animales."

        return reply

    def chat(self, input, history):
        history = history or []
        my_history = list(sum(history, ()))
        my_history.append(input)
        my_input = ' '.join(my_history)
        output = self.generate_response(my_input)
        history.append((input, output))
        return history, history


def main():
    animal_chatbot = AnimalChatbot()

    with gr.Blocks() as bot:
        gr.Markdown("""
            <div style="background-color: #41465f; padding: 20px; border-radius:10px;">
                <h1 style="color: #ffffffff; font-family: Arial; text-align: center;">
                    Chat sobre Animales
                </h1>
            </div>
        """)
        chatbot = gr.Chatbot()
        chatbot.label = "Chat sobre animales"
        state = gr.State()
        text = gr.Textbox(placeholder="Hola, pregúntame algo animales. -> DALE ENTER PARA ENVIAR PREGUNTA", label="Pregunta -> DALE ENTER PARA ENVIAR PREGUNTA")
        text.submit(fn=animal_chatbot.chat, inputs=[text, state], outputs=[chatbot, state])

        submit = gr.Button("ENVIAR RESPUESTA")
        submit.click(animal_chatbot.chat, inputs=[text, state], outputs=[chatbot, state])

    bot.launch(share=True)


if __name__ == '__main__':
    main()