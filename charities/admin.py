from django.contrib import admin

from charities.models import Benefactor, Task, Charity


@admin.register(Benefactor)
class BenefactorAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience', 'free_time_per_week')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_benefactor', 'charity', 'date', 'description', 'gender_limit', 'state')


@admin.register(Charity)
class CharityAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'reg_number')
