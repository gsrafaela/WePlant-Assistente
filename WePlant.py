import speech_recognition as sr
import pyttsx3
import openai


# Configura a chave de API da OpenAI
openai.api_key = ""

# Inicializa o motor de texto para voz
engine = pyttsx3.init()

# Inicializa o motor de reconhecimento de fala
r = sr.Recognizer()


# Configure as credenciais da API da OpenAI
def configure_openai(api_key):
    openai.api_key = api_key


def criar_lista_tarefas():
    lista_tarefas = []
    while True:
        print("Por favor, diga a tarefa que deseja adicionar: Plantar, Regar e/ou colher.")
        engine.say("Por favor, diga a tarefa que deseja adicionar: Plantar, Regar e/ou colher")
        engine.runAndWait()

        with sr.Microphone() as source:
            audio = r.listen(source)

        try:
            tarefa = r.recognize_google(audio, language="pt-BR")
            lista_tarefas.append(tarefa)
            print("Tarefa adicionada à lista de tarefas:", tarefa)
            engine.say("Tarefa adicionada à lista de tarefas.")
            engine.runAndWait()

        except sr.UnknownValueError:
            print("Desculpe, não consegui entender sua fala.")
            engine.say("Desculpe, não consegui entender sua fala.")
            engine.runAndWait()

        except sr.RequestError as e:
            print("Desculpe, ocorreu um erro ao solicitar resultados do reconhecimento de fala do Google:", e)
            engine.say("Desculpe, ocorreu um erro ao solicitar resultados do reconhecimento de fala do Google.")
            engine.runAndWait()

        # Verifica se o usuário deseja parar de adicionar tarefas
        print("Deseja adicionar mais tarefas? Diga sim ou não.")
        engine.say("Deseja adicionar mais tarefas? Diga sim ou não.")
        engine.runAndWait()
        with sr.Microphone() as source:
            audio = r.listen(source)

        try:
            resposta = r.recognize_google(audio, language="pt-BR")
            if "não" in resposta.lower():
                break
        except sr.UnknownValueError:
            pass

    return lista_tarefas


def realizar_pesquisa():
    print("O que sobre agricultura você gostaria de pesquisar?")
    engine.say("O que sobre agricultura você gostaria de pesquisar?")
    engine.runAndWait()

    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        topico = r.recognize_google(audio, language="pt-BR")
        print("Pesquisando informações sobre", topico)
        engine.say("Pesquisando informações sobre " + topico)
        engine.runAndWait()

        # Realiza a pesquisa usando a API da OpenAI
        resposta = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Pesquisar sobre " + topico,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5
        )

        resultado = resposta.choices[0].text.strip()
        print("Resultado da pesquisa:", resultado)
        engine.say("Aqui está o resultado da pesquisa: " + resultado)
        engine.runAndWait()

    except sr.UnknownValueError:
        print("Desculpe, não consegui entender sua fala.")
        engine.say("Desculpe, não consegui entender sua fala.")
        engine.runAndWait()

    except sr.RequestError as e:
        print("Desculpe, ocorreu um erro ao solicitar resultados do reconhecimento de fala do Google:", e)
        engine.say("Desculpe, ocorreu um erro ao solicitar resultados do reconhecimento de fala do Google.")
        engine.runAndWait()


# Loop principal do programa
while True:
    print("Como posso ajudar? Você pode dizer 'criar uma lista de tarefas', 'realizar uma pesquisa' ou 'sair'.")
    engine.say("Como posso ajudar? Você pode dizer 'criar uma lista de tarefas', 'realizar uma pesquisa' ou 'sair'.")
    engine.runAndWait()

    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        comando = r.recognize_google(audio, language="pt-BR")

        if "criar uma lista de tarefas" in comando.lower():
            lista_tarefas = criar_lista_tarefas()
            print("Lista de tarefas:")
            for tarefa in lista_tarefas:
                print("-", tarefa)

        elif "realizar uma pesquisa" in comando.lower():
            realizar_pesquisa()

        elif "sair" in comando.lower():
            engine.say("Até logo!")
            engine.runAndWait()
            break

        else:
            print("Desculpe, não entendi o comando.")
            engine.say("Desculpe, não entendi o comando.")
            engine.runAndWait()

    except sr.UnknownValueError:
        print("Desculpe, não consegui entender sua fala.")
        engine.say("Desculpe, não consegui entender sua fala.")
        engine.runAndWait()

    except sr.RequestError as e:
        print("Desculpe, ocorreu um erro ao solicitar resultados do reconhecimento de fala do Google:", e)
        engine.say("Desculpe, ocorreu um erro ao solicitar resultados do reconhecimento de fala do Google.")
        engine.runAndWait()
