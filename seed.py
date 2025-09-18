import os
import django
import random
from decimal import Decimal
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_rest.settings")
django.setup()

from books.models import Author, Publisher, Book, BookAuthor

fake = Faker()


def run(authors_count=20, publishers_count=5, books_count=50):
    print("Seeding database...")

    # --- Authors ---
    authors = []
    for _ in range(authors_count):
        author = Author.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            birth_date=fake.date_of_birth(minimum_age=25, maximum_age=80),
            biography=fake.paragraph(nb_sentences=5),
        )
        authors.append(author)
    print(f"Created {len(authors)} authors")

    # --- Publishers ---
    publishers = []
    for _ in range(publishers_count):
        publisher = Publisher.objects.create(
            name=fake.company(),
            established_date=fake.date_between(start_date="-120y", end_date="-1y"),
            website=fake.url(),
        )
        publishers.append(publisher)
    print(f"Created {len(publishers)} publishers")

    # --- Books ---
    books = []
    for _ in range(books_count):
        price = Decimal(random.randint(5, 100))
        discounted_price = price if random.random() < 0.7 else price - Decimal(random.randint(1, 4))

        book = Book.objects.create(
            title=fake.sentence(nb_words=4),
            subtitle=fake.sentence(nb_words=6),
            publisher=random.choice(publishers),
            published_date=fake.date_between(start_date="-30y", end_date="today"),
            isbn=fake.isbn13(separator=""),
            price=price,
            discounted_price=discounted_price,
            is_bestseller=random.choice([True, False]),
        )
        books.append(book)
    print(f"Created {len(books)} books")

    # --- BookAuthor relations ---
    roles = list(BookAuthor.Role)
    relations_count = 0
    for book in books:
        chosen_authors = random.sample(authors, k=random.randint(1, 3))
        for order, author in enumerate(chosen_authors, start=1):
            BookAuthor.objects.create(
                book=book,
                author=author,
                role=random.choice(roles),
                order=order,
            )
            relations_count += 1

    print(f"Created {relations_count} book-author relations")
    print("Done!")


if __name__ == "__main__":
    run(authors_count=30, publishers_count=10, books_count=100)