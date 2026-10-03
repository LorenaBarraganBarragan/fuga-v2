Create the FUGA+ UML Class Diagram.

IMPORTANT: Physically create this file using the terminal/filesystem:

docs/diagramas/diagrama-clases.drawio

Do NOT just describe it.
Do NOT only show XML in the chat.

Use the existing folder:

docs/diagramas

Create a valid Draw.io XML file containing the following UML classes.

TITLE:
Diagrama de Clases — FUGA+

SUBTITLE:
Clases principales, atributos, métodos y relaciones

CLASSES:

Usuario
Attributes:

* idUsuario: String
* nombre: String
* correo: String
* contraseñaHash: String
* rol: RolUsuario
* estado: EstadoUsuario

Methods:

* registrarse()
* iniciarSesion()
* cerrarSesion()
* actualizarPerfil()

Gasto
Attributes:

* idGasto: String
* monto: Decimal
* moneda: String
* categoria: Categoria
* descripcion: String
* fecha: Date
* textoOriginal: String
* usuarioId: String

Methods:

* confirmar()
* editarCategoria()
* consultarDetalle()

Categoria
Attributes:

* idCategoria: String
* nombre: String

Methods:

* listarCategorias()
* validarCategoria()

PosibleFuga
Attributes:

* idFuga: String
* categoria: String
* descripcion: String
* cantidadOcurrencias: Integer
* montoAcumulado: Decimal
* reglaActivada: String
* fechaDeteccion: Date

Methods:

* detectar()
* calcularAcumulado()
* obtenerEvidencia()
* verificarDatosSuficientes()

Alerta
Attributes:

* idAlerta: String
* tipo: String
* mensaje: String
* fecha: Date
* leida: Boolean

Methods:

* generar()
* marcarComoLeida()

AnalizadorGasto
Attributes:

* textoEntrada: String

Methods:

* interpretarGasto()
* extraerMonto()
* extraerMoneda()
* extraerCategoria()
* extraerDescripcion()
* validarInterpretacion()

Autenticacion
Attributes:

* correo: String
* credencialesValidas: Boolean

Methods:

* registrarUsuario()
* autenticar()
* cerrarSesion()
* verificarEstado()
* validarRol()

ComparadorPeriodos
Attributes:

* periodoInicial: Date
* periodoFinal: Date
* totalPeriodo: Decimal
* cantidadGastos: Integer
* promedioGasto: Decimal

Methods:

* comparar()
* calcularVariacionAbsoluta()
* calcularVariacionPorcentual()

RELATIONSHIPS:

Usuario 1 -------- 0..* Gasto

Categoria 1 -------- 0..* Gasto

Usuario 1 -------- 0..* PosibleFuga

PosibleFuga 1 -------- 1..* Gasto

Usuario 1 -------- 0..* Alerta

PosibleFuga 1 -------- 0..* Alerta

AnalizadorGasto ..> Gasto
label: interpreta

Autenticacion ..> Usuario
label: autentica

ComparadorPeriodos ..> Gasto
label: analiza

ROLE VALUES:

RolUsuario:

* Visitante
* Usuario
* Administrador

EstadoUsuario:

* Activo
* Inactivo

IMPORTANT:

All visible text in the diagram must be in Spanish.

Use standard UML class notation:

* class name
* attributes
* methods
* associations
* multiplicities
* dependency arrows

Do NOT create classes for MongoDB, OpenAI, API, Backend, Frontend, React, Node, JWT or Database.

Do NOT create classes for bank connections, payments, transfers, cards, loans, investments or financial advice.

Make the diagram clean, readable and well organized.

Place Usuario, Gasto, Categoria and PosibleFuga in the center.

Place AnalizadorGasto, Autenticacion, Alerta and ComparadorPeriodos around them.

AFTER creating the file, verify it with:

Test-Path "docs\diagramas\diagrama-clases.drawio"

Then verify the file exists and has a size greater than 0.

If the verification returns False, DO NOT say that the file was created. Fix the file creation first.

FINAL RESPONSE ONLY AFTER SUCCESS:

Created and verified:
docs/diagramas/diagrama-clases.drawio
