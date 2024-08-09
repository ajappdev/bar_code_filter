# DJANGO DECLARATIONS
from django.contrib import admin

# APP DECLARATIONS
import app.models as am

# DECLARING CLASSES
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'creation', 'modification')
    list_filter = ('user', 'creation', 'modification')

class CustomUserAdmin(admin.ModelAdmin):
    pass

class LogingLogAdmin(admin.ModelAdmin):
    pass

class AccessLogAdmin(admin.ModelAdmin):
    pass

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'barcode']

admin.site.register(am.UserProfile, UserProfileAdmin)
admin.site.register(am.CustomUser, CustomUserAdmin)
admin.site.register(am.LogingLog, LogingLogAdmin)
admin.site.register(am.AccessLog, AccessLogAdmin)
admin.site.register(am.Product, ProductAdmin)

