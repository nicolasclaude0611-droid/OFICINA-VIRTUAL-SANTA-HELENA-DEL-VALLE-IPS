# Episodio 1 · medicina general y vacunación (guion aprobado por Nicolas el 25-nov-2026)
# Cada mito: creencia (voz «a»), veredicto («mito» o «verdad»), respuesta (voz «b») y hasta 4 puntos que
# aparecen cuando la voz dice su palabra. Íconos disponibles: ver ICONOS en gen.py.

EPISODIO = 1

MITOS = [
    dict(
        creencia='Si me siento bien, no necesito chequeo.',
        voz_a='mv1-a', voz_b='mv1-b', veredicto='mito',
        texto_b='Muchas enfermedades, como la hipertensión arterial, la diabetes o las dislipidemias, no dan síntomas al comienzo. Un chequeo las detecta a tiempo, cuando es más fácil tratarlas y prevenir complicaciones.',
        claves=['hipertensión', 'diabetes', 'dislipidemias', 'síntomas', 'chequeo'],
        puntos=[
            ('presion', 'Hipertensión arterial', 'hipertensión'),
            ('azucar', 'Diabetes', 'diabetes'),
            ('grasa', 'Dislipidemias <small>(grasas elevadas en la sangre)</small>', 'dislipidemias'),
            ('lupa', 'Un <b>chequeo</b> las detecta a tiempo', 'chequeo'),
        ],
        etiqueta=('SIN SÍNTOMAS<br>AL COMIENZO', 'síntomas'),
    ),
    dict(
        creencia='Las vacunas son solo para niños.',
        voz_a='mv2-a', voz_b='mv2-b', veredicto='mito',
        texto_b='Las vacunas protegen toda la vida, no solo en la niñez. Algunas necesitan refuerzos con los años, como la vacuna contra el tétanos. Y otras se aplican cada año, como la vacuna contra la influenza.',
        claves=['toda', 'vida,', 'refuerzos', 'tétanos.', 'año,', 'influenza.'],
        puntos=[
            ('edades', 'Protegen <b>toda la vida</b>', 'vida'),
            ('refuerzo', 'Algunas se refuerzan: vacuna contra el <b>tétanos</b>', 'tétanos'),
            ('calendario', 'Otras, <b>cada año</b>: vacuna contra la influenza', 'influenza'),
        ],
    ),
    dict(
        creencia='Las vacunas debilitan las defensas.',
        voz_a='mv5-a', voz_b='mv5-b', veredicto='mito',
        texto_b='Al contrario: una vacuna le enseña al cuerpo a reconocer un germen, sin enfermarlo, para que sepa defenderse.',
        claves=['contrario:', 'reconocer', 'defenderse.'],
        puntos=[
            ('germen', 'Le enseña al cuerpo a <b>reconocer</b> un germen', 'reconocer'),
            ('escudo', 'Sin enfermarlo, para que sepa <b>defenderse</b>', 'defenderse'),
        ],
    ),
    dict(
        creencia='Ya casi no hay esas enfermedades, no hace falta vacunarse.',
        voz_a='mv6-a', voz_b='mv6-b', veredicto='mito',
        texto_b='Son poco comunes, como el sarampión o la polio, justamente porque la mayoría se vacunó. Pero los gérmenes siguen existiendo, y si baja la vacunación, esas enfermedades pueden volver.',
        claves=['sarampión', 'polio,', 'vacunó.', 'existiendo,', 'volver.'],
        puntos=[
            ('familia', 'Son poco comunes porque <b>la mayoría se vacunó</b>', 'vacunó'),
            ('germen', 'Los gérmenes <b>siguen existiendo</b>', 'existiendo'),
            ('alerta', 'Si baja la vacunación, <b>pueden volver</b>', 'volver'),
        ],
    ),
]
