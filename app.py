from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import json
import csv

app = Flask(__name__)

def get_search_results(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    for g in soup.find_all('div', class_='g'):
        title = g.find('h3')
        link = g.find('a', href=True)
        if title and link:
            results.append({'title': title.text, 'link': link['href']})

    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = get_search_results(query)
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
