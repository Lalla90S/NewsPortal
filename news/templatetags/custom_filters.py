from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def censor(value):
    """
    Фильтр для цензурирования нежелательных слов.
    Заменяет все буквы кроме первой на '*' в запрещенных словах.
    """
    # Список нежелательных слов (можно расширить)
    bad_words = ['редиска', 'хрен', 'дурак']

    result = value

    for word in bad_words:
        # Заменяем слово в любом регистре
        if word in result.lower():
            # Находим позицию слова
            start = result.lower().find(word)
            # Заменяем все буквы кроме первой на '*'
            censored_word = word[0] + '*' * (len(word) - 1)
            # Заменяем в оригинальной строке с сохранением регистра
            original_word = result[start:start + len(word)]
            censored_word_with_case = original_word[0] + '*' * (len(original_word) - 1)
            result = result.replace(original_word, censored_word_with_case)

    return result