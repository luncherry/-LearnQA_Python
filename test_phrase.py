def test_short_phrase():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, f"Фраза '{phrase}' длиннее или равна 15 символам (длина: {len(phrase)})"