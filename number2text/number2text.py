def convert_number_to_text(number, language='en'):
    if language == 'en':
        import lang.en as lang
    elif language == 'uz':
        import lang.uz as lang
    elif language == 'ru':
        import lang.ru as lang
    else:
        raise ValueError(f"Unsupported language: {language}")

    return lang.convert(number)
