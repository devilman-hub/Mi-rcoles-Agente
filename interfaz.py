import ollama
import json
from datetime import datetime


class Agente:
    def __init__(self, model = "gemma3:1b", max_history = 10):
        self.model = model
        self.conversation_history = []
        self.max_history = max_history
        self.topics_proposed = []
        self.system_prompt = """Eres un agente conversacional inteligente y amigable. Tu objetivo es tener una conversación interesante y significativa con el usuario.
        
        Habilidades: 

        - Propones temas de conversación relevantes e interesantes.
        - Mantienes conversaciones naturales y fluidas.
        - Puedes profundizar en temas complejos.
        - Eres curioso y haces preguntas relevantes sobre el tema.
        - Te adaptas al estilo de la conversación del usuario.

        Cuando propongas temas, considera:

        - Intereses previos mostrados en la conversación.
        - Temas actuales y relevantes.
        - Balance entre profundidad y accesibilidad.
        - Diversidad de áreas (Ciencia, Cultura, Tecnología, etc).
        
        Responde siempre en Español y de forma Natural y Conversacional.

        """


    def add_to_history(self, role, content):
            self.conversation_history_append({
                "role": role,
                "content": content
            })

            if len(self.conversation_history)>self.max_history:
                self.conversation_historiy = self.conversation_history[-self.max_history] #Para que mantenga la cantidad de mensajes.

    def get_messages(self):
            messages = [{"role": "system", "content": self.system_prompt}]
            messages.extend(self.conversation_history)
            return messages
        
    def propose_topic(self):
            prompt = """Proponga un tema de conversación interesante y atractivo. 
            
            Considera: 
            
            - Que sea algo que genere una buena discusión.
            -  Que sea algo accesible y profundo. 
            - Que despierte curiosidad e interés.

            Formato: Presenta el tema en 3-5 líneas máximo, de forma entusiasta y con una pregunta para empezar la conversación.
            """

            self.add_to_history("user", prompt)
            response = ollama.chat(
                model = self.model,
                messages = self.get_messages()
            )

            topic = response['message']['content']
            self.add_to_history("assistant", topic)
            self.topics_proposed.append({
                "topic": topic,
                "timestamp": datetime.now().isoformat()
            })

            return topic
        
    def chat(self, user_message): 
            self.add_to_history("user", user_message)
            try:
                response = ollama.chat(
                    model = self.model,
                    messages = self.get_messages() 
                )
                
                assistant_message = response['message']['content']
                self.add_to_history("assistant", assistant_message)
                return assistant_message

            except Exception as e:
                return f"Error al comunicarse con el Orquestador:{str(e)}"
            
    def get_conversation_summary(self):
            if not self.conversation_history:
                return "No existe conversación activa."
            total_message = len(self.conversation_history)
            user_message = len([m for m in self.conversation_history if m['role'] == 'user'])
            return f"""
                        
            Resumen de la Conversación:
            - Total de Mensajes: {total_message}
            - Mensajes de Usuario: {user_message}
            - Temas propuestos: {len(self.topics_proposed)}
            """
        
    def  reset_conversation(self):
            self.conversation_history = []
            self.topics_proposed = []
            print("Reiniciando... ... ...")

def main():
    print("Iniciando Atente IA... Espere un momento.")
    agent = Agente(model = "gemma3:1b")
    print("Pille el tema: \n")
    initial_topic = agent.propose_topic()
    print(f"Agente: \n{initial_topic}")

    while True:
        try:

            user_input = input('Yo:').strip()

            if not user_input:
                continue

            if user_input.lower()== 'salir':
                print("Suerte.")

            elif user_input.lower()== 'proponer':
                print("Pille el tema: \n")
                topic = agent.propose_topic()
                print(f"Agente: \n{topic}")

            elif user_input.lower() == 'resumen':
                print(agent.get_conversation_summary())
            
            elif user_input.lower() == 'reiniciar':
                agent.reset_conversation()
                print("Agente: Otra vez iniciamos.")
            
            else:
                print("Agente: ", end = "", flush = True)
                response = agent.chat(user_input)
                print(f"{response}")
            

        except KeyboardInterrupt:
            print("\n Vemos perro.")
            break

        except Exception as e:
            print(f"Error:{str(e)}")


if __name__ == "__main__":
    main()


