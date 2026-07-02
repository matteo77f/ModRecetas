import os
from typing import Dict, List

try:
    import openai
except ImportError:
    openai = None

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = (
    "Eres un chef experto en cocina saludable. Recibes una receta original y una preferencia de modificación. "
    "Devuelve siempre un JSON con los campos: original_ingredients, modified_ingredients, modified_steps, warnings. "
    "No incluyas texto adicional fuera de la estructura JSON. Usa cantidades y nombres de ingredientes reales. "
    "Si el cambio puede afectar la química de la receta, agrega una advertencia breve en el campo warnings."
)

PROMPT_TEMPLATE = (
    "Receta original:\n{recipe_text}\n\n"
    "Preferencia de cambio: {preferences}\n\n"
    "Devuelve la respuesta en formato JSON con estas claves:\n"
    "original_ingredients: [{{name, quantity}}],\n"
    "modified_ingredients: [{{name, quantity}}],\n"
    "modified_steps: [texto de cada paso],\n"
    "warnings: [lista de advertencias]."
)


def parse_openai_response(response_text: str) -> Dict:
    try:
        import json
        return json.loads(response_text)
    except Exception:
        return {
            "original_ingredients": [],
            "modified_ingredients": [],
            "modified_steps": [],
            "warnings": ["Error parsing IA response. Revisa la configuración de OpenAI."],
        }


def generate_recommendations(recipe_text: str, preferences: str) -> Dict:
    if OPENAI_API_KEY and openai:
        openai.api_key = OPENAI_API_KEY
        prompt = PROMPT_TEMPLATE.format(recipe_text=recipe_text, preferences=preferences)
        completion = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        content = completion.choices[0].message.content
        return parse_openai_response(content)

    return {
        "original_ingredients": [
            {"name": "Receta original no procesada", "quantity": "1 unidad"}
        ],
        "modified_ingredients": [
            {"name": "Ingrediente saludable sugerido", "quantity": "1 unidad"}
        ],
        "modified_steps": [
            "Esta es una respuesta de ejemplo. Configura OPENAI_API_KEY para recibir recomendaciones reales."
        ],
        "warnings": [
            "La API de OpenAI no está configurada. Esta es una respuesta de demostración."
        ],
    }
