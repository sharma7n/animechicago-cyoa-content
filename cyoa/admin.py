from django.contrib import admin

from .models import Question, Source, Recommendation, Choice

for model in [Question, Source, Recommendation, Choice]:
    admin.site.register(model)