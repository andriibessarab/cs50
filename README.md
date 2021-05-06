# Project 1

Web Programming with Python and JavaScript

home: Home has two different web pages. One shows when user is not logged in. It just says "Let's get started!" And has two buttons "Log In" and "Register". And the other home says "Hello, (your username)!" It has button "Log Out". And has a search bar, where you can type ISBN or title or author of any book.

search: After you typed in a search bar something and submit the form, it's going to show you all of the relevant results on this page. It shows title and author of all the relevant books. It also has a button "Open", which is going to open a book page of a book that you chose.

book page: It has all the information about a specific book. It has its title, author, year of publication and ISBN. It also has the rating from my website and GoodReads. In addition to this, you can also leave a review about this book. And see all of the reviews submitted by other users.

register: This is just a form where you can register. You need to provide it with the username and password. By the way, there are some restrictions there, that are described below the form.

login: This is also a form where you can log in to already existing account.

API: By going to the following URL "/api/(ISBN OF A BOOK)", you will see a JSON file. Which has all required information to use it as an API. If you'll type wrong ISBN it will show you an error. If you'll type correct ISBN, but we don't have any reviews about this book, it will show you an error as well.