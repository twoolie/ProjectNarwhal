from django.conf import settings

CATEGORY_NAME = getattr(settings, "MOVIE_CATEGORY_NAME", 'Movies')