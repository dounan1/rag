
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

class URL(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    thumbnail = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<URL {self.title}>'

def get_metadata(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        print(f"Soup fetched metadata: {soup}")


        # Get title
        title = soup.title.string if soup.title else urlparse(url).netloc

        # Get description
        description = ''
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc:
            description = meta_desc.get('content', '')

        # Get thumbnail
        thumbnail = ''
        og_image = soup.find('meta', property='og:image')
        if og_image:
            thumbnail = og_image.get('content', '')

        return {
            'title': title,
            'description': description,
            'thumbnail': thumbnail
        }
    except Exception as e:
        print(f"Error fetching metadata: {e}")
        return {
            'title': urlparse(url).netloc,
            'description': '',
            'thumbnail': ''
        }

@app.route('/')
def index():
    urls = URL.query.order_by(URL.created_at.desc()).all()
    return render_template('index.html', urls=urls)

@app.route('/add', methods=['GET', 'POST'])
def add_url():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            flash('URL is required!')
            return redirect(url_for('add_url'))

        metadata = get_metadata(url)
        new_url = URL(
            title=request.form.get('title') or metadata['title'],
            url=url,
            description=request.form.get('description') or metadata['description'],
            thumbnail=metadata['thumbnail']
        )

        try:
            db.session.add(new_url)
            db.session.commit()
            flash('URL added successfully!')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding URL: {e}')
            return redirect(url_for('add_url'))

    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete_url(id):
    url = URL.query.get_or_404(id)
    try:
        db.session.delete(url)
        db.session.commit()
        flash('URL deleted successfully!')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting URL: {e}')
    return redirect(url_for('index'))

# Database initialization script
def init_db():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
