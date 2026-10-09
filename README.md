# ReconPassword

Motor de pruebas de patrones de contraseña para laboratorios y auditorías autorizadas. Esta primera versión funciona por terminal; la interfaz Tkinter se añadirá después de validar la lógica.

## Requisitos

- Python 3.9 o posterior
- No requiere dependencias externas

## Estructura

```text
ReconPassword/
├── password_generator.py
├── config/password_rules.json
├── data/existing_passwords.txt
├── output/
└── tests/
```

## Ejecución

```bash
python3 password_generator.py
```

Introduce un año o identificador de prueba y palabras ficticias separadas por comas. Los resultados se guardan en `output/generated_passwords.txt`.

## Configuración

Edita `config/password_rules.json` para cambiar:

- Longitud mínima y máxima.
- Reglas de sustitución numérica (`leet_rules`), por ejemplo `g: 6`.
- Reglas de sustitución especial (`special_rules`).
- Separadores permitidos.
- Plantillas de patrón, usando `{WORD}`, `{YEAR}` y `{SEP}`.

Ejemplo de plantilla:

```json
"{WORD}{SEP}{YEAR}"
```

## Exclusión de resultados existentes

Añade una entrada por línea a `data/existing_passwords.txt`. Las coincidencias exactas se omiten de los resultados. Este mecanismo **no** hace comparación normalizada ni guarda hashes; por tanto, úsalo solo con datos ficticios de laboratorio y no almacenes contraseñas reales.

## Seguridad

- Utiliza la herramienta solo en sistemas propios o con autorización explícita.
- No introduzcas credenciales reales ni listas filtradas que contengan secretos personales.
- La longitud es una validación de caracteres, no una medición de fortaleza.
- Este prototipo es un motor de patrones de prueba, no un generador de contraseñas aleatorias criptográficamente seguras.

## Licencia

Elige una licencia antes de publicar el repositorio (por ejemplo, MIT si deseas permitir reutilización con atribución).
