// TEXTOS DE LA HISTORIA SEMANAL DE VACUNAS PARTICULARES
// Para cambiar un texto, edite solo este archivo. Variaciones: A, B1, B2, B3.
// WhatsApp 301 655 3822: EXCLUSIVO de esta historia semanal.
const COMUN = {
  whatsapp: "301 655 3822",
  sinOrden: "No necesita orden médica",
  sede: "Disponible en nuestra sede de Valledupar · Carrera 11 # 14-34",
  eslogan: "¡La Salud, nuestro compromiso!"
};

const VARIACIONES = {
  A: {
    p1: { etiqueta: "Vacunas particulares", titulo: "¡Vacúnese y amplíe su protección!", apoyo: "Conozca nuestro portafolio de vacunas particulares." },
    p2: { etiqueta: "Vacunas disponibles", lista: ["Meningococo", "Neumococo", "Virus del papiloma humano (VPH)", "Herpes zóster", "Hepatitis A", "Hepatitis B", "Tétanos", "Varicela", "Influenza", "Hexavalente", "Dengue", "Otras"] },
    p3: { etiqueta: "¿Por qué vacunarse?", puntos: ["Amplía sus opciones de protección.", "Ayuda a prevenir enfermedades.", "Ayuda a reducir el riesgo de complicaciones.", "Cuida su bienestar y el de su familia."],
          llamado: "Agende su valoración por WhatsApp y reciba asesoría de nuestro equipo de profesionales de la salud." }
  },
  B1: {
    p1: { etiqueta: "¿Sabía que…?", titulo: "Los virus de la influenza cambian con el tiempo", apoyo: "" },
    p2: { etiqueta: "Influenza", texto: "Por eso la vacuna se actualiza cada temporada. Ayuda a prevenir la influenza y sus complicaciones." },
    p3: { etiqueta: "Vacuna de influenza", puntos: [], llamado: "Pregunte por la vacuna de influenza. Agende su valoración:" }
  },
  B2: {
    p1: { etiqueta: "¿Sabía que…?", titulo: "El virus de la varicela se queda en el cuerpo", apoyo: "" },
    p2: { etiqueta: "Varicela y herpes zóster", texto: "Años después puede reactivarse y causar herpes zóster. Hay vacunas que ayudan a prevenir ambas enfermedades." },
    p3: { etiqueta: "Varicela y herpes zóster", puntos: [], llamado: "Pregunte por la vacuna de varicela y herpes zóster." }
  },
  B3: {
    p1: { etiqueta: "¿Sabía que…?", titulo: "Existen muchos tipos de virus del papiloma humano (VPH)", apoyo: "" },
    p2: { etiqueta: "VPH", texto: "Algunos pueden causar cáncer de cuello uterino. La vacuna ayuda a prevenir las infecciones por los tipos más comunes." },
    p3: { etiqueta: "Vacuna contra el VPH", puntos: [], llamado: "Pregunte por la vacuna contra el VPH." }
  }
};
