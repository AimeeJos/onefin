from django.contrib import admin

from movies.models import Movies, Collections

tables = (Movies, Collections)

for table in tables:
    admin.site.register(table)
    