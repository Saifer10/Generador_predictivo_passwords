#!/usr/bin/env python3
"""ReconPassword: motor de pruebas de patrones y exclusión de duplicados.

Uso previsto: laboratorios y auditorías autorizadas. No almacenes aquí credenciales
reales; el archivo de exclusión es texto plano y se compara por coincidencia exacta.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config" / "password_rules.json"
EXISTING_FILE = BASE_DIR / "data" / "existing_passwords.txt"
OUTPUT_FILE = BASE_DIR / "output" / "generated_passwords.txt"


def load_config():
    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        config = json.load(file)

    min_len = config["length"]["min"]
    max_len = config["length"]["max"]
    if not isinstance(min_len, int) or not isinstance(max_len, int):
        raise ValueError("Las longitudes deben ser números enteros.")
    if min_len < 1 or max_len < min_len:
        raise ValueError("Rango de longitud inválido.")
    return config


def load_existing_passwords():
    if not EXISTING_FILE.exists():
        return set()
    with EXISTING_FILE.open("r", encoding="utf-8") as file:
        return {line.strip() for line in file if line.strip() and not line.lstrip().startswith("#")}


def apply_rules(text, rules):
    """Aplica reglas por carácter, sin re-procesar el texto de reemplazo."""
    result = []
    for char in text:
        replacement = rules.get(char.lower())
        result.append(replacement if replacement is not None else char)
    return "".join(result)


def render_pattern(pattern, word, year, separator):
    return pattern.format(WORD=word, YEAR=year, SEP=separator)


def generate_patterns(words, year, config):
    """Genera variantes limitadas según patrones y separadores configurados."""
    min_len = config["length"]["min"]
    max_len = config["length"]["max"]
    separators = config.get("separators", [])
    patterns = config.get("patterns", [])
    leet_rules = config.get("leet_rules", {})
    special_rules = config.get("special_rules", {})
    results = set()
    stats = {"too_short": 0, "too_long": 0}

    for raw_word in words:
        word = "".join(raw_word.split())
        if not word:
            continue

        variants = {
            word,
            word.lower(),
            word.capitalize(),
            apply_rules(word, leet_rules),
            apply_rules(word, special_rules),
        }

        for variant in variants:
            for pattern in patterns:
                pattern_separators = separators if "{SEP}" in pattern else [""]
                for separator in pattern_separators:
                    candidate = render_pattern(pattern, variant, year, separator)
                    if len(candidate) < min_len:
                        stats["too_short"] += 1
                    elif len(candidate) > max_len:
                        stats["too_long"] += 1
                    else:
                        results.add(candidate)

    return results, stats


def main():
    print("=" * 62)
    print(" ReconPassword | Motor de patrones de laboratorio")
    print("=" * 62)
    print("Usa únicamente datos ficticios o una auditoría autorizada.\n")

    try:
        config = load_config()
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"[ERROR] No se pudo cargar la configuración: {exc}")
        return 1

    year = input("Año para la prueba (por ejemplo, 2026): ").strip()
    if not year:
        print("[ERROR] Debes introducir un año o identificador de prueba.")
        return 1

    print("Introduce palabras de laboratorio separadas por comas.")
    raw_words = input("Palabras: ").strip()
    words = [item.strip() for item in raw_words.split(",") if item.strip()]
    if not words:
        print("[ERROR] Introduce al menos una palabra.")
        return 1

    existing = load_existing_passwords()
    results, stats = generate_patterns(words, year, config)
    filtered = results - existing

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        for item in sorted(filtered):
            file.write(item + "\n")

    print("\n--- Resumen ---")
    print(f"Resultados únicos antes del filtro: {len(results)}")
    print(f"Excluidos por coincidencia exacta:  {len(results & existing)}")
    print(f"Resultados finales:                 {len(filtered)}")
    print(f"Fuera de longitud mínima:            {stats['too_short']}")
    print(f"Fuera de longitud máxima:            {stats['too_long']}")
    print(f"Archivo de salida: {OUTPUT_FILE}")
    print("\nMuestra de resultados:")
    for item in sorted(filtered)[:20]:
        print(f"  {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
