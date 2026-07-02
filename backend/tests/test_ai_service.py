from backend.ai_service import parse_openai_response, generate_recommendations


def test_parse_openai_response_with_invalid_json():
    invalid_json = "{not valid json}"
    parsed = parse_openai_response(invalid_json)
    assert parsed["original_ingredients"] == []
    assert parsed["modified_ingredients"] == []
    assert "Error parsing IA response" in parsed["warnings"][0]


def test_generate_recommendations_returns_structure():
    result = generate_recommendations("Harina, azúcar, leche", "hacerla vegana")
    assert isinstance(result, dict)
    assert "original_ingredients" in result
    assert "modified_ingredients" in result
    assert "modified_steps" in result
    assert "warnings" in result
