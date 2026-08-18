from django.core.management.base import BaseCommand
from scheduler.models import Product

class Command(BaseCommand):
    help = 'Seeds default hair products into the database'

    def handle(self, *args, **kwargs):
        products_data = [
            {
                'name': 'HairGlow Rosemary Growth Shampoo',
                'description': 'Infused with natural rosemary, mint, and biotin, this luxury shampoo gently cleanses while stimulating the scalp, promoting thicker, stronger hair growth.',
                'price': 24.99,
                'image_path': 'images/hair_growth_shampoo.png',
                'stock': 25,
                'is_available': True
            },
            {
                'name': 'HairGlow Nourishing Argan Hair Oil',
                'description': 'A premium lightweight treatment crafted with cold-pressed Moroccan argan oil and lavender. Penetrates deep to restore shine, tame frizz, and mend split ends.',
                'price': 29.99,
                'image_path': 'images/nourishing_hair_oil.png',
                'stock': 15,
                'is_available': True
            },
            {
                'name': 'HairGlow Deep Repair Mask',
                'description': 'A rich, restorative conditioning mask that intensely hydrates, strengthens damaged hair, and improves elasticity. Formulated with hibiscus and shea butter.',
                'price': 34.99,
                'image_path': 'images/glow_hair_mask.png',
                'stock': 20,
                'is_available': True
            },
            {
                'name': 'HairGlow Ergonomic Scalp Massager',
                'description': 'A soft silicone scalp massaging brush that promotes blood circulation, exfoliates the scalp, and enhances the penetration of hair oils and shampoos.',
                'price': 14.99,
                'image_path': 'images/scalp_massager_brush.png',
                'stock': 40,
                'is_available': True
            }
        ]

        self.stdout.write('Seeding products...')

        for p_data in products_data:
            product, created = Product.objects.get_or_create(
                name=p_data['name'],
                defaults={
                    'description': p_data['description'],
                    'price': p_data['price'],
                    'image_path': p_data['image_path'],
                    'stock': p_data['stock'],
                    'is_available': p_data['is_available']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created product: {product.name}"))
            else:
                self.stdout.write(f"Product already exists: {product.name}")

        self.stdout.write(self.style.SUCCESS('Successfully seeded products!'))
