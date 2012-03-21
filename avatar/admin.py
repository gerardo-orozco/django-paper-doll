from django.contrib import admin
from avatar.models import Category, Part, Avatar


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('display', 'layer_index', 'thumbnail_img')

    def thumbnail_img(self, obj):
        if obj.thumbnail:
            return "<img src='%s'/>" % obj.thumbnail.url
    thumbnail_img.short_description = "Thumbnail"
    thumbnail_img.allow_tags = True


class PartAdmin(admin.ModelAdmin):
    list_display = ('display', 'label', 'category', 'image_img', 'thumbnail_img')
    list_filter = ('category',)

    def image_img(self, obj):
        if obj.image:
            return "<img src='%s'/>" % obj.image.url
    image_img.short_description = "Image"
    image_img.allow_tags = True

    def thumbnail_img(self, obj):
        if obj.thumbnail:
            return "<img src='%s'/>" % obj.thumbnail.url
    thumbnail_img.short_description = "Thumbnail"
    thumbnail_img.allow_tags = True


class AvatarAdmin(admin.ModelAdmin):
    list_display = ('image_img',)

    def image_img(self, obj):
        if obj.image:
            return "<img src='%s'/>" % obj.image.url
    image_img.short_description = "Image"
    image_img.allow_tags = True


admin.site.register(Category, CategoryAdmin)
admin.site.register(Part, PartAdmin)
admin.site.register(Avatar, AvatarAdmin)
