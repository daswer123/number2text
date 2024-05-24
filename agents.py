import time
from openai import OpenAI
import os
import shutil
import random
import datetime
import json

# OpenAI

# Rate limiting variables
MAX_REQUESTS_PER_MINUTE = 5
request_timestamps = []

def is_rate_limited():
    global request_timestamps
    current_time = time.time()

    # Remove timestamps older than 1 minute
    request_timestamps = [timestamp for timestamp in request_timestamps if current_time - timestamp <= 60]

    if len(request_timestamps) >= MAX_REQUESTS_PER_MINUTE:
        return True

    request_timestamps.append(current_time)
    return False

# OpenAI
def request_openai(messages):
    while is_rate_limited():
        print("[Лог] Превышенно кол-во запросов, повторный запрос через 5 секунд...")
        time.sleep(5)

    client = OpenAI(
        api_key="-",
        base_url="-"
    )

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="claude-3-opus-20240229",
        max_tokens=4000,
        temperature=0.4
    )

    return chat_completion.choices[0].message.content

langs = [
    "en", "es", "fr",
    "ar", "bn", "ru", "pt", "id",
    "ur", "ja", "de", "ko", "vi",
    "ta", "it", "tr", "pl", "uk",
    "fa", "ro", "nl", "yo", "th",
    "sw", "az", "ps", "ha", "am",
    "jv", "hu", "uz", "ig", "si",
    "my", "su", "mg", "kk", "te",
    "ml", "or", "gu", "cs", "kn",
    "ne", "pa", "so", "mr", "km",
    "lo", "ckb", "ceb", "sk", "ny",
    "be", "el", "ka", "sd", "ky",
    "tg", "co", "tk", "hr", "mn",
    "bs", "sr", "sq", "hy", "lt",
    "nn", "mt", "gl", "da", "sl",
    "ug", "tl", "he", "fil", "fi",
    "et", "lv", "sv", "nb", "mk",
    "eo", "ku", "af", "is", "ms",
    "eu", "ca", "ga", "cy", "fy"
]

def log_prompt(agent, prompt, response):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - Agent {agent}:\nPrompt: {prompt}\nResponse: {response}\n\n"
    with open("number2text/prompt_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

def create_temp_file(lang_code, code, timestamp):
    os.makedirs("number2text/temp", exist_ok=True)
    with open(f"number2text/temp/{lang_code}_{timestamp}.py", "w", encoding="utf-8") as f:
        f.write(code)

def move_file_to_lang_dir(lang_code, timestamp):
    os.makedirs("number2text/lang", exist_ok=True)
    shutil.move(f"number2text/temp/{lang_code}_{timestamp}.py", f"number2text/lang/{lang_code}.py")

def move_file_to_check_dir(lang_code, timestamp):
    os.makedirs("number2text/check_language", exist_ok=True)
    shutil.move(f"number2text/temp/{lang_code}_{timestamp}.py", f"number2text/check_language/{lang_code}.py")

def generate_test_code(lang_code, timestamp):
    test_cases = [random.randint(0, 100) for _ in range(10)]
    test_cases += [random.randint(100, 10000) for _ in range(10)]
    test_cases += [random.randint(1, 20) for _ in range(10)]
    test_cases += [random.randint(10000, 1000000000) for _ in range(10)]
    # Add test cases for negative numbers
    test_cases += [-random.randint(0, 100) for _ in range(10)]

    test_code = f"""
import json
from number2text.temp.{lang_code}_{timestamp} import convert

test_cases = {test_cases}
results = []

for case in test_cases:
    try:
        result = convert(case)
        results.append({{
            "input": case,
            "output": result
        }})
    except Exception as e:
        results.append({{
            "input": case,
            "output": str(e)
        }})

with open("number2text/temp/{lang_code}_{timestamp}_test_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)
"""
    return test_code

def evaluate_test_results(lang_code, timestamp):
    with open(f"number2text/temp/{lang_code}_{timestamp}_test_results.json", "r", encoding="utf-8") as f:
        test_results = json.load(f)

    agent2_prompt = f"""
    Instructions for Agent 2:
    1. Review the test results for the language module "{lang_code}_{timestamp}.py":
       Test results:
       {json.dumps(test_results, ensure_ascii=False, indent=4)}
    2. Evaluate the correctness of the number-to-text conversion functionality on a scale of 1 to 10.
    3. If the score is 9 or above, respond with the score on the first line.
    4. If the score is below 9, respond with the score on the first line, followed by a detailed analysis of the specific errors, suggestions for improvement, and any other relevant feedback starting from the second line.
    """
    agent2_response = request_openai([
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": agent2_prompt},
    ])
    agent2_response_lines = agent2_response.strip().split("\n", 1)
    quality_score = int(agent2_response_lines[0].strip())
    improvement_note = agent2_response_lines[1].strip() if len(agent2_response_lines) > 1 else ""

    log_prompt(2, agent2_prompt, agent2_response)

    if quality_score >= 9:
        return True, quality_score, improvement_note
    else:
        with open(f"number2text/temp/{lang_code}_{timestamp}_improve_note.json", "w", encoding="utf-8") as f:
            json.dump(improvement_note, f, ensure_ascii=False, indent=4)
        return False, quality_score, improvement_note

def fix_code(lang_code, timestamp, test_results, improvement_note):
    agent3_prompt = f"""
    Instructions for Agent 3:
    1. The language module "{lang_code}_{timestamp}.py" has failed the tests.
    2. Review the current language module code, test results, and the improvement note:
       Language module code:
       {open(f"number2text/temp/{lang_code}_{timestamp}.py", "r", encoding="utf-8").read()}

       Test results:
       {json.dumps(test_results, ensure_ascii=False, indent=4)}

       Improvement note:
       {improvement_note}
    3. Based on the provided information, identify issues in the language module code and provide corrections.
    4. Take into account the peculiarity of the language and how the number is formed. It is important to keep only the numeral declaration and the output from the convert function, the rest can be changed completely so that the code can fully cover the peculiarities of the language.
    5. Return the complete code without any comments.
    """
    agent3_response = request_openai([
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": agent3_prompt},
                # {"role": "user", "content": "Be sure to fix the code where you are told and improve it so that there are no more errors"},
        {"role": "assistant", "content": "Here is the corrected code without any  comments:"}
    ])
    corrected_code = agent3_response.strip()
    new_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    create_temp_file(lang_code, corrected_code, new_timestamp)
    log_prompt(3, agent3_prompt, agent3_response)
    return new_timestamp

# Start Here
if __name__ == "__main__":
    for lang_code in langs:
        print(f"[Лог] Начинаем обработку языка: {lang_code}")

        # Проверяем, существует ли уже модуль для данного языка
        if os.path.exists(f"number2text/lang/{lang_code}.py"):
            print(f"[Лог] Модуль для языка {lang_code} уже существует. Переходим к следующему языку.")
            continue

        # Агент 1: Создание нового модуля
        print(f"[Лог] Агент 1 начинает создание модуля для языка {lang_code}")

        # Выбираем два случайных языка в качестве примеров
        example_langs = random.sample(os.listdir("number2text/lang"), 2)
        example_code = []
        for example_lang in example_langs:
            with open(f"number2text/lang/{example_lang}", "r", encoding="utf-8") as f:
                example_code.append(f.read())

        agent1_prompt = f"""
        Instructions for Agent 1:
        1. Generate new code in Python for the target language "{lang_code}", adhering to its specific rules and conventions.
        2. Use the provided code from two random existing language modules as context:
           Example 1:
           {example_code[0]}
           Example 2:
           {example_code[1]}
        3. Return the complete code starting from the `_ones` variable, without any  comments. JUST CODE, NO ANY COMMENT.
        4. These examples do not have to be a reference, you can write code to cover the peculiarities of the language. Only two things are important. It is to declare numerals at the beginning and to have a convert function that returns a string and accepts a number. The rest can be changed
        """
        agent1_response = request_openai([
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": agent1_prompt},
            {"role": "assistant", "content": "Here is the complete code starting from the `_ones` variable, without any  comments:"}
        ])
        generated_code = "_ones" + agent1_response.split("_ones", 1)[1].strip()
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        create_temp_file(lang_code, generated_code, timestamp)
        log_prompt(1, agent1_prompt, agent1_response)
        print(f"[Лог] Агент 1 успешно создал модуль для языка {lang_code}")

        max_attempts = 10
        attempt = 1

        while attempt <= max_attempts:
            print(f"[Лог] Попытка {attempt} из {max_attempts} для языка {lang_code}")

            # Генерация кода для проверки работы функции
            print(f"[Лог] Генерация кода для проверки работы функции для языка {lang_code}")
            test_code = generate_test_code(lang_code, timestamp)
            with open(f"number2text/temp/{lang_code}_{timestamp}_test.py", "w", encoding="utf-8") as f:
                f.write(test_code)
            print(f"[Лог] Код для проверки работы функции успешно сгенерирован для языка {lang_code}")

            # Запуск проверки работы функции
            print(f"[Лог] Запуск проверки работы функции для языка {lang_code}")
            exec(open(f"number2text/temp/{lang_code}_{timestamp}_test.py", "r", encoding="utf-8").read())
            print(f"[Лог] Проверка работы функции завершена для языка {lang_code}")

            # Оценка результатов проверки
            print(f"[Лог] Оценка результатов проверки для языка {lang_code}")
            test_passed, quality_score, improvement_note = evaluate_test_results(lang_code, timestamp)

            if test_passed:
                print(f"[Лог] Проверка для языка {lang_code} успешно пройдена с оценкой {quality_score}")
                move_file_to_lang_dir(lang_code, timestamp)
                break
            else:
                print(f"[Лог] Проверка для языка {lang_code} не пройдена с оценкой {quality_score}")
                print(f"[Лог] Замечания по улучшению: {improvement_note}")

                # Агент 3: Исправление ошибок
                print(f"[Лог] Агент 3 начинает исправление ошибок в модуле для языка {lang_code}")
                with open(f"number2text/temp/{lang_code}_{timestamp}_test_results.json", "r", encoding="utf-8") as f:
                    test_results = json.load(f)
                with open(f"number2text/temp/{lang_code}_{timestamp}_improve_note.json", "r", encoding="utf-8") as f:
                    improvement_note = json.load(f)
                new_timestamp = fix_code(lang_code, timestamp, test_results, improvement_note)
                print(f"[Лог] Агент 3 исправил ошибки в модуле для языка {lang_code}")
                timestamp = new_timestamp

            attempt += 1

        if attempt > max_attempts:
            print(f"[Лог] Не удалось привести код для языка {lang_code} в порядок после {max_attempts} попыток")
            move_file_to_check_dir(lang_code, timestamp)
            shutil.rmtree("number2text/temp")

    print("[Лог] Обработка всех языков завершена")
