MODEL = "gpt-5.6-luna"

FAILURES_LIST = """No enciende
No se apaga
Se apaga solo
Se reinicia
Funciona a ratos
Se para solo
Hace ruido
Vibra mucho
Huele a quemado
Echa humo
Se calienta demasiado
Pierde agua
Tiene una fuga
No coge agua
No desagua
No calienta
Calienta poco
Calienta demasiado
No enfría
Enfría poco
No congela
Hace demasiado hielo
No seca
No centrifuga
No gira
No tiene fuerza
No aspira
No echa aire
No abre
No cierra
Está atascado
No responde a los botones
No responde al mando
No carga
La batería dura poco
Marca error
La pantalla no funciona
No se ve
Se ve mal
La imagen se corta
No hay señal
La señal va y viene
No encuentra canales
No hay sonido
Se oye mal
El sonido se corta
No conecta
Pierde la conexión
No reconoce el dispositivo
No funciona una conexión
No funciona la luz
No mantiene la temperatura
No termina el programa
El programa no funciona
Salta el automático
Da corriente
Tiene una pieza rota o suelta
"""

APPLIANCES_LIS="""
Televisión
TDT
Antena
Decodificador
Equipo de música
Altavoz
Radio
Reproductor DVD/Blu-ray
Lavadora
Secadora
Lavavajillas
Frigorífico
Congelador
Horno
Microondas
Vitrocerámica
Placa de inducción
Campana extractora
Cafetera
Hervidor
Tostadora
Batidora
Licuadora
Exprimidor
Robot de cocina
Freidora
Freidora de aire
Sandwichera
Plancha de cocina
Aspiradora
Robot aspirador
Plancha
Centro de planchado
Ventilador
Aire acondicionado
Calefactor
Radiador eléctrico
Estufa eléctrica
Humidificador
Deshumidificador
Purificador de aire
Termo eléctrico
Calentador
Secador de pelo
Máquina de afeitar
Depiladora
Cepillo de dientes eléctrico
Báscula
Máquina de coser
Taladro
Herramienta eléctrica
Cargador
Transformador
Mando a distancia
Teléfono fijo
Router
Repetidor Wi-Fi
Monitor
Impresora
Proyector
Otro
"""

SYSTEM_PROMPT = f"""Haz como si fueras un asistente para un reparador
               de electrodomesticos y necesitas sacar la informacion
               clave de los avisos de reparacion a partir de la
               llamada de un cliente. 
               
               Extrae solo la información que esté explícitamente en 
               el texto, si no, devuelve null. Además pon sólo 
               información relevante para la resolución de la avería. 
               Si el cliente añade datos que no ayudan a la resolución, 
               ignóralos.
               
               Los nombres de las personas pueden tener acentos o no,
               lo mejor es que le quites todos los acentos. Además, en
               el campo nombre, queremos sólo añadir nombres y apellidos
               que sean correctos. En muchos casos, la información se da
               en forma de mote, o en forma relativa (estuviste ayer en
               mi casa, vivo al lado de angel el panadero). Todo esto
               no habría que ponerlo en el campo de nombre. Aunque incluso
               si es relativo (soy Pedro, el primo de María), Pedro debe
               ir al campo nombre, porque es absoluto, y el primo de 
               María debe ir a other_details
               
               La dirección hay que unificarla. Tendrá que empezar siempre
               por el tipo de vía (calle, avenida) y ser consistente en
               como la escribes. Después el nombre de la calle. Después
               vendrán los números, sin separar sin comas, sólo espacios
               en blanco. Si alguno de los números no están en la información,
               déjalos en blanco. Después la población si la hubiera. Entonces,
               el formato debe ser siempre, por ejemplo
               Calle Salvador 25 3 1 Villahermosa
               En esta dirección es la calle salvador, número 25, piso 3, puerta
               1, en la población española. No añadas numerales, sólo el número.
               
               Para la descripción del fallo, manda únicamente un fallo
               de esta lista, y si no hay ningún candidato claro, escribe
               "Avería desconocida": {FAILURES_LIST}.
               
               Para la appliance muestra también el campo que más se ajuste
               a esta lista. Si no hay ningún candidato claro, escribe "Otro".
               Esta es la lista:{APPLIANCES_LIS}.
               
               Si hay información extra que no hayas podido reflejar en ninguno
               de estos cambios porque ha habido que descartarla, y crees
               que aún así podría ser relevante como información sobre la avería,
               escríbela en forma de texto libre en "otros detalles". Por ejemplo,
               si dice cada cuánto pasa, algún síntoma más concreto, si el nombre
               no es explícito pero da alguna referencia informal como un mote, o
               una relativa, como que vive cerca de alguien, o al lado de la casa
               de otra persona.
               
               
               
               Identifica también el tipo de mensaje, si es uno nuevo, a
               ctualización de datos, cancelación. Si no está claro qué 
               tipo es, usa el tipo undetermined"""

