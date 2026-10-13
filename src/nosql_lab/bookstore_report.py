#!/usr/bin/env python3

import logging
import os
import sys

import pymongo
from pymongo.errors import PyMongoError

MONGODB_ATLAS_URL = os.environ.get("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.environ.get("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.environ.get("MONGODB_ATLAS_PWD")

AUTHOR_IDS = ["author_002", "author_003", "author_004"]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)


def check_environment():
    missing = [
        name
        for name, value in [
            ("MONGODB_ATLAS_URL", MONGODB_ATLAS_URL),
            ("MONGODB_ATLAS_USER", MONGODB_ATLAS_USER),
            ("MONGODB_ATLAS_PWD", MONGODB_ATLAS_PWD),
        ]
        if not value
    ]
    if missing:
        logger.error("Missing variables: %s", ", ".join(missing))
        return False
    return True


def print_author_report(authors, books, author_ids):
    total = authors.count_documents({"_id": {"$in": author_ids}})
    print(f"Authors: {total}\n")

    for author_id in author_ids:
        author = authors.find_one({"_id": author_id})
        if author is None:
            logger.warning("Author %s not found", author_id)
            continue

        print(author["name"])
        for book in books.find({"author_ids": author["_id"]}):
            print(f"  {book['title']} ({book['published_year']})")
        print()


def main():
    if not check_environment():
        sys.exit(1)

    client = None
    try:
        client = pymongo.MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
            serverSelectionTimeoutMS=5000,
        )
        # Force a round trip so connection problems surface here
        client.admin.command("ping")
        logger.info("Connected to MongoDB Atlas")

        db = client["bookstore"]
        authors = db["authors"]
        books = db["books"]

        print_author_report(authors, books, AUTHOR_IDS)
    except PyMongoError as err:
        logger.error("MongoDB error: %s", err)
        sys.exit(1)
    finally:
        # Always release the connection
        if client is not None:
            client.close()
            logger.info("Connection closed")


if __name__ == "__main__":
    main()
