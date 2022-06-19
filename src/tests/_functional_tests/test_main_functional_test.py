import time

import pytest

from products.models import Category, Product
from accounts.models import Customer
from src.tests.products.params_for_mark_parametrize.products_objs import welformed_products
from accounts.constants import USER_LARA_CROFT


pytestmark = pytest.mark.django_db

categories_dict = {}


@pytest.fixture
def store_categories_in_db():
    # Create categories from the attribute 'categories' of each downloaded product
    # so that a product can be added to the database and get included in a stored category
    categories = set(
        category
        for product in welformed_products
        for category in product.categories)

    for category in categories:
        categories_dict[category] = Category.objects.create(name=category)

    return categories_dict


@pytest.fixture
def add_products_to_db(store_categories_in_db):
    store_categories_in_db
    Product.add_many(welformed_products)


@pytest.fixture
def remove_user_lara_croft():
    Customer.objects.filter(username="lara@croft-12345678.fr").delete()


@pytest.mark.test_me
@pytest.mark.usefixtures("init_driver")
class TestBrowser:
    def test_signup(self):
        try:
            driver = self.driver
            find = driver.find_element_by_xpath

            # Remove fake users from database
            driver.get("http://localhost:5550/accounts_delete_fake_users")

            print("No characters after the domain name should take the user to the home page")
            driver.get("http://localhost:5550")
            time.sleep(2)
            h1_content = find("//h1").text
            assert "Du gras, oui, mais de qualit" in h1_content

            print("Entering keywords in the search bar")
            field_enter_product_keywords = find("//input[@id='form1']")
            field_enter_product_keywords.send_keys("coca cola")
            # Click submit
            find("//button[@type='submit']").click()
            time.sleep(2)

            print("     should take the user to the original products page even though the "
                    "user is not logged in")
            assert ("Choisissez dans la liste ci-dessous le produit que vous voulez remplacer."
                    in driver.page_source)

            print("     so that he can select the product he wants to substitute "
                    "among a list of products")
            selected_product = find('//div[contains(text(), "original")]')
            assert selected_product

            print("Clicking on the original product")
            selected_product.click()
            time.sleep(2)

            print("     should take the user to the substitute products page")
            assert "Vous pouvez remplacer cet aliment par" in driver.page_source

            print("Clicking on a substitute product", end=" ")
            selected_product = find("//button[@class='product-as-button']")
            selected_product.click()
            time.sleep(2)

            print("should take the user to the details page of the substitute product")
            assert "nutritionnels pour 100g" in driver.page_source

            print("Clicking the button <<Voir la fiche d'OpenFoodFact>>")
            openfoodfact_btn = find("//button[@class='biscuits-as-background-for-button']")
            openfoodfact_btn.click()
            time.sleep(5)

            print("     should take the user to the details page of the substitute product "
                    "on https://fr.openfoodfacts.org/ (in a new tab)")
            driver.switch_to.window(driver.window_handles[1])  # Switch to new window
            assert "Open Food Facts" in driver.page_source
            assert "les produits alimentaires du monde entier." in driver.page_source
            time.sleep(2)
            print("Closing the new tab should take back the user to the Pure Beurre application")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])  # Switch to previous window

            print("When << s'inscrire >> is clicked should take the user to "
                    "signup page")
            # Click on sign up link
            find("//a[contains(@href,'/accounts_signup')]").click()
            time.sleep(2)
            h2_content = find("//h2").text
            assert "inscrire" in h2_content

            print("If the signup form is properly filled and submitted then")
            email_field = find('//*[@id="username"]')
            email_field.send_keys(USER_LARA_CROFT["username"])
            password_field = find('//*[@id="password"]')
            password_field.send_keys(USER_LARA_CROFT["password"])
            # Click on the submit button
            find('//*[@id="submitButton"]').click()
            time.sleep(2)

            print("     should redirect the user to home page")
            h1_content = find("//h1").text
            assert "Du gras, oui, mais de qualit" in h1_content

            print("     should connect the user. As a result, the logout "
                    "button is displayed")
            link_to_logout = driver.find_element_by_xpath('//a[@id="logout"]')
            assert link_to_logout

            print("Entering keywords in the search bar")
            field_enter_product_keywords = find("//input[@id='form1']")
            field_enter_product_keywords.send_keys("coca cola")
            # Click submit
            find("//button[@type='submit']").click()
            time.sleep(2)

            print("     should take the user to the original products page")
            assert ("Choisissez dans la liste ci-dessous le produit que vous voulez remplacer."
                    in driver.page_source)

            print("     so that he can select the product he wants to substitute "
                    "among a list of products")
            selected_product = find('//div[contains(text(), "original")]')
            assert selected_product

            print("Clicking on the original product")
            selected_product.click()
            time.sleep(2)

            print("     should take the user to the substitute products page")
            assert "Vous pouvez remplacer cet aliment par" in driver.page_source

            print("Clicking on the button 'Ajouter à mes aliments'", end=" ")
            add_to_fav_btn = find("//*[contains(text(), 'Ajouter')]")
            add_to_fav_btn.click()
            time.sleep(2)

            print("should display the message: "
                    "Ce produit a bien été enregistré dans vos aliments préférés.")
            assert "Ce produit a bien " in driver.page_source
            assert "enregistr" in driver.page_source
            assert " dans vos aliments pr" in driver.page_source

            print("Clicking on 'mes aliments' (the carrot icon)")
            favorites_link = find("//a[@id='get_fav']")
            favorites_link.click()
            time.sleep(2)

            print("     should take the user to the favorites page")
            assert "Mes aliments" in driver.page_source

            print("     should display the favorites products")
            image_of_product = find("//img[@class='image-thumb-of-product']")
            assert image_of_product

            print("Clicking on the 'logout' icon ")
            logout_link = find("//a[@id='logout']")
            logout_link.click()
            time.sleep(2)

            print("     should redirect the user to home page")
            h1_content = find("//h1").text
            assert "Du gras, oui, mais de qualit" in h1_content

            print("     should log-out the user from the app. As a result, "
                    "the login link is displayed")
            assert "inscrire" in driver.page_source

            time.sleep(2)
            # Remove fake users from database
            driver.get("http://localhost:5550/accounts_delete_fake_users")

        except Exception as e:
            driver.save_screenshot("screenshot_of fail.png")
            print("TEST FAILED! Reason: ", str(e))
