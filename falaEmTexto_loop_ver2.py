chave1 = ""
regiao = ""


#***************************************************************************
# Reconhecer e converter fala em texto [Speech service]
#
# Serviços cognitivos  ==>  Speech
#
# https://learn.microsoft.com/pt-br/azure/cognitive-services/speech-service/get-started-speech-to-text?tabs=terminal&pivots=programming-language-python
#
# pip install azure-cognitiveservices-speech
# pip install mysql-connector-python
#
#***************************************************************************


from os import system

system('cls')

if chave1 == "" or regiao == "":
    print('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('+++ Necessário informar a Chave e Regiao da Azure +++')
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
    exit()


import azure.cognitiveservices.speech as speechsdk
import mysql.connector

# subscription ==> CHAVE 1
# region       ==> Localização/região
  
def recognize_from_microphone():
    print("\nAguardado fala ...\n")        
    speech_config = speechsdk.SpeechConfig(subscription=chave1, region=regiao)   
    speech_config.speech_recognition_language="pt-BR"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)    
        
    while True:
        speech_recognition_result = speech_recognizer.recognize_once_async().get()
        if speech_recognition_result.text != "":
            break            
    
    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        if speech_recognition_result.text[0:-1].lower() == 'tom e jerry':
            exit()

        print(f"Falando: {speech_recognition_result.text[0:-1]}")
        gravar_banco(speech_recognition_result.text[0:-1])

    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        # print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        print("", end='')
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")


def gravar_banco(texto):
    conexao = mysql.connector.connect(
        host = 'cognitive18052023.mysql.database.azure.com',
        user = 'tux',
        password = 'Mud@r123',
        database = 'db_azure'
    )

    cursor = conexao.cursor()
    comando = f'INSERT INTO tbl_fala (texto) VALUES ("{texto}")'
    cursor.execute(comando)
    conexao.commit()
    cursor.close()
    conexao.close()

if __name__ == '__main__':
    while True:
        recognize_from_microphone()
		
