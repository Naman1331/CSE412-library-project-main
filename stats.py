from flask import Blueprint, render_template
import psycopg2

# Define a Blueprint for the stats functionality
stats_bp = Blueprint('stats', __name__, template_folder='templates')

def get_conn():
    """Establish and return a new database connection."""
    return psycopg2.connect(
        dsn="postgresql://cse412db_owner:2Qqcbp9CvasX@ep-quiet-star-a6r8acx0.us-west-2.aws.neon.tech/cse412db?sslmode=require"
    )

def put_conn(conn):
    """Close the database connection."""
    conn.close()

@stats_bp.route('/stats', methods=['GET'])
def show_stats():
    """Fetch and display statistics."""
    conn = get_conn()
    stats = {}
    try:
        with conn.cursor() as cur:
            # Fetch total number of authors
            cur.execute("SELECT COUNT(*) FROM Author;")
            stats['total_authors'] = cur.fetchone()[0]

            # Fetch total number of works (books)
            cur.execute("SELECT COUNT(*) FROM Work;")
            stats['total_books'] = cur.fetchone()[0]

            # Fetch total number of editions
            cur.execute("SELECT COUNT(*) FROM Edition;")
            stats['total_editions'] = cur.fetchone()[0]

            # Add more stats queries as needed...
    finally:
        put_conn(conn)

    return render_template('stats.html', stats=stats)
