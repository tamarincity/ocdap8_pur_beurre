# ocdap8_pur_beurre
Website that allows you to find a food equivalent to the one of your choice but of better quality.

## Adding products in the database

Open the terminal in the src folder then type:
python manage.py addproducts "quantity" "keyword" "quantity" "keyword" "quantity" "keyword" ...

E.g.:
```html
python manage.py addproducts 100 boissons 50 petits-dejeuners
```

If you want to download any type of product from Open Food Facts then type **any** or **all**.
E.g.:
```html
python manage.py addproducts 800 any
```
