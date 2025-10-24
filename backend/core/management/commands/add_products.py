from django.core.management.base import BaseCommand
from core.models import Product, Inventory
import csv
import os

class Command(BaseCommand):
    help = 'Add products to the POS system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            type=str,
            help='Path to CSV file with products (sku,name,cost_price,list_price,qty)'
        )
        parser.add_argument(
            '--interactive',
            action='store_true',
            help='Add products interactively'
        )
        parser.add_argument(
            '--sample',
            action='store_true',
            help='Add sample products for testing'
        )

    def handle(self, *args, **options):
        if options['csv']:
            self.add_from_csv(options['csv'])
        elif options['interactive']:
            self.add_interactive()
        elif options['sample']:
            self.add_sample_products()
        else:
            self.stdout.write(
                self.style.ERROR('Please specify --csv, --interactive, or --sample option')
            )

    def add_from_csv(self, csv_path):
        """Add products from CSV file"""
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'CSV file not found: {csv_path}'))
            return

        created_count = 0
        with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                sku = row.get('sku', '').strip()
                name = row.get('name', '').strip()
                cost_price = float(row.get('cost_price', 0))
                list_price = float(row.get('list_price', 0))
                qty = int(row.get('qty', 0))

                if not sku or not name:
                    self.stdout.write(self.style.WARNING(f'Skipping invalid row: {row}'))
                    continue

                if Product.objects.filter(sku=sku).exists():
                    self.stdout.write(self.style.WARNING(f'Product {sku} already exists, skipping'))
                    continue

                # Create product
                product = Product.objects.create(
                    sku=sku,
                    name=name,
                    cost_price=cost_price,
                    list_price=list_price
                )

                # Create inventory
                Inventory.objects.create(product=product, qty=qty)

                self.stdout.write(
                    self.style.SUCCESS(f'Created: {name} (SKU: {sku})')
                )
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} products from CSV')
        )

    def add_interactive(self):
        """Add products interactively"""
        self.stdout.write(self.style.SUCCESS('Adding products interactively...'))
        self.stdout.write('Press Ctrl+C to stop\n')

        try:
            while True:
                sku = input('Enter SKU: ').strip()
                if not sku:
                    break

                if Product.objects.filter(sku=sku).exists():
                    self.stdout.write(self.style.ERROR(f'Product {sku} already exists!'))
                    continue

                name = input('Enter product name: ').strip()
                if not name:
                    self.stdout.write(self.style.ERROR('Name cannot be empty'))
                    continue

                try:
                    cost_price = float(input('Enter cost price: $') or '0')
                    list_price = float(input('Enter list price: $'))
                    qty = int(input('Enter initial quantity: ') or '0')
                except ValueError:
                    self.stdout.write(self.style.ERROR('Invalid price or quantity'))
                    continue

                # Create product
                product = Product.objects.create(
                    sku=sku,
                    name=name,
                    cost_price=cost_price,
                    list_price=list_price
                )

                # Create inventory
                Inventory.objects.create(product=product, qty=qty)

                self.stdout.write(
                    self.style.SUCCESS(f'Created: {name} (SKU: {sku}) - ${list_price}')
                )
                self.stdout.write('')

        except KeyboardInterrupt:
            self.stdout.write('\nStopped by user')

    def add_sample_products(self):
        """Add sample products for testing"""
        sample_products = [
            {'sku': 'COFFEE001', 'name': 'Premium Coffee', 'cost_price': 2.50, 'list_price': 5.00, 'qty': 100},
            {'sku': 'TEA001', 'name': 'Green Tea', 'cost_price': 1.50, 'list_price': 3.00, 'qty': 75},
            {'sku': 'SNACK001', 'name': 'Chocolate Bar', 'cost_price': 1.00, 'list_price': 2.50, 'qty': 200},
            {'sku': 'WATER001', 'name': 'Bottled Water', 'cost_price': 0.50, 'list_price': 1.50, 'qty': 300},
            {'sku': 'SANDWICH001', 'name': 'Ham Sandwich', 'cost_price': 3.00, 'list_price': 7.50, 'qty': 50},
            {'sku': 'SODA001', 'name': 'Cola', 'cost_price': 0.75, 'list_price': 2.00, 'qty': 150},
            {'sku': 'CAKE001', 'name': 'Chocolate Cake Slice', 'cost_price': 2.00, 'list_price': 6.00, 'qty': 25},
            {'sku': 'JUICE001', 'name': 'Orange Juice', 'cost_price': 1.25, 'list_price': 3.50, 'qty': 80}
        ]

        created_count = 0
        for product_data in sample_products:
            if not Product.objects.filter(sku=product_data['sku']).exists():
                # Create product
                product = Product.objects.create(
                    sku=product_data['sku'],
                    name=product_data['name'],
                    cost_price=product_data['cost_price'],
                    list_price=product_data['list_price']
                )

                # Create inventory
                Inventory.objects.create(
                    product=product,
                    qty=product_data['qty']
                )

                self.stdout.write(
                    self.style.SUCCESS(f'Created: {product.name} (SKU: {product.sku})')
                )
                created_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f'Product {product_data["sku"]} already exists, skipping')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} sample products!')
        )