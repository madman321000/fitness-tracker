from rest_framework import serializers
from .models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    """Serializer for Exercise model."""
    
    class Meta:
        model = Exercise
        fields = ['id', 'exercise_type', 'description', 'weight', 'reps', 'time_seconds', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate that reps or time_seconds is provided based on exercise_type."""
        exercise_type = data.get('exercise_type')
        reps = data.get('reps')
        time_seconds = data.get('time_seconds')
        
        if exercise_type == 'reps_weight':
            if not reps:
                raise serializers.ValidationError({
                    'reps': 'Reps is required for reps_weight type'
                })
            if time_seconds:
                raise serializers.ValidationError({
                    'time_seconds': 'Time should not be provided for reps_weight type'
                })
        elif exercise_type == 'time_weight':
            if not time_seconds:
                raise serializers.ValidationError({
                    'time_seconds': 'Time is required for time_weight type'
                })
            if reps:
                raise serializers.ValidationError({
                    'reps': 'Reps should not be provided for time_weight type'
                })
        
        return data

