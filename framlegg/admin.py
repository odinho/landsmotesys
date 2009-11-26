# vim: ts=4 sts=4 expandtab sw=4 fileencoding=utf8
from framlegg.models import *
from django.contrib import admin

class PatchAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'document', 'backed_by', 'line_no', 'nemnd_accepted')
    list_filter = ('document', 'backed_by', 'nemnd_accepted',)
    list_editable = ('nemnd_accepted',)
    raw_id_fields = ('document', 'nemnd_superseeding',)
    save_on_top = True
    search_fields = ('=id','what_to_change', 'backed_by',)
    fieldsets = (
        (None, {
            'fields': (('document', 'backed_by', 'line_no'),
                        ('what_to_change', 'reason'),)
        }),
        ('Nemnding', {
            'fields': ('nemnd_accepted',
                        'nemnd_desc',
                        'nemnd_superseeding',)
        }),
    )

    class Media:
        css = {"all": ("/web/admin.css",)}

    def save_model(self, request, obj, form, change):
        obj.created_by = unicode(request.user)
        obj.save()


class PatchInline(admin.StackedInline):
    model = Patch
    #fields = ('backed_by', 'line_no', 'what_to_change', 'nemnd_accepted', 'nemnd_desc', 'nemnd_superseeded_by')
    fieldsets = (
        (None, {
            'fields': (('backed_by', 'line_no'),
                        ('what_to_change', 'reason'),
                        ('nemnd_accepted', 'nemnd_superseeding',),
                        'nemnd_desc',)
        }),
    )
    extra = 10


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'category', 'num_patches', 'num_undef_patches', 'nemnd_accepted')
    exclude = ('created_by',)
    list_filter = ('category',)
    list_editable = ('nemnd_accepted',)
    save_on_top = True
    search_fields = ('=id', 'title',)
    inlines = [PatchInline,]

    class Media:
        css = {"all": ("/web/admin.css",)}

    def save_model(self, request, obj, form, change):
        obj.created_by = unicode(request.user)
        obj.save()

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'time_limit')
    date_hierarchy = 'time_limit'

admin.site.register(Document, DocumentAdmin)
admin.site.register(Patch, PatchAdmin)
admin.site.register(Category, CategoryAdmin)
