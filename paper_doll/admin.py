from django.contrib import admin
from django.core.urlresolvers import reverse
from paper_doll.models import Category, Part, Avatar
from paper_doll.settings import (
    PAPER_DOLL_ADMIN_IMAGE_RATE,
    PAPER_DOLL_ADMIN_THUMB_RATE,
    PAPER_DOLL_ADMIN_PAPER_DOLL_RATE
)


class PartInline(admin.TabularInline):
    model = Part
    fields = ('label', 'display', 'image')
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = (PartInline,)
    list_display = ('display', 'layer_index', 'thumbnail_img')

    def thumbnail_img(self, obj):
        if obj.thumbnail:
            return "<img src='%s'/>" % obj.thumbnail.url
    thumbnail_img.short_description = "Thumbnail"
    thumbnail_img.allow_tags = True


class PartAdmin(admin.ModelAdmin):
    list_display = ('display', 'category', 'image_img',
                    'thumbnail_img', 'is_default', 'set_default')
    list_filter = ('category',)

    def image_img(self, obj):
        if obj.image:
            return "<img src='%s' width='%s' height='%s'>" % (
                obj.image.url,
                int(obj.image.width * PAPER_DOLL_ADMIN_IMAGE_RATE),
                int(obj.image.height * PAPER_DOLL_ADMIN_IMAGE_RATE))
    image_img.short_description = "Image"
    image_img.allow_tags = True

    def thumbnail_img(self, obj):
        if obj.thumbnail:
            return "<img src='%s' width='%s' height='%s'>" % (
                obj.image.url,
                int(obj.image.width * PAPER_DOLL_ADMIN_THUMB_RATE),
                int(obj.image.height * PAPER_DOLL_ADMIN_THUMB_RATE))
    thumbnail_img.short_description = "Thumbnail"
    thumbnail_img.allow_tags = True

    def set_default(self, obj):
        if not obj.is_default:
            return "<a href='%s' class='paper-doll-set-default'>Set as default</a>" % (
                        reverse('set_default_part', args=[obj.pk]))
        return ""
    set_default.short_description = "Actions"
    set_default.allow_tags = True


class AvatarAdmin(admin.ModelAdmin):
    fields = ('parts',)
    list_display = ('image_img',)

    def image_img(self, obj):
        if obj.image:
            return "<img src='%s' width='%s' height='%s'>" % (
                obj.image.url,
                int(obj.image.width * PAPER_DOLL_ADMIN_PAPER_DOLL_RATE),
                int(obj.image.height * PAPER_DOLL_ADMIN_PAPER_DOLL_RATE))
    image_img.short_description = "Image"
    image_img.allow_tags = True


admin.site.register(Category, CategoryAdmin)
admin.site.register(Part, PartAdmin)
admin.site.register(Avatar, AvatarAdmin)
