import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO deals (place, category, dates, title, notes) VALUES (?, ?, ?, ?, ?)",
            ("Larry's Dawg House", "food", "Wednesday", "Weenie Wednesday", "$1.29 regular hot dogs")
            )

cur.execute("INSERT INTO deals (place, category, dates, title, notes) VALUES (?, ?, ?, ?, ?)",
            ('Qdoba', "food", 'Wednesday', 'Wednesday Night Special', '$6.99 burrito meal')
            )

cur.execute("INSERT INTO deals (place, category, dates, title, notes) VALUES (?, ?, ?, ?, ?)",
            ("Tim Horton's", "drink", 'Daily', '$2 Iced Lattes', '$2 any sized iced latte after 4pm')
            )

cur.execute("INSERT INTO deals (place, category, dates, title, notes) VALUES (?, ?, ?, ?, ?)",
            ("Broney's", "food", 'Friday', 'Half Apps Friday', r"50% off all appetizers")
            )

cur.execute("INSERT INTO deals (place, category, dates, title, notes) VALUES (?, ?, ?, ?, ?)",
            ('Pigskin', "food", 'Tuesday', 'Burger Tuesday', '$8 burgers')
            )

cur.execute("INSERT INTO deals (place, category, dates, title, notes) VALUES (?, ?, ?, ?, ?)",
            ('Pigskin', "food", 'Thursday', 'Boneless Wing Night', '$5.99 1lbs boneless wings')
            )

cur.execute("INSERT INTO deals (place, category, dates, title, notes) VALUES (?, ?, ?, ?, ?)",
            ('Mac Shack', "food", 'Monday', 'Half Priced Mac Monday', r'50% off large mac')
            )

cur.execute("INSERT INTO deals (place, category, dates, title, notes) VALUES (?, ?, ?, ?, ?)",
            ('Buffalo Wild Wings', "food", 'Tuesday', 'Traditional Wing Night', r'50% off traditional wings')
            )

cur.execute("INSERT INTO deals (place, category, dates, title, notes) VALUES (?, ?, ?, ?, ?)",
            ('Buffalo Wild Wings', "food", 'Thursday', 'Boneless Wing Night', r'50% off boneless wings')
            )

cur.execute("INSERT INTO deals (place, category, dates, title, notes) VALUES (?, ?, ?, ?, ?)",
            ("Lucky's Sports Tavern", "drink", 'Wednesday', 'Liquor Pitchers', '$5 liquor pitchers')
            )

connection.commit()
connection.close()