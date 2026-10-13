db = db.getSiblingDB("bookstore")

db.authors.drop()
let authorsData = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(authorsData)

db.books.drop()
let booksData = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(booksData)

print("--- Authors ---")
db.authors.find().forEach(printjson)
print("--- Books ---")
db.books.find().forEach(printjson)

db.books.insertMany([
  { title: "The Long Earth", published_year: 2012, author_ids: ["author_003", "author_004"] },
  { title: "Dune", published_year: 1965, author_ids: ["author_005"] }
])

db.authors.insertMany([
  {
    _id: "author_004",
    name: "Stephen Baxter",
    nationality: "British",
    bio: {
      short: "British science fiction author.",
      long: "Stephen Baxter is known for hard science fiction, including the Xeelee Sequence, and co-wrote The Long Earth series with Terry Pratchett."
    }
  },
  {
    _id: "author_005",
    name: "Frank Herbert",
    nationality: "American",
    bio: {
      short: "American science fiction author.",
      long: "Frank Herbert is best known for Dune (1965), one of the best-selling science fiction novels of all time."
    }
  }
])

print("--- Books by author_001 or author_004 ---")
db.books.find({ author_ids: { $in: ["author_001", "author_004"] } }).forEach(printjson)
