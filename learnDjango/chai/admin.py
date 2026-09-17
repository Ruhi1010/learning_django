from django.contrib import admin
from .models import ChaiVarity, ChaiReview, Store, ChaiCertificate, StoreReview
# Register your models here.

class ChaiReviewInline(admin.TabularInline):
    model = ChaiReview
    extra = 2
    
class ChaiVarityAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'date')
    inlines = [ChaiReviewInline]




class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    filter_horizontal = ('chai_varieties',)


class ChaiCertificateAdmin(admin.ModelAdmin):
    list_display = ('chai', 'certificate_number')
    
    
    
class StoreReviewAdmin(admin.ModelAdmin): 
    list_display = ('store', 'rating', 'review_text') 
    list_filter = ('rating', 'store') 
    search_fields = ('review_text', 'store__name')
    
    
admin.site.register(ChaiVarity, ChaiVarityAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(StoreReview, StoreReviewAdmin)
admin.site.register(ChaiCertificate, ChaiCertificateAdmin)