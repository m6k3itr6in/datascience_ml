import sqlite3
import json

conn = sqlite3.connect('database.db')
cur = conn.cursor()

query = """
    PRAGMA foreign_keys=ON;

    CREATE TABLE Тип_измерения(
        id integer primary key autoincrement,
        name text
    );

    CREATE TABLE Продукция(
        id integer primary key autoincrement,
        name text,
        price real,
        id_тип_измерения integer,
        FOREIGN KEY (id_тип_измерения) REFERENCES Тип_измерения(id)
    );

    CREATE TABLE Материалы(
        id integer primary key autoincrement,
        name text,
        id_тип_измерения integer,
        price real,
        FOREIGN KEY (id_тип_измерения) REFERENCES Тип_измерения(id)
    );

    CREATE TABLE Заказчики(
        id integer PRIMARY KEY,
        name text not null,
        inn text,
        addres text,
        phone_number text
    );

    CREATE TABLE Изготовители(
        id integer primary key autoincrement,
        name text
    );

    CREATE TABLE Заказ(
        id integer primary key autoincrement,
        id_заказчика integer,
        id_изготовителя integer,
        order_date date,
        total_sum real,
        FOREIGN KEY (id_заказчика) REFERENCES Заказчики(id),
        FOREIGN KEY (id_изготовителя) REFERENCES Изготовители(id)
    );

    CREATE TABLE Продукты_в_заказах(
        id integer primary key autoincrement,
        id_заказа integer,
        id_продукта integer,
        quantity integer,
        price real,
        FOREIGN KEY (id_заказа) REFERENCES Заказ(id),
        FOREIGN KEY (id_продукта) REFERENCES Продукция(id)
    );

    CREATE TABLE Спецификация_продукции(
        id integer primary key autoincrement,
        id_продукции integer,
        id_материала integer,
        quantity integer,
        FOREIGN KEY (id_продукции) REFERENCES Продукция(id),
        FOREIGN KEY (id_материала) REFERENCES Материалы(id)
    );

    CREATE TABLE Производство(
        id integer primary key autoincrement,
        id_продукции integer,
        date date,
        quantity integer,
        FOREIGN KEY (id_продукции) REFERENCES Продукция(id)
    );

    CREATE TABLE Расход_материала_на_производство(
        id integer primary key autoincrement,
        id_материала integer,
        id_производства integer,
        FOREIGN KEY (id_материала) REFERENCES Материалы(id),
        FOREIGN KEY (id_производства) REFERENCES Производство(id)
    );
"""

cur.executescript(query)

with open('Заказчики.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


for row in data:
    cur.execute(""" INSERT INTO Заказчики (id, name, inn, addres, phone_number)
                      VALUES (?, ?, ?, ?, ?)""", (row['id'], row['name'], row['inn'], row['addres'], row['phone']))
    
conn.commit()
conn.close()
