from myapp import create_app
from add_book import add_book_bp  # Import the blueprint
from stats import stats_bp  # Import the blueprint

app = create_app()

# Register the blueprint
app.register_blueprint(add_book_bp)
app.register_blueprint(stats_bp)

if __name__ == "__main__":
    app.run(debug=True)
