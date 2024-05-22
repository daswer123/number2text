_ones = ["", "bir", "ikki", "uch", "to'rt", "besh", "olti", "yetti", "sakkiz", "to'qqiz"]
_teens = ["o'n", "o'n bir", "o'n ikki", "o'n uch", "o'n to'rt", "o'n besh", "o'n olti", "o'n yetti", "o'n sakkiz", "o'n to'qqiz"]
_tens = ["", "", "yigirma", "o'ttiz", "qirq", "ellik", "oltmish", "yetmish", "sakson", "to'qson"]
_hundreds = ["", "bir yuz", "ikki yuz", "uch yuz", "to'rt yuz", "besh yuz",
             "olti yuz", "yetti yuz", "sakkiz yuz", "to'qqiz yuz"]

_scales = [
    ("", "", ""),
    ("ming", "ming", "ming"),
    ("million", "million", "million"),
    ("milliard", "milliard", "milliard"),
    # ...
]

def convert_less_than_thousand(number):
    if number < 10:
        return _ones[number]
    elif number < 20:
        return _teens[number - 10]
    elif number < 100:
        tens, ones = divmod(number, 10)
        if ones == 0:
            return _tens[tens]
        else:
            return _tens[tens] + " " + _ones[ones]
    else:
        hundreds, less_than_hundred = divmod(number, 100)
        if less_than_hundred == 0:
            return _hundreds[hundreds]
        else:
            return _hundreds[hundreds] + " " + convert_less_than_thousand(less_than_hundred)

def get_scale(number, scale_index):
    if scale_index == 0:
        return ""
    elif number == 1:
        return _scales[scale_index][0]
    else:
        return _scales[scale_index][1]

def convert(number):
    if number == 0:
        return "nol"

    if number < 0:
        return "minus " + convert(-number)

    parts = []
    scale_index = 0
    while number > 0:
        if number % 1000 != 0:
            part = convert_less_than_thousand(number % 1000)
            scale = get_scale(number % 1000, scale_index)
            if scale:
                part += " " + scale
            parts.append(part)
        number //= 1000
        scale_index += 1

    return " ".join(reversed(parts))