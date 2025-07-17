# 🧠 CLASS — CLI Assistant for Contacts & Notes

## Опис

CLASS — це зручний командний асистент для зберігання контактів, днів народження, нотаток та тегів. Підтримує підказки, пошук, красивий вивід (rich) і запуск з будь-якого місця через консольну команду classbot.

---

## 🏃‍♂️ Як встановити та запустити 🚀


Клонуй репозиторій або розпакуй архів.

Встанови в editable mode з підтримкою консолі:

bash

pip install -e .

Тепер можеш викликати бота з будь-якої директорії:

bash

classbot


## 🌈 Особливості


✅ Інтелектуальне вгадування команд (Levenshtein Match)
✅ Обробка помилок через декоратори
✅ Автоматичне збереження контактів і нотаток у файл
✅ Гарна стилізація виводу завдяки бібліотеці rich
✅ Запуск з будь-якого місця командою classbot


---

## 🗂 Структура проєкту

classbot/  
├── main.py  
├── address_book.py  
├── notebook.py  
├── guesser.py  
├── handlers.py  
├── decorators.py  
├── storage.py  
├── console.py  


---


## 📋 Основні команди

###👤 Контакти
Команда	                                Опис  
contact set John	                    Створити новий контакт John  
contact set John phone 1234567890	    Додати телефон  
contact set John email john@site.com	Додати email  
contact set John address "Kyiv"	      Додати адресу  
contact set John birthday 01.01.1990	Додати день народження  
contact get John	                    Показати контакт або знайти за ключовим словом  
contact get all	                      Показати всі контакти  
contact get birthdays	                Дні народження на наступний тиждень  
contact get birthdays 10	            Дні народження на N днів  
contact delete John	                  Видалити весь контакт  
contact delete John phone 1234567890	Видалити конкретний телефон  

###🗒️ Нотатки
Команда	                                Опис  
note set "Shopping" "Buy bread"	        Створити нотатку  
note set "Shopping" tag "food"	        Додати тег до нотатки  
note set "Shopping" content "Buy milk"	Оновити текст  
note get all	                          Всі нотатки  
note get "Shopping"	                    Показати нотатку за назвою  
note get tag "food"	                    Знайти нотатки за тегом  
note get search "milk"	                Пошук вмісту  
note delete "Shopping"	                Видалити нотатку  
note delete "Shopping" tag "food"	      Видалити тег з нотатки  

###🆘 Інше
Команда	                                Опис  
help	                                  Показати допомогу  
exit	                                  Вийти з програми збереженням  


close	                                Те саме, що й exit

