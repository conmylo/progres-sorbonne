import pytest
import requests

# This is the URL of the running server
BASE_URL = "http://localhost:8080"


def test_get_publication():
    response = requests.get(f"{BASE_URL}/publications/1")
    assert response.status_code == 200
    assert 'title' in response.json()
    assert 'venue' in response.json()


def test_get_publications():
    response = requests.get(f"{BASE_URL}/publications")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_author_info():
    response = requests.get(f"{BASE_URL}/authors/1")
    assert response.status_code == 200
    assert 'name' in response.json()
    assert 'coauthored_publications' in response.json()
    assert 'coauthor_count' in response.json()


def test_get_author_publications():
    response = requests.get(f"{BASE_URL}/authors/1/publications")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_coauthors():
    response = requests.get(f"{BASE_URL}/authors/1/coauthors")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_search_authors():
    response = requests.get(f"{BASE_URL}/search/authors/John")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_search_publications():
    response = requests.get(f"{BASE_URL}/search/publications/robot")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_collaboration_distance():
    response = requests.get(f"{BASE_URL}/authors/1/distance/2")
    assert response.status_code == 200
    assert 'distance' in response.json()
    assert 'shortest_path' in response.json()

# Use pytest test.py in terminal to use these unit tests
