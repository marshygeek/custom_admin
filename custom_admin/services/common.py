from django.shortcuts import render


def render_error_page(request, msg):
    return render(request, 'custom_admin/error_page.html', {'msg': msg})
