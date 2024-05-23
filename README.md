# Number2Text

Welcome to the Number2Text project! This Python package provides a convenient way to convert numbers into their textual representations in various languages. Whether you need to convert integers, floating-point numbers, or even fractions, Number2Text has got you covered.

## Interesting Fact
*This library was written 90% using LLM agents, everything from writing the code to validating the result rests on the shoulders of LLMs*

## Features
- Support for a wide range of languages (see the list below)
- Conversion of integers, floating-point numbers, and fractions
- Easy-to-use API with a simple `convert` method
- Retrieval of supported languages using the `supported_languages` method

## Supported Languages
Number2Text currently supports the following languages:
- English (en)
- Russian (ru)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Chinese (zh)
- Japanese (ja)
- Korean (ko)
- Arabic (ar)
- Hindi (hi)
- Bengali (bn)
- ... and many more!

## Installation
You can install the Number2Text package using pip:

```bash
pip install number2text
```

## Usage
Here's a quick example of how to use Number2Text:

```python
from number2text.number2text import NumberToText

# Create an instance of NumberToText with the default language (English)
converter = NumberToText()

# Convert a number to text
result = converter.convert(42)
print(result)  # Output: "forty-two"

# Convert a floating-point number to text
result = converter.convert(3.14)
print(result)  # Output: "three point one four"

# Get the list of supported languages
supported_langs = NumberToText.supported_languages()
print("Supported languages:", supported_langs)
```

## TODO
- Add support for symbolic numbers (e.g., π, e)
- Improve the overall quality and accuracy of the conversions
- Expand language support to cover even more languages

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request on the [GitHub repository](https://github.com/daswer123/number2text).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
