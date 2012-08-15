from paper_doll.models import Part
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, get_object_or_404


@staff_member_required
def set_default_part(request, id):
    part = get_object_or_404(Part, pk=id)
    part.set_as_default()
    return redirect(request.META.get('HTTP_REFERER') or 'admin:index')
