from django.contrib import admin
from .models import CompanyId

# Register your models here.

class company_IdentityInLine(admin.TabularInline):
    model = CompanyId
    admin.site.register(CompanyId)
