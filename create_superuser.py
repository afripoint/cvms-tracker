import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "app.settings"
)  # Replace 'your_project' with your project name
django.setup()

User = get_user_model()

# username = os.getenv("DJANGO_SUPERUSER_USERNAME", "afripoint")
username = os.getenv("DJANGO_SUPERUSER_USERNAME", "afriuser")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "afri2024")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password)
    print(f"Superuser {username} created.")
else:
    print(f"Superuser {username} already exists.")
