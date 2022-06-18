import pytest


@pytest.mark.test_me
@pytest.mark.usefixtures("init_driver")
class TestBrowser:
    def test_signup(self, live_server):
        driver = self.driver
        find = driver.find_element_by_xpath

        print("Should go to home page")
        driver.get(("%s%s" % (live_server.url, "")))
        h1_content = find("//h1").text
        assert "Du gras, oui, mais de qualit" in h1_content

        print("When << s'inscrire >> is clicked should go to signup page")
        # Click on sign up link
        find("//a[contains(@href,'/accounts_signup')]").click()
        h2_content = find("//h2").text
        assert "inscrire" in h2_content

        print("If the signup form is properly filled and submitted then")
        email_field = find('//*[@id="username"]')
        email_field.send_keys("lara@croft.fr")
        password_field = find('//*[@id="password"]')
        password_field.send_keys("12345678")
        # Click on the submit button
        find('//*[@id="submitButton"]').click()

        print("     should redirect to home page")
        h1_content = find("//h1").text
        assert "Du gras, oui, mais de qualit" in h1_content

        print("     should be connected")
        link_to_logout = driver.find_element_by_xpath('//a[@id="logout"]')
        assert link_to_logout
