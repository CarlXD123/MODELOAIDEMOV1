from flask import Flask, request, jsonify, send_file  # Importamos Flask y sus funciones para manejar peticiones, respuestas JSON, y envío de archivos
from flask_cors import CORS  # Importamos CORS para permitir solicitudes desde distintos orígenes
import joblib  # Importamos joblib para cargar y guardar modelos
import pandas as pd  # Pandas se usa para manipular datos tabulares
import json  # JSON se usa para cargar y guardar datos en archivos JSON
import os  # Proporciona funciones para interactuar con el sistema operativo
import re  # Expresiones regulares para trabajar con patrones en cadenas
from sklearn.model_selection import train_test_split  # Para dividir los datos en entrenamiento y prueba
from sklearn.feature_extraction.text import TfidfVectorizer  # Para convertir texto en vectores numéricos
from sklearn.linear_model import LogisticRegression  # Modelo de clasificación
from gtts import gTTS  # Para convertir texto a voz
import time  # Para trabajar con tiempos y generar nombres únicos
import speech_recognition as sr  # Para reconocer y convertir audio en texto
import webbrowser  # Para abrir sitios web en el navegador predeterminado
from pydub import AudioSegment  # Para manejar y convertir archivos de audio

# Inicializamos la aplicación Flask
app = Flask(__name__)
CORS(app)  # Permitimos solicitudes de distintos orígenes

# Cargamos el modelo y el vectorizador
model = joblib.load('model.pkl')  # Cargamos el modelo de clasificación desde un archivo
vectorizer = joblib.load('vectorizer.pkl')  # Cargamos el vectorizador de TF-IDF desde un archivo

# Definimos el archivo donde almacenaremos nuevas muestras para reentrenamiento
new_data_file = 'new_data.json'

# Creamos la carpeta 'audio' si no existe para almacenar archivos de audio
audio_folder = 'audio'
if not os.path.exists(audio_folder):
    os.makedirs(audio_folder)

# Inicializamos el archivo de nuevas muestras si no existe
if not os.path.exists(new_data_file):
    with open(new_data_file, 'w') as f:
        json.dump([], f)  # Creamos un JSON vacío en el archivo

# Función para convertir un archivo de audio en texto usando reconocimiento de voz
def recognize_speech_from_audio(audio_path):
    recognizer = sr.Recognizer()  # Inicializamos el reconocedor
    audio_file = sr.AudioFile(audio_path)  # Cargamos el archivo de audio
    with audio_file as source:
        audio = recognizer.record(source)  # Grabamos el audio para procesarlo
    try:
        text = recognizer.recognize_google(audio, language='es-ES')  # Intentamos convertir el audio en texto en español
        return text
    except sr.UnknownValueError:
        return "No se pudo entender el audio"  # Mensaje de error si el audio no es claro
    except sr.RequestError as e:
        return f"Error al solicitar resultados del servicio de reconocimiento de voz; {e}"  # Error de solicitud

# Función para manejar comandos especiales detectados en el texto de entrada
def handle_special_commands(command):
    commands = {  # Diccionario con comandos especiales y sus respectivas acciones
        "youtube": "YouTube",
        "google": "Google",
        "facebook": "Facebook",
        "crea una carpeta": "create_folder",
    }
    
    urls = {  # Diccionario con URLs asociadas a comandos específicos
        "YouTube": "https://www.youtube.com",
        "Google": "https://www.google.com",
        "Facebook": "https://www.facebook.com",
    }
    
    # Buscar coincidencias con los comandos en el texto de entrada
    for key in commands:
        if re.search(r'\b' + key + r'\b', command.lower()):  # Usamos expresiones regulares para detectar el comando
            if commands[key] == "create_folder":
                match = re.search(r'crea una carpeta llamada (.+)', command.lower())  # Detectamos el nombre de la carpeta
                if match:
                    folder_name = match.group(1).strip()
                    if folder_name:
                        folder_path = os.path.join(audio_folder, folder_name)
                        if not os.path.exists(folder_path):
                            os.makedirs(folder_path)  # Creamos la carpeta si no existe
                            return f"Carpeta '{folder_name}' creada exitosamente."
                        else:
                            return f"La carpeta '{folder_name}' ya existe."
                    else:
                        return "No se proporcionó un nombre para la carpeta."
            else:
                site_name = commands[key]
                url = urls[site_name]
                webbrowser.open(url)  # Abrimos la URL correspondiente
                return f"Abriendo {site_name}"
    return None  # Si no hay coincidencias, regresamos None

# Ruta para hacer predicciones usando el modelo
@app.route('/predict', methods=['POST'])
def predict():
    if 'audio' in request.files:  # Verificamos si el archivo de audio está en la solicitud
        audio_file = request.files['audio']
        audio_path = os.path.join(audio_folder, audio_file.filename)
        audio_file.save(audio_path)  # Guardamos el archivo de audio en la carpeta

        # Convertimos el archivo a formato WAV si es necesario
        if not audio_path.endswith('.wav'):
            sound = AudioSegment.from_file(audio_path)
            audio_path_wav = audio_path.replace(audio_path.split('.')[-1], 'wav')
            sound.export(audio_path_wav, format="wav")
            audio_path = audio_path_wav

        # Reconocemos el texto a partir del audio
        data = recognize_speech_from_audio(audio_path)
    else:
        data = request.json['text']  # Si no hay audio, usamos el texto en el JSON de la solicitud
    
    # Verificamos si hay comandos especiales en el texto
    command_response = handle_special_commands(data.lower())
    if command_response:
        response_text = command_response
    else:
        data_vec = vectorizer.transform([data])  # Transformamos el texto a un vector
        prediction = model.predict(data_vec)  # Realizamos la predicción
        response_text = prediction[0]

    # Convertimos el texto de respuesta en audio
    tts = gTTS(response_text, lang='es')
    timestamp = int(time.time())  # Usamos un timestamp para nombres únicos
    audio_response_path = os.path.join(audio_folder, f'response_{timestamp}.mp3')
    tts.save(audio_response_path)  # Guardamos el archivo de audio de respuesta

    # Devolvemos el archivo de audio como respuesta
    return send_file(audio_response_path, mimetype='audio/mp3')

# Ruta para actualizar el archivo JSON con nuevas muestras
@app.route('/update', methods=['POST'])
def update():
    new_data = request.json  # Obtenemos los datos de la solicitud
    new_question = new_data['question']
    new_answer = new_data['answer']

    # Guardamos la nueva muestra en el archivo JSON
    with open(new_data_file, 'r') as f:
        data = json.load(f)

    data.append({'question': new_question, 'answer': new_answer})

    with open(new_data_file, 'w') as f:
        json.dump(data, f)

    return jsonify({'message': 'New data added successfully'})

# Ruta para reentrenar el modelo con los datos nuevos
@app.route('/retrain', methods=['POST'])
def retrain():
    # Cargamos todas las muestras, incluidas las nuevas
    with open(new_data_file, 'r') as f:
        new_data = json.load(f)

    # Cargamos los datos originales y los combinamos con las nuevas muestras
    with open('large_conversations.json', 'r') as f:
        original_data = json.load(f)

    all_data = original_data + new_data
    df = pd.DataFrame(all_data)  # Convertimos los datos en un DataFrame

    # Dividimos los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(df['question'], df['answer'], test_size=0.2, random_state=42)

    # Vectorizamos el texto
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Entrenamos un modelo de regresión logística
    model.fit(X_train_vec, y_train)

    # Guardamos el modelo y el vectorizador actualizados
    joblib.dump(model, 'model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')

    return jsonify({'message': 'Model retrained successfully'})

# Ejecutamos la aplicación en modo de depuración
if __name__ == '__main__':
    app.run(debug=True)
