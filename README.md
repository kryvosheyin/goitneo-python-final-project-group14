# goitneo-python-final-project-group14


<h3>Requirements:</h3>
Bot requires external libraries:
<table>
  <tr>
    <th>Dependency name</th>
    <th>Installation</th>
    <th>Reference</th>
  </tr>
    <tr>
    <th>rich</th>
    <th><b>pip install rich</b></th>
    <th><a href="https://rich.readthedocs.io/en/stable/index.html">reference</a></th>
  </tr>
</table>

To install all required dependencies please run <b>pip install -r requirements.txt</b>

# Персональний помічник

Цей проект - Персональний помічник, створений для зберігання та взаємодії з записами адресної книги та нотатками.

## Основні можливості:

1. Зберігання контактів з іменами, адресами, номерами телефонів, електронною поштою та днями народження до книги контактів.
2. Виведення списку контактів, у яких день народження через задану кількість днів від поточної дати.
3. Перевірка правильності введеного номера телефону та електронної пошти під час створення або редагування запису та повідомлення користувача у разі некоректного введення.
4. Здійснення пошуку контактів серед контактів книги.
5. Редагування та видалення записів з книги контактів.
6. Зберігання нотаток з текстовою інформацією.
7. Проведення пошуку за нотатками.
8. Редагування та видалення нотаток.

## Встановлення:

1. Клонуйте репозиторій на свій комп'ютер:

   ```bash
   git clone https://github.com/kryvosheyin/goitneo-python-final-project-group14.git

Встановіть необхідні залежності:
pip install -r requirements.txt

## Використання:
Запустіть програму:
python main.py

Дотримуйтесь інструкцій, що виводяться на екрані, щоб користуватися Персональним помічником:

Available commands:
Exit - 'close' or 'exit'
Start work - 'hello'
Add new contact - 'add' <name without spaces> <phone>
Add new phone - 'add-phone' <name without spaces> <phone1>,<phone2>,...
Remove phone - 'remove-phone' <name without spaces> <phone>
Edit phone - 'edit' <name without spaces> phone <phone to replace> <new phone>
Edit/add email - 'edit' <name without spaces> email <new email>
Edit/add birthday - 'edit' <name without spaces> birthday <date in format DD.MM.YYYY>
Edit name - 'edit' <name without spaces> name <new name>
Get all phones for contact - 'get-phone' <name without spaces>
Find contacts by value - 'find' <value containing in any field>
Remove email - 'remove-email' <name without spaces>
Get Birthday of contact - 'show-birthday' <name without spaces>
Get list of contacts to be congratulated next week - 'birthdays'
Remove contact - 'remove' <name without spaces>
Add address - 'add-address' <name without spaces> <address>
Print all contacts - 'all'

##  Внесок:
Якщо у вас є ідеї для покращення цього проекту, будь ласка, внесіть свій внесок. Ми відкриті до пул-запитів.
