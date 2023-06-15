from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Book

class BookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create some sample books
        Book.objects.create(title='Book 1', author='Author 1', publication_year=2020)
        Book.objects.create(title='Book 2', author='Author 2', publication_year=2021)
        Book.objects.create(title='Book 3', author='Author 3', publication_year=2022)

    def test_list_books(self):
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Ensure all books are returned

    def test_create_book(self):
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'publication_year': 2023
        }
        response = self.client.post(reverse('book-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)  # Ensure new book is created

    def test_retrieve_book(self):
        book = Book.objects.first()
        response = self.client.get(reverse('book-retrieve', args=[book.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], book.title)
        self.assertEqual(response.data['author'], book.author)
        self.assertEqual(response.data['publication_year'], book.publication_year)

    def test_update_book(self):
        book = Book.objects.first()
        data = {
            'title': 'Updated Book',
            'author': 'Updated Author',
            'publication_year': 2024
        }
        response = self.client.put(reverse('book-update', args=[book.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, 'Updated Book')
        self.assertEqual(book.author, 'Updated Author')
        self.assertEqual(book.publication_year, 2024)

    def test_delete_book(self):
        book = Book.objects.first()
        response = self.client.delete(reverse('book-delete', args=[book.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)  # Ensure book is deleted
