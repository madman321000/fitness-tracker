from django.db import models
from accounts.models import User


class Exercise(models.Model):
    """Exercise model with two types: reps+weight or time+weight."""
    
    EXERCISE_TYPE_CHOICES = [
        ('reps_weight', 'Reps and Weight'),
        ('time_weight', 'Time and Weight'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercises')
    exercise_type = models.CharField(max_length=20, choices=EXERCISE_TYPE_CHOICES)
    description = models.TextField(help_text="Description of how to perform the exercise")
    weight = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Weight (can be positive or negative)"
    )
    reps = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Number of reps (required for reps_weight type)"
    )
    time_seconds = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Time in seconds (required for time_weight type)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'exercises'
        ordering = ['-created_at']
    
    def __str__(self):
        type_display = dict(self.EXERCISE_TYPE_CHOICES)[self.exercise_type]
        if self.exercise_type == 'reps_weight':
            return f"{type_display} - {self.reps} reps @ {self.weight}kg"
        else:
            return f"{type_display} - {self.time_seconds}s @ {self.weight}kg"
    
    def clean(self):
        """Validate that reps or time_seconds is provided based on exercise_type."""
        from django.core.exceptions import ValidationError
        
        if self.exercise_type == 'reps_weight' and not self.reps:
            raise ValidationError({'reps': 'Reps is required for reps_weight type'})
        if self.exercise_type == 'time_weight' and not self.time_seconds:
            raise ValidationError({'time_seconds': 'Time is required for time_weight type'})
        
        # Ensure the other field is None
        if self.exercise_type == 'reps_weight' and self.time_seconds:
            self.time_seconds = None
        if self.exercise_type == 'time_weight' and self.reps:
            self.reps = None

