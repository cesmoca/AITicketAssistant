class Case:
    input = ""
    expected_name = ""
    expected_address = ""
    expected_appliance = ""
    expected_failure = ""
    expected_type = ""


cases: list[Case] = [
    {
        "input": "Hola, soy Pedro Martínez. Se me ha estropeado la lavadora, no enciende. Estoy en calle salvador número 25. Pasate pronto, por favor, gracias!",
        "expected_name": "Pedro Martinez",
        "expected_address": "Calle Salvador 25",
        "expected_appliance": "Lavadora",
        "expected_failure": "No enciende",
        "expected_type": "new",
    },
    {
        "input": "Cesar, que soy pedro martínez otra vez, ya te dije que la lavadora no se enciende. No se por qué. estoy en salvador veinticinco. Estoy todo el dia viendo la tele y con ropa sucia porque no puedo lavar",
        "expected_name": "Pedro Martinez",
        "expected_address": "Calle Salvador 25",
        "expected_appliance": "Lavadora",
        "expected_failure": "No enciende",
        "expected_type": "new",
    },
    {
        "input": "Oye, que soy pedro otra vez, he llamado esta mañana. Mira, que ya no vengas, que ya nos hemos apañado",
        "expected_name": "Pedro",
        "expected_address": None,
        "expected_appliance": "Otro",
        "expected_failure": "Avería desconocida",
        "expected_type": "cancel",
    },
    {
        "input": "Oye cesareo, que llevo ya tres dias esperando, pasate hombre, que la mujer se va a cabrear. Venga",
        "expected_name": None,
        "expected_address": None,
        "expected_appliance": "Otro",
        "expected_failure": "Avería desconocida",
        "expected_type": "undetermined",
    },
    {
        "input": "Cesareo, que soy pedro otra vez, mira que no te pases por mi casa, pásate por casa de mi tía, que vive en calle domingo, 27, que yo no voy a estar en casa",
        "expected_name": "Pedro",
        "expected_address": "Calle Domingo 27",
        "expected_appliance": "Otro",
        "expected_failure": "Avería desconocida",
        "expected_type": "update",
    },

    {
        "input":"Mira cesáreo, que soy la de la calle libertad de la Ossa, que me he equivocado, no era la lavadora, sino la secadora la que no funciona, pasate cuanto antes posible",
        "expected_name":None,
        "expected_address":"calle libertad de la Ossa",
        "expected_appliance":"Secadora",
        "expected_failure":"Avería desconocida",
        "expected_type":"update",
    },
    
    # {
    #     "input":"",
    #     "expected_name":"",
    #     "expected_address":"",
    #     "expected_appliance":"",
    #     "expected_failure":"",
    #     "expected_type":"",
    # },
]
