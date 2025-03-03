import re
from abc import ABC, abstractmethod

# Базовый класс для текстовых элементов (Паттерн Компоновщик)
class TextComponent(ABC):
    @abstractmethod
    def get_text(self) -> str:
        pass

# Класс для символа
class Symbol(TextComponent):
    def __init__(self, char: str):
        self._char = char  # инкапсуляция: символ хранится в приватном атрибуте

    def get_text(self) -> str:
        return self._char

    def __str__(self):
        return self.get_text()

# Класс для знака препинания, наследуется от Symbol
class Punctuation(Symbol):
    def __init__(self, char: str):
        # Можно добавить дополнительные проверки, является ли символ знаком препинания
        super().__init__(char)

# Класс для слова, состоит из символов
class Word(TextComponent):
    def __init__(self, word: str):
        # Приводим слово к нижнему регистру для нечувствительности к регистру
        self._word = word.lower()
        # Создаём список объектов Symbol для каждого символа
        self._symbols = [Symbol(ch) for ch in self._word]

    def get_text(self) -> str:
        return ''.join(symbol.get_text() for symbol in self._symbols)

    def __str__(self):
        return self.get_text()

    @property
    def text(self):
        return self._word

# Класс для предложения, состоит из слов и знаков препинания
class Sentence(TextComponent):
    def __init__(self, sentence_str: str):
        # Удаляем табуляции и заменяем множественные пробелы на один
        cleaned = re.sub(r'\s+', ' ', sentence_str.strip())
        self._raw_text = cleaned
        # Разбиваем предложение на слова, игнорируя знаки препинания
        self._words = [Word(word) for word in re.findall(r'\w+', cleaned)]
    
    def get_text(self) -> str:
        return self._raw_text

    def __str__(self):
        return self.get_text()

    def count_word_occurrence(self, target: str) -> int:
        target = target.lower()
        return sum(1 for word in self._words if word.text == target)

    @property
    def words(self):
        return self._words

# Класс для целого текста, состоит из предложений
class Text(TextComponent):
    def __init__(self, text_str: str):
        # Заменяем табуляции и последовательности пробелов одним пробелом
        cleaned = re.sub(r'\s+', ' ', text_str.strip())
        self._raw_text = cleaned
        # Разбиваем текст на предложения по знакам . ! ? 
        # (учтите, что для более сложного разбора можно использовать nltk.tokenize)
        sentence_strings = [s.strip() for s in re.split(r'[.?!]', cleaned) if s.strip()]
        self._sentences = [Sentence(s) for s in sentence_strings]

    def get_text(self) -> str:
        return self._raw_text

    def __str__(self):
        return self.get_text()

    @property
    def sentences(self):
        return self._sentences

    def total_occurrence(self, target: str) -> int:
        return sum(sentence.count_word_occurrence(target) for sentence in self._sentences)

# Функция для обработки текста и подсчёта вхождений заданных слов
def process_text(text_str: str, words_to_find: list):
    text_obj = Text(text_str)
    results = {}
    for word in words_to_find:
        per_sentence = [sentence.count_word_occurrence(word) for sentence in text_obj.sentences]
        total = sum(per_sentence)
        results[word] = {"total": total, "per_sentence": per_sentence}
    
    # Сортировка слов по убыванию общего количества вхождений
    sorted_results = sorted(results.items(), key=lambda item: item[1]['total'], reverse=True)
    return sorted_results

# Пример использования в консольном приложении
def main():
    # Здесь можно загрузить параметры из файла, например, имя файла с текстом и список слов
    # Для демонстрации используем захардкоженный текст и список слов
    sample_text = (
        "Python – мощный язык программирования. "
        "Программирование на Python легко и весело! "
        "Изучение Python помогает понять основы программирования."
    )
    # Список слов для поиска (без учёта регистра)
    words_list = ["python", "программирования", "легко", "основы"]

    # Обработка текста
    results = process_text(sample_text, words_list)
    
    # Вывод результатов
    print("Результаты поиска:")
    for word, data in results:
        print(f"Слово: '{word}' | Общее количество: {data['total']} | По предложениям: {data['per_sentence']}")

if __name__ == '__main__':
    main()
