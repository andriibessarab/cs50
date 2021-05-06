# Project 3

Web Programming with Python and JavaScript

unauthorized: When you visit my website for the first time, you see this page. You can open popups with registration and log in forms. After you regitered an account, you will recieve an email with your credentials. Now, you can login.

authorized: After you logged in, you will see a page with the menu, you can choose a specific item that you want to add to your cart. In some cases it will open a popup where you can add a toppings or choose the size of an item. At the top there is "cart" button. When you tap on it, it will show you a popup with all items in your cart. if you want todelete any of the items in your cart, there is a cross button next to each item. After you tap continue, it asks you to review and confirm your order. And when you submit your order, you'll receive an email with your order's details. You can logout using "log out" button.

admin: If you logged in with account of an admin, you will see all orders that are stored in the database.

django admin: There are a different models for each type of products(like subs, salads, pizzas, etc.). There is also a model, that contain all the toppings(they all available for pizzas and some of them available for specific subs). and the last model is orders model that contain all of the orders and store them as lists(with dictionaries inside).