UNWANTED_CATEGORIES = [
    "Alimentos",
    "Aperitivos",
    "Artificially Sweetened Beverages",
    "Babeurres",
    "Bebidas",
    "Beverages",
    "Bevande",
    "Breads",
    "Breakfasts",
    "Canned",
    "Cibi ",
    "Cibo",
    "Coleslaw",
    "Common Beans",
    "Dorrobst",
    "Crisp",
    "Diet Beverages",
    "Diet Cola Soft Drink",
    "Dry ",
    "Dry Pastas",
    "Durum Wheat Pasta",
    "Farmer",
    "Fats",
    "Flavour",
    "Food",
    "Frucht",
    "Getränke",
    "Getranke",
    "Getreide",
    "Gemusebasierte",
    "Generi Alimentari",
    "Gezuckerte Getranke",
    "Gg",
    "Gluten-Free Breads",
    "Напитки",
    "Hot Beverages",
    "Instant Beverages",
    "Kaffeegetranke",
    "Knr Moul Leg Autref 2X1L",
    "Lebensmittel",
    "Legume Milks",
    "Legumes And Their Products",
    "Legume Seeds",
    "Light Margarines",
    "Mandelmilch",
    "Meals",
    "Meat Analogues",
    "Milk Substitute",
    "Mixes-Of-Squeezed-Fruit-Juices",
    "Mountain Products",
    "Mountain Waters",
    "Napoje Bezalkoholowe",
    "Nusse Und Nussprodukte",
    "Nussmilch",
    "Nuts",
    "Nuts And Their Products",
    "Продукты питания",
    "Pecan Nuts",
    "Pflanzenmilch",
    "Pflanzliche Lebensmittel",
    "Plantaardige",
    "Plant-Based Foods",
    "Plant-Based Foods And Beverages",
    "Plant-Based Meals",
    "Plant-Based Spreads",
    "Plant Milks",
    "Pomodori E Prodotti Derivati",
    "Pre-Baked Breads",
    "Products Without Gluten",
    "Red Beans",
    "Salse",
    "Salted",
    "Shelled",
    "Soy Milks",
    "Spaetzle",
    "Spreadable Fats",
    "Spreads",
    "Spring Waters",
    "Seeds",
    "Sweetened Beverages",
    "Unsweetened Beverages",
    "Unsweetened Natural Soy Milks",
    "Waters",
    "De:",
    "En:",
    "Es:",
    "Fr:",
    "It:",
    "1/2"]

NBR_OF_PAGES = 4
PAGE_NBR_FOR_EXTRACTION_FILENAME = 'page_nbr.txt'
PRODUCTS_PER_PAGE = 5  # ====== Should be reset to 50
URL_OPEN_FOOD_FACT = "https://fr.openfoodfacts.org/cgi/search.pl"
REQUIRED_FIELDS_OF_A_PRODUCT = (
    "_id,"
    "product_name_fr,"
    "quantity,"
    "brands,"
    "ingredients_text_fr,"
    "nutriscore_grade,"
    "nutriments,"
    "pnns_groups_1,"
    "image_url,"
    "stores,"
    "stores_tags,"
    "categories_old,"
    "url,"
    "lang",
    "_keywords,")
