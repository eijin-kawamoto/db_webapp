from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import pytz

app = Flask(__name__)

DATABASE = 'expenses.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name text not null,
                amount real not null,
                category text,
                date text default CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    selected_date = request.args.get('date')

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        if selected_date:
            cursor.execute('''
                select date, id, name, amount, category
                from expenses
                where date(date) = ?
                order by date DESC, id ASC
            ''', (selected_date,))
        else:
            cursor.execute('''
                select date, id, name, amount, category 
                from expenses
                order by date DESC, id ASC
            ''')
        all_expenses = cursor.fetchall()

        if selected_date:
            cursor.execute('select sum(amount) from expenses where date(date) = ?', (selected_date,))
        else:
            cursor.execute('select sum(amount) from expenses')
        total_amount = cursor.fetchone()[0] or 0

    
    expenses_by_date = {}
    for expense in all_expenses:
        date, expense_id, name, amount, category = expense

        utc_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        utc_date = pytz.utc.localize(utc_date)
        japan = pytz.timezone('Asia/Tokyo')
        jp_date = utc_date.astimezone(japan).strftime('%Y-%m-%d %H:%M')

        if jp_date not in expenses_by_date:
            expenses_by_date[jp_date] = []
        expenses_by_date[jp_date].append({
            'id': expense_id,
            'name': name,
            'amount': float(amount),
            'category': category
        })

    return render_template('index.html', expenses_by_date=expenses_by_date, 
                           total_amount=total_amount, selected_date=selected_date)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    amount = request.form.get('amount', type=int)
    category = request.form.get('category', default="その他")

    if not name or not amount:
        return redirect(url_for('index'))

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            insert into expenses (name, amount, category) 
            values (?, ?, ?)
        ''', (name, amount, category))
        conn.commit()
    
    return redirect(url_for('index'))

@app.route('/delete/<int:expense_id>')
def delete(expense_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('delete from expenses where id = ?', (expense_id,))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/analysis')
def analysis():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        cursor.execute('''
            select date(date) as day, sum(amount) as total
            from expenses
            group by day
            order by day
        ''')
        daily_data = cursor.fetchall()

        cursor.execute('''
            select category, sum(amount) as total
            from expenses
            group by category
            order by total DESC
        ''')
        category_data = cursor.fetchall()

    return render_template('analysis.html', 
                           daily_data=daily_data, 
                           category_data=category_data)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
