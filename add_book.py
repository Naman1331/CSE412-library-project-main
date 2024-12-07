from flask import Blueprint, render_template, request, redirect, url_for, flash

import psycopg2

def get_conn():
    """Establish and return a new database connection."""
    return psycopg2.connect(
        dsn="postgresql://cse412db_owner:2Qqcbp9CvasX@ep-quiet-star-a6r8acx0.us-west-2.aws.neon.tech/cse412db?sslmode=require"
    )

def put_conn(conn):
    """Close the database connection."""
    conn.close()


# Define a Blueprint for the add book functionality
add_book_bp = Blueprint('add_book', __name__, template_folder='templates')

@add_book_bp.route('/add_book_form', methods=['GET'])
def add_book_form():
    return render_template('add_book_form.html')

@add_book_bp.route('/add_book', methods=['POST'])
def add_book():
    # Extract data from the form
    title = request.form.get('title')
    subtitle = request.form.get('subtitle')
    author = request.form.get('author')
    publish_date = request.form.get('publish_date')
    number_of_pages = request.form.get('number_of_pages')
    isbn = request.form.get('isbn')
    description = request.form.get('description')

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # Insert work data
            cur.execute("""
                INSERT INTO Work (title, subtitle, description, first_publish_date)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (title, subtitle, description, publish_date))
            work_id = cur.fetchone()[0]

            # Insert author data
            cur.execute("""
                INSERT INTO Author (name) VALUES (%s) RETURNING id
            """, (author,))
            author_id = cur.fetchone()[0]

            # Link author to work
            cur.execute("""
                INSERT INTO Work_Authors (author_id, work_id)
                VALUES (%s, %s)
            """, (author_id, work_id))

        conn.commit()
        flash("Book added successfully!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "danger")
    finally:
        put_conn(conn)

    return redirect(url_for('add_book.add_book_form'))
