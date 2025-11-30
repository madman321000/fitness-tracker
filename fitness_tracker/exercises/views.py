from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Exercise
from .serializers import ExerciseSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_exercise(request):
    """
    Create a new exercise (authenticated users only).
    
    Expected POST data:
    {
        "exercise_type": "reps_weight" or "time_weight",
        "description": "string",
        "weight": decimal (can be positive or negative),
        "reps": integer (required if exercise_type is "reps_weight"),
        "time_seconds": integer (required if exercise_type is "time_weight")
    }
    
    Returns:
    {
        "id": integer,
        "exercise_type": "string",
        "description": "string",
        "weight": decimal,
        "reps": integer or null,
        "time_seconds": integer or null,
        "created_at": "datetime",
        "updated_at": "datetime"
    }
    """
    serializer = ExerciseSerializer(data=request.data)
    
    if serializer.is_valid():
        # Associate the exercise with the authenticated user
        exercise = serializer.save(user=request.user)
        return Response(ExerciseSerializer(exercise).data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exercises(request):
    """
    Get all exercises for the authenticated user.
    
    Returns a list of exercises:
    [
        {
            "id": integer,
            "exercise_type": "string",
            "description": "string",
            "weight": decimal,
            "reps": integer or null,
            "time_seconds": integer or null,
            "created_at": "datetime",
            "updated_at": "datetime"
        },
        ...
    ]
    """
    exercises = Exercise.objects.filter(user=request.user)
    serializer = ExerciseSerializer(exercises, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exercise(request, exercise_id):
    """
    Get a specific exercise by ID (authenticated users only).
    Users can only access their own exercises.
    
    URL parameter: exercise_id (integer)
    
    Returns:
    {
        "id": integer,
        "exercise_type": "string",
        "description": "string",
        "weight": decimal,
        "reps": integer or null,
        "time_seconds": integer or null,
        "created_at": "datetime",
        "updated_at": "datetime"
    }
    """
    try:
        exercise = Exercise.objects.get(id=exercise_id, user=request.user)
    except Exercise.DoesNotExist:
        return Response(
            {'error': 'Exercise not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = ExerciseSerializer(exercise)
    return Response(serializer.data, status=status.HTTP_200_OK)

