_ones= ["", "ერთი", "ორი", "სამი", "ოთხი", "ხუთი", "ექვსი", "შვიდი", "რვა", "ცხრა"]
_teens = ["ათი", "თერთმეტი", "თორმეტი", "ცამეტი", "თოთხმეტი", "თხუთმეტი", "თექვსმეტი", "ჩვიდმეტი", "თვრამეტი", "ცხრამეტი"]
_tens = ["", "", "ოცი", "ოცდაათი", "ორმოცი", "ორმოცდაათი", "სამოცი", "სამოცდაათი", "ოთხმოცი", "ოთხმოცდაათი"] 
_hundreds = ["", "ას", "ორას", "სამას", "ოთხას", "ხუთას", "ექვსას", "შვიდას", "რვაას", "ცხრაას"]

_scales = [
    ("", "", ""),
    ("ათას", "ათას", "ათას"),  
    ("მილიონ", "მილიონ", "მილიონ"),
    ("მილიარდ", "მილიარდ", "მილიარდ"),
    ("ტრილიონ", "ტრილიონ", "ტრილიონ"),
    ("კვადრილიონ", "კვადრილიონ", "კვადრილიონ"),
    ("კვინტილიონ", "კვინტილიონ", "კვინტილიონ"),
    ("სექსტილიონ", "სექსტილიონ", "სექსტილიონ"),
    ("სეპტილიონ", "სეპტილიონ", "სეპტილიონ"),
    ("ოქტილიონ", "ოქტილიონ", "ოქტილიონ"),
    ("ნონილიონ", "ნონილიონ", "ნონილიონ"),
    ("დეცილიონ", "დეცილიონ", "დეცილიონ"),
]

_fractions = {
    2: 'ნახევარი',
    3: 'მესამედი',
    4: 'მეოთხედი',
    5: 'მეხუთედი',
    6: 'მეექვსედი',
    7: 'მეშვიდედი',
    8: 'მერვედი',
    9: 'მეცხრედი',
    10: 'მეათედი',
}

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
            return _tens[tens] + _ones[ones]
    else:
        hundreds, less_than_hundred = divmod(number, 100)
        if less_than_hundred == 0:
            return _hundreds[hundreds]
        else:
            return _hundreds[hundreds] + convert_less_than_thousand(less_than_hundred)

def get_scale(number, scale_index):
    if scale_index == 0:
        return ""
    elif number == 1:
        return _scales[scale_index][0] 
    elif 1 < number < 20:
        return _scales[scale_index][1]
    else:
        return _scales[scale_index][2]

def convert_fraction(numerator, denominator):
    if numerator == 1:
        return _fractions[denominator]
    else:
        return convert(numerator) + " " + _fractions[denominator]

def convert(number):
    if isinstance(number, float):
        integer_part = int(number)
        fraction_part = round(number - integer_part, 10)

        integer_words = convert(integer_part)
        fraction_words = convert_fraction(int(fraction_part * 10), 10)

        return f"{integer_words} მთელი და {fraction_words}"

    if number == 0:
        return "ნული"

    if number < 0:
        return "მინუს " + convert(-number)

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