import base64
import json
import mimetypes
import os
import re
from typing import Dict, List

from dotenv import load_dotenv

try:
    import openai
except ImportError:
    openai = None

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_IMAGE_MODEL = os.getenv("OPENAI_IMAGE_MODEL", "gpt-4.1-mini")

SYSTEM_PROMPT = (
    "Eres un chef experto en cocina saludable. Recibes una receta original y una preferencia de modificación. "
    "Devuelve siempre un JSON con los campos: original_ingredients, modified_ingredients, modified_steps, warnings. "
    "No incluyas texto adicional fuera de la estructura JSON. Usa cantidades y nombres de ingredientes reales. "
    "Si la preferencia indica un ingrediente concreto a sustituir, sugiere un reemplazo para ese ingrediente y conserva el resto de la receta original. "
    "Si el cambio puede afectar la química de la receta, agrega una advertencia breve en el campo warnings."
)

PROMPT_TEMPLATE = (
    "Receta original:\n{recipe_text}\n\n"
    "Preferencia de cambio: {preferences}\n\n"
    "Devuelve SOLO un objeto JSON válido con estas claves: original_ingredients, modified_ingredients, modified_steps, warnings.\n"
    "El formato debe ser exactamente así:\n"
    "{{\n"
    "  \"original_ingredients\": [{{\"name\": \"...\", \"quantity\": \"...\"}}],\n"
    "  \"modified_ingredients\": [{{\"name\": \"...\", \"quantity\": \"...\"}}],\n"
    "  \"modified_steps\": [\"paso 1\", \"paso 2\"],\n"
    "  \"warnings\": [\"advertencia 1\", \"advertencia 2\"]\n"
    "}}\n"
    "No escribas texto adicional fuera de ese JSON."
)


def parse_openai_response(response_text: str) -> Dict:
    try:
        return json.loads(response_text)
    except Exception:
        # Intentar extraer un bloque JSON válido dentro de la respuesta
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", response_text, re.S)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass

        start = response_text.find("{")
        end = response_text.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidate = response_text[start:end+1]
            try:
                return json.loads(candidate)
            except Exception:
                pass

        return {
            "original_ingredients": [],
            "modified_ingredients": [],
            "modified_steps": [],
            "warnings": ["Error parsing IA response. Revisa la configuración de OpenAI."],
        }


def image_bytes_to_data_url(image_bytes: bytes, filename: str | None = None) -> str:
    content_type, _ = mimetypes.guess_type(filename or "")
    if not content_type:
        content_type = "image/png"
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{content_type};base64,{b64}"


def extract_text_from_image(image_bytes: bytes, filename: str | None = None) -> Dict[str, str]:
    if OPENAI_API_KEY and openai:
        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            data_url = image_bytes_to_data_url(image_bytes, filename)
            response = client.responses.create(
                model=OPENAI_IMAGE_MODEL,
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": "Extrae todo el texto de receta de esta imagen y responde solo con el texto reconocido."
                            },
                            {
                                "type": "input_image",
                                "image_url": data_url,
                            },
                        ],
                    }
                ],
            )

            if getattr(response, "output_text", None):
                return {"text": response.output_text.strip()}

            text_segments = []
            for item in getattr(response, "output", []):
                contents = getattr(item, "content", [])
                for content in contents:
                    if getattr(content, "type", None) == "output_text":
                        text_segments.append(getattr(content, "text", ""))
                    elif isinstance(content, dict) and content.get("type") == "output_text":
                        text_segments.append(content.get("text", ""))

            extracted_text = "\n".join(text_segments).strip()
            if extracted_text:
                return {"text": extracted_text}

            return {"error": "No se pudo extraer texto de la imagen."}
        except Exception as exc:
            return {"error": f"Error de OpenAI al procesar la imagen: {str(exc)}"}

    return {"error": "La API de OpenAI no está configurada para procesar imágenes."}


def generate_recommendations(recipe_text: str, preferences: str) -> Dict:
    if OPENAI_API_KEY and openai:
        prompt = PROMPT_TEMPLATE.format(recipe_text=recipe_text, preferences=preferences)
        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            completion = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            content = completion.choices[0].message.content
            return parse_openai_response(content)
        except Exception as exc:
            return {
                "original_ingredients": [
                    {"name": "Receta original no procesada", "quantity": "1 unidad"}
                ],
                "modified_ingredients": [
                    {"name": "Ingrediente saludable sugerido", "quantity": "1 unidad"}
                ],
                "modified_steps": [
                    "No se pudo procesar la respuesta de OpenAI. Configura una clave válida para recibir recomendaciones reales."
                ],
                "warnings": [
                    f"Error de OpenAI: {str(exc)}"
                ],
            }

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
