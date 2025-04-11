from django.contrib import admin

from habits.models import Habits, Award


@admin.register(Habits)
class AdminHabits(admin.ModelAdmin):
    list_display = ['id', 'user', 'place', 'tame', 'action', 'pleasant_habits_sign', 'related_habit', 'periodicity',
                    'award', 'time_to_complete', 'is_public']
    list_filter = ['id', 'action', 'user', 'award']


@admin.register(Award)
class AdminAward(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'description', 'price']
    list_filter = ['id', 'name', 'price',]
