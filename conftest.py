import pytest
from selenium import webdriver


@pytest.fixture(params=["chrome", "firefox"], scope="class")  # Will execute test with each param
def init_driver(request):
    def create_options(options):
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--start-maximized")
        options.add_argument('--headless')
        options.add_argument('window-size=2000x1200')
        return options

    if request.param == "chrome":
        options = webdriver.ChromeOptions()
        options = create_options(options)
        driver = webdriver.Chrome(executable_path=r"./chromedriver", options=options)

    if request.param == "firefox":
        options = webdriver.FirefoxOptions()
        options = create_options(options)
        driver = webdriver.Firefox(executable_path=r"./geckodriver", options=options)


    request.cls.driver = driver
    yield
    driver.close()