#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HIDRA ACADEMY | Password Security Lab
Generador de contraseñas aleatorias para pruebas autorizadas.

Uso:
    python3 password_generator.py

Solo utiliza la biblioteca estándar de Python.
"""

import json
import secrets
import string
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config" / "password_rules.json"
EXISTING_FILE = BASE_DIR / "data" / "existing_passwords.txt"
OUTPUT_FILE = BASE_DIR / "output" / "generated_passwords.txt"

DEFAULT_CONFIG = {
    "length": {"min": 12, "max": 20},
    "separators": [".", "_", "-", "+", "@", "/", "|", ":"],
    "leet_rules": {
        "a": "4", "e": "3", "i": "1",
        "o": "0", "s": "5", "g": "6"
    },
    "special_rules": {
        "i": "!", "s": "$", "l": "|",
        "a": "@", "y": "&", "o": "()"
    }
}


def load_config():
    """Carga la configuración o crea una predeterminada."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(
            json.dumps(DEFAULT_CONFIG, indent=4, ensure_ascii=False) + "\n",
            encoding="utf-8"
        )

    try:
        config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        config.setdefault("length", DEFAULT_CONFIG["length"].copy())
        config.setdefault("separators", DEFAULT_CONFIG["separators"].copy())
        config.setdefault("leet_rules", DEFAULT_CONFIG["leet_rules"].copy())
        config.setdefault("special_rules", DEFAULT_CONFIG["special_rules"].copy())
        return config
    except (json.JSONDecodeError, OSError) as exc:
        raise RuntimeError(
            f"No se pudo leer la configuración {CONFIG_FILE}: {exc}"
        ) from exc


def ask_optional(prompt):
    """Solicita un dato opcional; Enter permite omitirlo."""
    value = input(f"{prompt} (Enter para omitir): ").strip()
    return value or None


def ask_int(prompt, default, minimum, maximum):
    """Solicita un entero dentro de un rango."""
    while True:
        raw = input(f"{prompt} [{default}]: ").strip()
        if not raw:
            return default
        try:
            value = int(raw)
            if minimum <= value <= maximum:
                return value
        except ValueError:
            pass
        print(f"Introduce un número entre {minimum} y {maximum}.")


def load_existing_passwords():
    """Carga las contraseñas que se deben excluir del resultado."""
    if not EXISTING_FILE.exists():
        return set()

    return {
        line.strip()
        for line in EXISTING_FILE.read_text(
            encoding="utf-8-sig"
        ).splitlines()
        if line.strip()
    }


def build_alphabet(separators):
    """Construye el conjunto de caracteres para generación aleatoria."""
    symbols = "".join(separators)
    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + symbols
    # Evita caracteres repetidos en el alfabeto.
    return "".join(dict.fromkeys(alphabet))


def random_password(length, alphabet, separators):
    """Genera una contraseña usando el generador criptográfico de secrets."""
    groups = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
    ]

    available_symbols = "".join(
        char for char in separators if char in alphabet
    )
    if available_symbols:
        groups.append(available_symbols)

    # Garantiza un carácter de cada categoría disponible.
    chars = [secrets.choice(group) for group in groups]
    chars.extend(
        secrets.choice(alphabet) for _ in range(length - len(chars))
    )
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def main():
    print("\n" + "=" * 58)
    print(" HIDRA ACADEMY | PASSWORD SECURITY LAB")
    print("=" * 58)
    print("Uso autorizado para laboratorios y auditorías.\n")

    # Los datos son opcionales y se recopilan en el orden solicitado.
    fields = {
        "Año": ask_optional("1. Año"),
        "País": ask_optional("2. País"),
        "Cargo o área": ask_optional("3. Cargo o área"),
        "Entidad o empresa abreviada": ask_optional(
            "4. Entidad o empresa abreviada"
        ),
    }

    print("\n--- RESUMEN DE DATOS PARA AUDITORÍA ---")
    for label, value in fields.items():
        print(f"{label}: {value or '(omitido)'}")

    try:
        config = load_config()
    except RuntimeError as exc:
        print(f"\n[ERROR] {exc}")
        return

    configured_min = int(config["length"].get("min", 12))
    configured_max = int(config["length"].get("max", 20))

    print("\n--- 3. OPCIONES DE GENERACIÓN ---")
    minimum = ask_int("Longitud mínima", configured_min, 8, 128)
    maximum = ask_int("Longitud máxima", max(configured_max, minimum), minimum, 128)
    quantity = ask_int("Cantidad de contraseñas", 10, 1, 500)

    print("\n--- 9. CARACTERES ESPECIALES (SEPARADORES) ---")
    configured_separators = config.get("separators", [])
    print("Configurados:", " ".join(configured_separators) or "(ninguno)")
    custom = input(
        "Añadir separadores (escribe los caracteres; Enter para omitir): "
    ).strip()

    separators = list(dict.fromkeys(configured_separators + list(custom)))

    print("\n--- 10. REEMPLAZO DE CARACTERES (REGLAS CONFIGURADAS) ---")
    print("Reglas numéricas:", config.get("leet_rules", {}))
    print("Reglas especiales:", config.get("special_rules", {}))
    print(f"Puedes editar estas reglas en: {CONFIG_FILE}")

    print("\n--- 4. VISTA PREVIA DE PATRONES ---")
    print("Plantillas de referencia (solo vista previa):")
    print("  {PALABRA}{SEPARADOR}{AÑO}")
    print("  {AÑO}{SEPARADOR}{PALABRA}")
    print("  {PALABRA}{SEPARADOR}{SÍMBOLO_FINAL}")
    print("Los datos de país, cargo y entidad no se convierten en candidatos.")

    existing = load_existing_passwords()
    alphabet = build_alphabet(separators)

    if len(alphabet) < 4:
        print("\n[ERROR] El conjunto de caracteres es demasiado pequeño.")
        return

    results = set()
    attempts = 0
    max_attempts = max(quantity * 100, 1000)

    while len(results) < quantity and attempts < max_attempts:
        attempts += 1
        length = secrets.randbelow(maximum - minimum + 1) + minimum
        candidate = random_password(length, alphabet, separators)

        if candidate not in existing:
            results.add(candidate)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        "".join(password + "\n" for password in sorted(results)),
        encoding="utf-8"
    )

    print("\n--- RESULTADOS ---")
    print(f"Solicitadas: {quantity}")
    print(f"Generadas: {len(results)}")
    print(f"Entradas existentes cargadas: {len(existing)}")
    print(f"Archivo de salida: {OUTPUT_FILE}")

    for password in sorted(results):
        print(f"  {password}")

    if len(results) < quantity:
        print(
            "\n[AVISO] No se alcanzó la cantidad solicitada dentro del "
            "límite de intentos."
        )


if __name__ == "__main__":
    main()
