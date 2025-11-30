from django.contrib import admin
from .models import Exercise


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """Admin interface for Exercise model."""
    list_display = ('id', 'user', 'exercise_type', 'weight', 'reps', 'time_seconds', 'created_at')
    list_filter = ('exercise_type', 'created_at')
    search_fields = ('user__username', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('user', 'exercise_type')}),
        ('Exercise Details', {'fields': ('description', 'weight', 'reps', 'time_seconds')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

