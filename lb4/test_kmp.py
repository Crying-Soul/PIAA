# Тест 1: Текст с одним совпадением шаблона
pattern1 = "data"
text1 = "This is some sample text where the word data appears once."
expected_result1 = [37]  # Шаблон "data" встречается с индекса 37

# Тест 2: Текст с двумя совпадениями шаблона
pattern2 = "pattern"
text2 = "This text contains the word pattern twice. The pattern is what we're looking for."
expected_result2 = [28, 66]  # Шаблон "pattern" встречается на индексах 28 и 66

# Тест 3: Текст без совпадений шаблона
pattern3 = "hello"
text3 = "This is a test string without the target word."
expected_result3 = []  # Шаблон "hello" не найден

# Тест 4: Шаблон с несколькими символами, текст с одним совпадением
pattern4 = "finding"
text4 = "In this text, we are finding the word 'finding'."
expected_result4 = [26]  # Шаблон "finding" встречается с индекса 26

# Тест 5: Шаблон с несколькими символами, текст с одним совпадением в конце
pattern5 = "endend"
text5 = "This sentence ends with the word endend."
expected_result5 = [33]  # Шаблон "end" встречается с индекса 32