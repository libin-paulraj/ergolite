import csv
from home.models import Chairs
from django.core.files.images import ImageFile
from django.conf import settings
import os

def import_chairs_from_csv(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            image_path = os.path.join(settings.MEDIA_ROOT, row['image'])
            if not os.path.exists(image_path):
                print(f"⚠️ Image not found: {image_path}")
                continue

            with open(image_path, 'rb') as img_file:
                image_file = ImageFile(img_file, name=os.path.basename(image_path))

                chair, created = Chairs.objects.get_or_create(
                    name=row['name'],
                    defaults={
                        'description': row['description'],
                        'price': int(row['price']),
                        'category': row['category'],
                        'order': int(row['order']),
                        'image': image_file
                    }
                )
                if created:
                    print(f"✅ Created: {chair.name}")
                else:
                    print(f"ℹ️ Skipped (already exists): {chair.name}")
