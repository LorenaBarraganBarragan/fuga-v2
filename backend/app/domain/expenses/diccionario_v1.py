"""
Diccionario v1.0 — Clasificador de gastos FUGA+
Fuente de verdad para categorías, palabras clave y descripciones genéricas.
Versión: 1.0
"""

DICCIONARIO_VERSION = "1.0"
REGLAS_VERSION = "1.0"

# Las 9 categorías cerradas (D-02). El nombre debe coincidir EXACTAMENTE con el seed de BD.
# La clave de cada categoría es su nombre normalizado (minúsculas, sin tildes).
CATEGORIAS: dict[str, dict] = {
    "alimentacion": {
        "nombre": "Alimentación",
        "orden": 1,
        "keywords": [
            # Comida y bebida
            "comida", "almuerzo", "desayuno", "cena", "merienda", "meriendas",
            "restaurante", "restaurantes", "cafeteria", "cafetería", "cafe", "café",
            "pizza", "hamburguesa", "hamburguesas", "sushi", "tacos", "arepas", "arepa",
            "empanada", "empanadas", "bandeja", "corriente", "menu", "menú",
            # Mercado y compras de alimentos
            "mercado", "supermercado", "tienda", "frutas", "verduras", "carniceria",
            "panaderia", "panadería", "dulces", "snacks", "agua", "jugo", "juegos",
            "gaseosa", "gaseosas", "bebida", "bebidas",
            # Domicilios y delivery
            "domicilio", "delivery", "rappi", "ifood", "ubereats", "didi food",
            # Términos genéricos de alimentación
            "comidas", "alimento", "alimentos", "alimentacion",
        ],
    },
    "transporte": {
        "nombre": "Transporte",
        "orden": 2,
        "keywords": [
            "taxi", "taxista", "uber", "cabify", "didi", "indriver",
            "bus", "buseta", "colectivo", "metro", "transmilenio", "sitp",
            "moto", "motocicleta", "bicicleta", "ciclovía", "patineta",
            "gasolina", "combustible", "parqueadero", "parqueo", "peaje",
            "transporte", "pasaje", "boleto", "tiquete", "pasaportes",
            "vuelo", "avion", "avión", "aeropuerto", "tren", "flota",
            # Movilidad
            "carrera", "movilidad", "desplazamiento",
        ],
    },
    "vivienda": {
        "nombre": "Vivienda",
        "orden": 3,
        "keywords": [
            "arriendo", "arrendamiento", "alquiler", "renta",
            "administracion", "administración", "cuota", "conjunto",
            "hipoteca", "credito hipotecario",
            "mantenimiento", "reparacion", "reparación", "plomero", "electricista",
            "pintura", "muebles", "nevera", "lavadora", "estufa", "horno",
            "vivienda", "apartamento", "casa", "habitacion", "habitación",
        ],
    },
    "servicios": {
        "nombre": "Servicios",
        "orden": 4,
        "keywords": [
            "luz", "electricidad", "energia", "energía", "epm", "codensa",
            "acueducto", "alcantarillado", "recibo de agua", "factura de agua",
            "gas", "natural gas",
            "internet", "wifi", "banda ancha", "fibra",
            "telefono", "teléfono", "celular", "plan de datos", "recargas", "recarga",
            "television", "televisión", "tv", "cable", "claro", "movistar", "tigo",
            "servicios", "servicio", "factura", "recibo", "pago de",
        ],
    },
    "educacion": {
        "nombre": "Educación",
        "orden": 5,
        "keywords": [
            "universidad", "colegio", "escuela", "matricula", "matrícula",
            "pension", "pensión", "cuota educativa",
            "curso", "cursos", "clase", "clases", "taller", "talleres",
            "libro", "libros", "cuaderno", "cuadernos", "útiles", "utiles",
            "capacitacion", "capacitación", "diplomado", "certificado", "certificación",
            "ingles", "inglés", "frances", "francés", "idiomas",
            "tutoria", "tutoría", "profesor", "profesora",
            "plataforma educativa", "coursera", "udemy", "platzi",
            "educacion", "educación", "aprendizaje",
        ],
    },
    "salud": {
        "nombre": "Salud",
        "orden": 6,
        "keywords": [
            "medicina", "medicamento", "medicamentos", "pastilla", "pastillas",
            "farmacia", "droguería", "drogueria", "drogas",
            "medico", "médico", "médica", "doctor", "doctora", "cita",
            "consulta", "consultas", "especialista", "odontologo", "odontólogo",
            "dentista", "oculista", "ojos", "lentes", "gafas",
            "clinica", "clínica", "hospital", "urgencias", "eps", "ips",
            "copago", "cuota moderadora",
            "laboratorio", "examen", "examenes", "análisis", "radiografia",
            "fisioterapia", "psicologia", "psicología", "terapia",
            "vitaminas", "suplemento", "suplementos",
            "salud", "bienestar",
        ],
    },
    "entretenimiento": {
        "nombre": "Entretenimiento",
        "orden": 7,
        "keywords": [
            "cine", "pelicula", "película", "peliculas", "películas",
            "teatro", "concierto", "conciertos", "evento", "eventos",
            "netflix", "spotify", "disney", "hbo", "prime", "apple tv",
            "videojuego", "videojuegos", "juego", "juegos", "xbox", "playstation",
            "steam", "gaming",
            "bar", "discoteca", "rumba", "fiesta", "tragos", "cerveza", "cervezas",
            "bebida alcoholica", "alcohol",
            "deporte", "deportes", "gym", "gimnasio", "natacion", "natación",
            "yoga", "pilates", "futbol", "fútbol", "tenis", "piscina",
            "libro", "novela", "musica", "música",
            "paseo", "viaje", "vacaciones", "hotel", "hostal",
            "entretenimiento", "diversión", "diversion", "ocio",
        ],
    },
    "compras": {
        "nombre": "Compras",
        "orden": 8,
        "keywords": [
            # Ropa y accesorios
            "ropa", "camisa", "camiseta", "pantalon", "pantalón", "zapatos", "tenis",
            "botas", "medias", "ropa interior", "chaqueta", "abrigo",
            "bolso", "cartera", "mochila", "maleta",
            "accesorios", "joyeria", "joyería", "reloj", "relojes",
            # Tecnología
            "celular", "computador", "laptop", "tablet", "audifonos", "audífonos",
            "cargador", "cable", "mouse", "teclado", "monitor",
            # Hogar y otros
            "regalo", "regalos", "detalle", "detalles",
            "cosmeticos", "cosméticos", "maquillaje", "perfume", "crema",
            "shampoo", "jabon", "jabón", "papel",
            # Tiendas
            "amazon", "mercadolibre", "alkosto", "falabella", "zara", "h&m",
            # Genérico de tienda
            "tienda", "almacén", "almacen",
        ],
    },
    "otros": {
        "nombre": "Otros",
        "orden": 9,
        "keywords": [],  # Otros es el fallback; no tiene keywords propias
    },
}

# Descripciones que son demasiado genéricas para activar la regla FUGA-01.
# Fuente de verdad para rule_fuga_01.py y grouping.py.
# Cualquier cambio requiere nueva versión del diccionario.
GENERICAS: list[str] = [
    "gasto", "gastos", "compra", "compras", "pago", "pagos",
    "cosa", "cosas", "algo", "otros", "otro", "vario", "varios",
    "mercado", "tienda", "deuda", "deudas", "pendiente", "pendientes",
    "etc", "varios gastos", "cosas varias",
]
