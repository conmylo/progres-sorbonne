from bottle import Bottle, run, request, template, jinja2_template
import requests

app = Bottle()

# Since the API is running at http://localhost:8080
API_BASE_URL = "http://localhost:8080"

# HTML template for the index page
index_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Web Interface</title>
</head>
<body>
    <h1>Welcome to the web interface of this application!</h1>
    <h2>Get Information about a Publication</h2>
    <form action="/get_publication_info" method="post">
        <label for="id">Publication ID:</label>
        <input type="number" id="id" name="id" required>
        <button type="submit">Get Information</button>
    </form>
    <br>
    <h2>Get Information about an Author</h2>
    <form action="/get_author_info" method="post">
        <label for="author_id">Author ID:</label>
        <input type="number" id="author_id" name="author_id" required>
        <button type="submit">Get Information</button>
    </form>
    <br>
    <h2>Get Collaboration Distance between Authors</h2>
    <form action="/get_collaboration_distance" method="post">
        <label for="author1_id">Author 1 ID:</label>
        <input type="number" id="author1_id" name="author1_id" required>
        <label for="author2_id">Author 2 ID:</label>
        <input type="number" id="author2_id" name="author2_id" required>
        <button type="submit">Get Distance</button>
    </form>
    <br><br><br>
    <h5>Designed by Konstantinos Mylonas - 21306683</h5>
</body>
</html>
"""

# HTML template for displaying publication information
publication_info_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Publication Information</title>
</head>
<body>
    <h1>Publication Information</h1>
    <p>Title: {{ publication_info.title }}</p>
    <p>Venue: {{ publication_info.venue }}</p>
    <p>Year: {{ publication_info.year }}</p>
    <p>Author IDs: {{ publication_info.authors }}</p>
    <p><a href="/">Go Back</a></p>
</body>
</html>
"""

# HTML template for displaying author information
author_info_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Author Information</title>
</head>
<body>
    <h1>Author Information</h1>
    <p>Name: {{ author_info.name }}</p>
    <p>Co-authored Publications: {{ author_info.coauthored_publications }}</p>
    <p>Co-author Count: {{ author_info.coauthor_count }}</p>
    <p><a href="/">Go Back</a></p>
</body>
</html>
"""

# HTML template for displaying collaboration distance
collaboration_distance_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Collaboration Distance</title>
</head>
<body>
    <h1>Collaboration Distance</h1>
    <p>Distance: {{ distance_info.distance }}</p>
    <p>Shortest Path: {{ distance_info.shortest_path }}</p>
    <p><a href="/">Go Back</a></p>
</body>
</html>
"""


# Route to render the index page
@app.route('/')
def index():
    return template(index_html)


# Route to handle form submission and display publication information
@app.route('/get_publication_info', method='POST')
def get_publication_info():
    publication_id = request.forms.get('id')
    # Make a request to the API to get publication information
    response = requests.get(f"{API_BASE_URL}/publications/{publication_id}")
    result = response.json()
    return jinja2_template(publication_info_html, publication_info=result)


# Route to handle form submission and display author information
@app.route('/get_author_info', method='POST')
def get_author_info():
    author_id = request.forms.get('author_id')
    # Make a request to the API to get author information
    response = requests.get(f"{API_BASE_URL}/authors/{author_id}")
    result = response.json()
    return jinja2_template(author_info_html, author_info=result)


# Route to handle form submission and display collaboration distance
@app.route('/get_collaboration_distance', method='POST')
def get_collaboration_distance():
    author1_id = request.forms.get('author1_id')
    author2_id = request.forms.get('author2_id')
    # Make a request to the API to get collaboration distance
    response = requests.get(f"{API_BASE_URL}/authors/{author1_id}/distance/{author2_id}")
    result = response.json()
    return jinja2_template(collaboration_distance_html, distance_info=result)


# Call main and run on localhost port 8081
if __name__ == '__main__':
    run(app, host='localhost', port=8081, debug=True)
