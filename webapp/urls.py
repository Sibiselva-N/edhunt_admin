from django.urls import path
from .views import show_dashboard, show_category, show_service, show_banner, show_district, edit_district, add_district, \
    show_user, \
    add_service, edit_service, add_category, edit_category, delete_category, add_banner, edit_banner, delete_service, \
    delete_banner, delete_district, delete_grade, edit_grade, add_grade, show_grade, edit_user

urlpatterns = [
    path('dashboard', show_dashboard),
    path('category', show_category),
    path('category_add', add_category),
    path('category_edit', edit_category, name='category_edit'),
    path('category_delete', delete_category, name='category_delete'),
    path('service', show_service),
    path('banner', show_banner),
    path('banner_add', add_banner),
    path('banner_edit', edit_banner, name='banner_edit'),
    path('banner_delete', delete_banner, name='banner_delete'),
    path('district', show_district),
    path('district_add', add_district),
    path('district_edit', edit_district, name='district_edit'),
    path('district_delete', delete_district, name='district_delete'),

    path('grade', show_grade),
    path('grade_add', add_grade),
    path('grade_edit', edit_grade, name='grade_edit'),
    path('grade_delete', delete_grade, name='grade_delete'),

    path('users', show_user),
    path('user_edit', edit_user, name='user_edit'),
    path('service_add', add_service),
    path('service_edit', edit_service, name='service_edit'),
    path('service_delete', delete_service, name='service_delete')
]
