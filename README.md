# Query Assistant (FastAPI + PySpark + Next.js)

* Autor: Neobytes84
* Project_URL: https://github.com/neobytes84/query-assistant

Asistente que convierte preguntas en lenguaje natural a código PySpark, lo ejecuta sobre un CSV y muestra los resultados en un frontend Next.js.

## Arquitectura

- **query-parser** (FastAPI, :8001) → genera código PySpark a partir de texto.
- **execution-engine** (FastAPI + PySpark, :8002) → ejecuta el código sobre `data.csv`.
- **history-service** (FastAPI + SQLAlchemy, :8003) → guarda historial (opcional).
- **frontend** (Next.js, :3000) → UI para el usuario.

Todos los servicios traen **CORS habilitado** para `http://localhost:3000`.

## Conocimientos previos
1️⃣ Backend
Python avanzado:

Estructura de proyectos.

Manejo de excepciones y tipos (pydantic, BaseModel).

Uso de entornos virtuales.

FastAPI:

Creación de rutas (@app.post, @app.get).

Middlewares (CORS).

Validación de datos con pydantic.

Bases de datos:

SQL básico y modelado de tablas.

ORM con SQLAlchemy (definir modelos, sesiones, consultas).

Conexiones vía DATABASE_URL y uso de .env.

Apache Spark (nivel básico a intermedio):

DataFrames de Spark (select, limit, toJSON).

Lectura de CSV y manipulación de columnas.

Docker & Docker Compose:

Entender cómo levantar múltiples servicios en contenedores.

Variables de entorno en contenedores (env_file).

2️⃣ Frontend
JavaScript / TypeScript:

Tipado básico (interface, type).

Manejo de promesas (async/await).

React:

Componentes funcionales y hooks (useState).

Manejo de eventos y estado.

Next.js:

Estructura de pages o app/.

Rutas y APIs.

TailwindCSS (básico):

Clases para estilos rápidos y responsive.

Consumo de APIs REST con axios o fetch.

3️⃣ Infraestructura y DevOps
Control de versiones con Git/GitHub:

Ramas, commits, merges, .gitignore.

Buenas prácticas para no subir datos sensibles (.env, claves).

Buenas prácticas de seguridad:

No exponer credenciales.

Usar .env.example para repos públicos.

4️⃣ Extra (para largo plazo)

## Requisitos

- Docker / Docker Compose
- Node 18+ (para frontend)
- (Opcional) Python 3.11 para desarrollo local

## Variables de entorno

Crear un `.env` en la **raíz** (no se sube a git):

## Para probar los servicios
### Parser
curl -X POST http://localhost:8001/parse \
  -H "Content-Type: application/json" \
  -d '{"question": "Show top 5 values of column cnt"}'

### Execution
curl -X POST http://localhost:8002/run \
  -H "Content-Type: application/json" \
  -d '{"code": "result = df.select(\"cnt\").limit(5)"}'

### Para el frontend
cd frontend
npm install
npm run dev
# abre http://localhost:3000



