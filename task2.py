import requests
from lxml import html
import pymorphy2
import logging
import time

url = 'https://inlnk.ru/jElywR'
headers = {'user-agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'}
pattern = 'https://ru.wikipedia.org'
alpha_dict = {key : 0 for key in 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'} # словарь-алфавит
morph = pymorphy2.MorphAnalyzer()
all_animals_single = []

def upd_animal_dict(animal):
    if animal[0] == 'Ё':
        alpha_dict['Е'] += 1
    else:
        alpha_dict[animal[0]] +=1

def my_append(animal, is_unique = True):
    if is_unique:
        if animal.capitalize() not in all_animals_single:
            all_animals_single.append(animal.capitalize())
            upd_animal_dict(animal.capitalize())
    else:
        all_animals_single.append(animal.capitalize())
        upd_animal_dict(animal.capitalize())

def find_1w_nouns(animal_str): # функция для того чтобы из заголовка вытащить животное в виде одного слова
    animal = animal_str.split() # делим выражение на несколько слов
    if len(animal) == 1:
        return animal[0].capitalize() # выводим результат сразу
    else:
        if animal[-1][0].isupper(): # проверяем, с большой ли буквы последнее слово (если так, то это имя Собств., нас не интересует)
            animal.remove(animal[-1])
        nouns = []
        for word in animal:
            if morph.parse(word)[0].tag.POS == 'NOUN' and morph.parse(word)[0].tag.case != 'gent':# ищем существительные в сложном названии (> 1 слова)
                nouns.append(word)
        if len(nouns) == 1: # если в выражении посчастливилось найти единственно существительное, то выводим
            return nouns[0].capitalize()
        if len(nouns) == 0:  # в автоматизированном режиме не нашли существительные вообще - несовершенство библиотеки
            for word in animal:
                if word[-2:] in ['ая', 'ие', 'ий', 'ый', 'ой', 'ое', 'ые', 'ья']:  # вручную убираем прилагательные.
                    continue
                nouns.append(word)
        if len(nouns) == 1:
            return nouns[0].capitalize() # если в выражении посчастливилось найти единственно существительное, то выводим
        ####### для оставшихся слов
        noun, max_score = '', 0
        for word in animal:
            if morph.parse(word)[0].tag.POS == 'NOUN' and morph.parse(word)[0].score > max_score:
                noun, max_score = word, morph.parse(word)[0].score # выбор наиболее релевантного слова
        return noun

def parse(url = 'https://inlnk.ru/jElywR', simple_parsing=False, is_unique = True):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    logger = logging.getLogger()
    i = 0
    flag = True
    while flag:
        i += 1
        logger.info(f'parsing page {i}...')
        r = requests.get(url, headers)
        dom = html.fromstring(r.text)
        animals_list = dom.xpath("//div[@class='mw-category-group']/ul/li/a/@title")
        for animal in animals_list:
            if animal[0] == 'A': # Английская А. когда перешли на английскую раскладку, останавливаемся парсить
                logger.info(f'english words started, stop parsing')
                time.sleep(.3)
                flag = False
                break
            if ord(animal[-1]) >=ord('a') and ord(animal[-1]) <= ord('z'):
                continue
            if animal[-2:] == 'ии' or animal[-2:] == 'ые' or animal[-1] == 'ы' or animal[-1] == 'и':
                continue
            if '(' in animal or 'насекомые' in animal:
                continue
            if simple_parsing: # если хотим парсить не заморачиваясь с извлечением ключевого слова
                my_append(animal, is_unique)
            else:              # если хотим извлечь ключевое слово
                my_append(find_1w_nouns(animal), is_unique)
        if dom.xpath("//div/a[text()='Следующая страница']/@href"):
            url = pattern + dom.xpath("//div/a[text()='Следующая страница']/@href")[0] # ссылка на следующую страницу
        else:
            break

parse(simple_parsing=False, is_unique=True)    # парсинг с постобработкой, только уникальные животные (без повторов)
# parse(simple_parsing=False, is_unique=False) # парсинг с постобработкой, возможны повторы
# parse(simple_parsing=True)                   # простой парсинг без постобработки, просто названия всех страниц с животными

for key,value in alpha_dict.items():
    print(f'{key}: {value}')
