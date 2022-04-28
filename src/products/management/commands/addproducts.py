from pprint import pprint
import logging

from django.core.management.base import BaseCommand, CommandError
from icecream import ic

from products.etl.extract import download_data
from products.etl.transform import transform_data


# Import any models, django modules or packages here

class Command(BaseCommand):
    help = ('Download products from Open Food Facts API '
        '(command: addproducts 100 boissons 50 petit-dejeuners)')

    def add_arguments(self, parser):
        parser.add_argument('list_of_args', nargs='+')

    def _check_if_args_well_formed(self, options):

        # The last arg must not be an integer
        try:
            last_arg = int(options['list_of_args'][-1])
            print("type(last_arg): ", type(last_arg))
            raise Exception(
                    "command must be: function int str int str "
                    "(e.g.: addproducts 100 boissons 50 petit-dejeuners)")
        except Exception as e:
            if "invalid literal" in str(e):
                logging.info(
                    "The last argument of the command is probably OK (not an integer)")
            else:
                raise CommandError(str(e))

        # parse args
        for i, arg in enumerate(options['list_of_args']):

            # Get the number of products to download
            if i%2 == 0:
                try:
                    # arg must be an integer
                    arg = int(arg)
                except:
                    raise CommandError(
                        "command must be: function int str int str "
                        "(e.g.: addproducts 100 boissons 50 petit-dejeuners)")

            # Get the kind of products to download (e.g.: "pate a tartiner")
            if i%2 != 0 and not isinstance(arg, str):
                try:
                    # arg must be a string
                    arg = int(arg)
                    raise CommandError(
                        "command must be: function int str int str "
                        "(e.g.: addproducts 100 boissons 50 petit-dejeuners)")
                except:
                    pass

    def handle(self, *args, **options):

        self._check_if_args_well_formed(options)
        rought_products = []
        for i, arg in enumerate(options['list_of_args']):
            if i%2 != 0:            
                try:
                    quantity_of_products = int(options['list_of_args'][i-1])
                    keyword = arg
                    self.stdout.write(f'Downloading: {quantity_of_products} %s' % keyword)
                    rought_products += download_data(quantity_of_products, keyword)

                except Exception as e:
                    raise CommandError(str(e))

                if not rought_products:
                    self.stdout.write(
                        self.style.ERROR(
                            'No products to download for %s' % keyword))
                else:

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully downloaded "{quantity_of_products} %s"' % arg))

        print()
        print("Rought_products:")
        pprint(rought_products)


        formated_products = transform_data(rought_products)

        print("Formated products:")
        pprint(formated_products)