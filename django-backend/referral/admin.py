from django.contrib import admin
from .models import (Page, Referrer)

class PageAdmin(admin.ModelAdmin):
	readonly_fields=('created_at', 'last_modified')

class ReferrerAdmin(admin.ModelAdmin):
	readonly_fields=('created_at', 'last_modified')

# Register your models here.
admin.site.register(Page, PageAdmin)
admin.site.register(Referrer, ReferrerAdmin)