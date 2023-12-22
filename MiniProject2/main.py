import gzip
import json
import os
from collections import deque
from bottle import Bottle, HTTPError, request, run


# Print Size of Dataset
file_size = os.path.getsize('2022-08-30-papers.jsonl.gz')
print(f"Size of 2022-08-30-papers.jsonl.gz: {file_size} bytes")

# Print Number of Papers
with gzip.open('2022-08-30-papers.jsonl.gz') as f:
    papers_count = sum(1 for _ in f)
print(f"Number of papers: {papers_count}")

# Print Typical Structure of Paper
with gzip.open('2022-08-30-papers.jsonl.gz') as f:
    example_paper = json.loads(f.readline())
print("Typical structure of a paper:")
print(example_paper)


def transform_dataset(input_file, output_file):
    authors_dict = {}
    papers = []

    with gzip.open(input_file, 'rt', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line.strip())

            # Check if all required fields are present
            if 'title' in data and 'venue' in data and 'year' in data and 'authors' in data:
                # Filter out authors without authorId
                authors = [author.get('authorId') for author in data['authors'] if 'authorId' in author]

                # Check if authors list is not empty
                if authors and data['year'] is not None:
                    paper_info = {
                        'title': data['title'],
                        'venue': data['venue'],
                        'year': int(data['year']),
                        'authors': authors
                    }

                    papers.append(paper_info)

                    # Update authors_dict
                    for author_id in authors:
                        if author_id not in authors_dict:
                            authors_dict[author_id] = {'name': None, 'publications': []}

                        # Save publication ID instead of index
                        authors_dict[author_id]['publications'].append(paper_info)

    # Save the transformed dataset into a file
    with gzip.open(output_file, 'wt', encoding='utf-8') as out_file:
        for paper in papers:
            out_file.write(json.dumps(paper) + '\n')

    return papers, authors_dict


# Use the function
input_file = '2022-08-30-papers.jsonl.gz'
output_file = 'papers.jsonl.gz'
papers, authors_dict = transform_dataset(input_file, output_file)

# Load the JSON file into a dictionary
json_file_path = 'authors_dict.json'
with open(json_file_path, 'r') as file:
    authors_dict = json.load(file)

# Print Size of new Papers file
file_size = os.path.getsize('papers.jsonl.gz')
print(f"Size of papers.jsonl.gz: {file_size} bytes")

# Print Number of Publications in new file
with gzip.open('papers.jsonl.gz') as f:
    publications_count = sum(1 for _ in f)
print(f"Number of publications: {publications_count}")


# Search author function
def search_author(name):
    if name is None:
        return []
    matching_authors = [
        author_id
        for author_id, info in authors_dict.items()
        if info['name'] and name in info['name']
    ]
    return matching_authors

# Get paper function by publication ID
def get_paper(publication_id):
    for paper in papers:
        if paper.get('id') == publication_id:
            return paper
    return None

# Get author papers function by author ID
def get_author_papers(author_id):
    if author_id in authors_dict:
        publications_indices = authors_dict[author_id]['publications']
        author_publications = [papers[i] for i in publications_indices]
        return author_publications
    else:
        return None


# -------- API ----------
app = Bottle()


# Route to get a publication by ID
@app.route('/publications/<id:int>')
def get_publication(id):
    try:
        paper = get_paper(id)
        if paper:
            return paper
        else:
            raise HTTPError(404, "Publication not found")
    except Exception as e:
        raise HTTPError(500, f"Internal Server Error: {str(e)}")


# Route to get a list of publications with optional limit, start, and count parameters
@app.route('/publications')
def get_publications():
    try:
        limit = min(int(request.query.limit or 100), 100)
        start = int(request.query.start or 0)
        count = int(request.query.count or 100)

        publications = []
        with gzip.open('papers.jsonl.gz') as f:
            for line_number, line in enumerate(f, start=1):
                if start < line_number <= start + count:
                    publications.append(json.loads(line))

        return publications[:limit]
    except Exception as e:
        raise HTTPError(500, f"Internal Server Error: {str(e)}")


# Route to get author information by author_id
@app.route('/authors/<author_id:int>')
def get_author_info(author_id):
    try:
        author_info = authors_dict[{author_id}]
        if not author_info:
            raise HTTPError(404, "Author not found")

        coauthor_count = sum(
            1 for author in authors_dict.values() if author_id != author and author_id in author['publications'])

        return {
            'name': author_info.get('name', ''),
            'coauthored_publications': coauthor_count,
            'coauthor_count': len(author_info.get('publications', []))
        }
    except Exception as e:
        raise HTTPError(500, f"Internal Server Error: {str(e)}")


# Route to get a list of publications by author_id
@app.route('/authors/<author_id:int>/publications')
def get_author_publications(author_id):
    try:
        publications = get_author_papers(author_id)
        return publications
    except Exception as e:
        raise HTTPError(500, f"Internal Server Error: {str(e)}")


# Route to get co-authors by author_id
@app.route('/authors/<author_id:int>/coauthors')
def get_coauthors(author_id):
    try:
        coauthors = []

        for other_author_id, info in authors_dict.items():
            if other_author_id != author_id and author_id in info['publications']:
                coauthors.append({
                    'author_id': other_author_id,
                    'name': info.get('name', '')
                })

        return coauthors
    except Exception as e:
        raise HTTPError(500, f"Internal Server Error: {str(e)}")


# Route to search authors by name
@app.route('/search/authors/<search_string>')
def search_authors(search_string):
    try:
        result = search_author(search_string)
        return result[:100]
    except Exception as e:
        raise HTTPError(500, f"Internal Server Error: {str(e)}")


# Route to search publications by title with optional filter and order
@app.route('/search/publications/<search_string>')
def search_publications(search_string):
    try:
        filter_params = request.query.filter.split(',') if 'filter' in request.query else []
        order_by = request.query.order or None

        publications = []
        with gzip.open('papers.jsonl.gz') as f:
            for line_number, line in enumerate(f, start=1):
                paper = json.loads(line)
                if search_string.lower() in paper['title'].lower() and all(
                        key in paper and paper[key].lower() == value.lower() for key, value in
                        (param.split(':') for param in filter_params)):
                    publications.append(paper)

        if order_by:
            publications = sorted(publications, key=lambda x: x.get(order_by, ''))

        return publications[:100]
    except Exception as e:
        raise HTTPError(500, f"Internal Server Error: {str(e)}")


# Route to get collaboration distance between two authors
def calculate_collaboration_distance(id_origin, id_destination):
    if id_origin not in authors_dict or id_destination not in authors_dict:
        return None, None  # One or both authors not found

    if id_origin == id_destination:
        return 0, [id_origin]  # Same author, distance is 0 - as stated in the exercise

    visited = set()
    queue = deque([(id_origin, [id_origin])])

    while queue:
        current_author, path = queue.popleft()
        visited.add(current_author)

        for coauthor in authors_dict[current_author]['publications']:
            if coauthor not in visited:
                if coauthor == id_destination:
                    return len(path) - 1, path + [id_destination]  # Found the destination
                queue.append((coauthor, path + [coauthor]))

    return None, None  # No path found


# Route to search distance between authors
@app.route('/authors/<id_origin:int>/distance/<id_destination:int>')
def get_collaboration_distance(id_origin, id_destination):
    try:
        distance, shortest_path = calculate_collaboration_distance(id_origin, id_destination)

        if distance is not None:
            return {
                'distance': distance,
                'shortest_path': shortest_path
            }
        else:
            raise HTTPError(404, "Authors not found or no collaboration path")
    except Exception as e:
        raise HTTPError(500, f"Internal Server Error: {str(e)}")


# Call main and run the app in localhost port 8080
if __name__ == '__main__':
    run(app, host='localhost', port=8080)
