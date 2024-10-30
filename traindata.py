import json
import random

# Definir preguntas y respuestas más detalladas y variadas
questions = [
    "Hola, ¿cómo estás?", "¿Cuál es tu nombre?", "¿Qué día es hoy?", "¿Qué puedes hacer?",
    "¿Cuál es tu color favorito?", "¿Cuál es la capital de Francia?", "¿Cómo está el clima hoy?",
    "Cuéntame un chiste", "¿Qué es Python?", "¿Cuál es tu comida favorita?", "¿Qué hora es?",
    "¿Cuál es el significado de la vida?", "¿Dónde está la biblioteca?", "Cuéntame algo interesante",
    "¿Cómo se dice 'hola' en francés?", "¿Qué es el aprendizaje automático?", "¿Quién es el presidente de Estados Unidos?",
    "¿Cuál es la distancia de la Tierra a la Luna?", "¿Qué es el coronavirus?", "¿Cuál es la capital de Japón?",
    "¿Qué es el aprendizaje profundo?", "¿Cómo funciona una red neuronal?", "¿Qué es un algoritmo?",
    "¿Qué es la inteligencia artificial?", "¿Qué es el procesamiento del lenguaje natural?", "¿Qué es la ciencia de datos?",
    "¿Qué es el big data?", "¿Cómo aprenden las máquinas?", "¿Qué es un modelo predictivo?", "¿Qué es una red neuronal profunda?",
    "¿Cuál es el océano más grande?", "¿Qué es el cambio climático?", "¿Qué es una célula madre?", "¿Cuál es la capital de Australia?",
    "¿Qué es la fotosíntesis?", "¿Cómo funciona el motor de un coche?", "¿Quién escribió 'Cien años de soledad'?",
    "¿Cuál es la diferencia entre HTML y CSS?", "¿Qué es la economía circular?", "¿Qué es la física cuántica?",
    "¿Cómo se prepara una tortilla española?", "¿Cuál es el río más largo del mundo?", "¿Qué es una estrella fugaz?",
    "¿Cómo se genera la electricidad?", "¿Qué es un agujero negro?", "¿Cuál es el deporte más popular del mundo?",
    "¿Qué es una supernova?", "¿Cuál es el animal más rápido del mundo?", "¿Qué es el efecto invernadero?"
]

answers = [
    "Hola, ¿qué tal?", "Soy tu asistente virtual, ¿en qué te puedo ayudar?", "Hoy es un día genial, ¿verdad?",
    "Puedo ayudarte con muchas cosas, solo pregúntame.", "No tengo un color favorito, pero me gusta el azul.",
    "La capital de Francia es París, ¡una ciudad hermosa!", "No puedo ver el clima ahora, pero siempre es un buen día para sonreír.",
    "¡Aquí va uno! ¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter.", "Python es un lenguaje de programación super útil.",
    "No como, pero he oído que la pizza es genial.", "Lo siento, no tengo reloj, pero siempre es un buen momento para aprender algo nuevo.",
    "El significado de la vida... esa es una gran pregunta, ¡disfruta cada momento!", "La biblioteca está por allá, ¿necesitas un libro específico?",
    "¿Sabías que las ballenas azules son los animales más grandes del planeta?", "'Hola' en francés se dice 'Bonjour'.",
    "El aprendizaje automático permite a las computadoras aprender de los datos. ¡Muy cool!", "El presidente de Estados Unidos es Joe Biden.",
    "La distancia de la Tierra a la Luna es de unos 384,400 kilómetros.", "El coronavirus es un virus que causa enfermedades respiratorias.",
    "La capital de Japón es Tokio. ¡Me encantaría visitarla algún día!", "El aprendizaje profundo es una rama de la inteligencia artificial.",
    "Una red neuronal imita el cerebro humano para procesar información.", "Un algoritmo es una serie de pasos para resolver un problema.",
    "La inteligencia artificial es cuando las máquinas hacen cosas inteligentes.", "El procesamiento del lenguaje natural ayuda a las máquinas a entendernos mejor.",
    "La ciencia de datos es como buscar tesoros en grandes montones de datos.", "El big data se refiere a datos enormes y complejos.",
    "Las máquinas aprenden detectando patrones en los datos.", "Un modelo predictivo adivina lo que podría pasar en el futuro.",
    "Una red neuronal profunda tiene muchas capas para entender mejor los datos.", "El océano más grande es el Pacífico. ¡Gigante!",
    "El cambio climático está alterando nuestro planeta. Es un tema importante.", "Una célula madre puede convertirse en diferentes tipos de células.",
    "La capital de Australia es Canberra.", "La fotosíntesis permite a las plantas convertir luz en energía.",
    "El motor de un coche quema combustible para moverse.", "Gabriel García Márquez escribió 'Cien años de soledad'.",
    "HTML estructura una página web y CSS la hace bonita.", "La economía circular busca reducir residuos y reutilizar recursos.",
    "La física cuántica estudia las cosas más pequeñas del universo.", "Para una tortilla española necesitas huevos, patatas y cebolla.",
    "El río más largo es el Nilo.", "Una estrella fugaz es un meteoro que entra en nuestra atmósfera.",
    "La electricidad se genera moviendo turbinas con viento, agua o vapor.", "Un agujero negro tiene una gravedad tan fuerte que nada puede escapar.",
    "El deporte más popular es el fútbol.", "Una supernova es la explosión de una estrella masiva.", "El animal más rápido es el guepardo.",
    "El efecto invernadero atrapa el calor en la atmósfera de la Tierra."
]

# Generar 8,000,000 registros de datos sintéticos
data = []
for _ in range(8000000):
    question = random.choice(questions)
    answer = random.choice(answers)
    data.append({"question": question, "answer": answer})

# Guardar los datos en un archivo JSON
with open('data2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Archivo JSON generado con 8,000,000 registros.")
