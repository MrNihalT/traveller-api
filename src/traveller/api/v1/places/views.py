import datetime

from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny

from api.v1.places.serializers import PlaceSerializer , PlaceDetailSerializer , CommentSerializer
from places.models import Place , Comment 
from django.db.models import Q

from api.v1.places.pagination import StandaredResultSetPagination


@api_view(["GET"])
@permission_classes([AllowAny])
def places(request):
    instances = Place.objects.filter(is_deleted = False)

    q = request.GET.get("q")
    if q:
        ids = q.split(",")
        # instances = instances.filter(Q(name__icontains = q) | Q(place__icontains =q))
        instances = instances.filter(category__in=ids)
        # instances = instances.filter(category__name__icontains=q)

    paginator = StandaredResultSetPagination()
    paginated_result = paginator.paginate_queryset(instances,request)

    context = {
        "request":request
    }

    serializer = PlaceSerializer(paginated_result,many=True,context=context)

    response_data = {
        "status_code":6000,
        "count":paginator.page.paginator.count,
        "links": {
            "next": paginator.get_next_link(),
            "previous":paginator.get_previous_link() ,
        },
        "data": serializer.data,
    }
    return Response(response_data)


@api_view(["GET"])
@permission_classes([AllowAny])
def place(request, pk):
    try:
        instance = Place.objects.get(pk=pk)
    except Place.DoesNotExist:
        return Response({
            "status_code": 6001,
            "message": "Place does not exist",
        })

    context = {
        "request": request
    }
    serializer = PlaceDetailSerializer(instance, context=context)

    return Response({
        "status_code": 6000,
        "data": serializer.data,
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected(request,pk):
    if Place.objects.filter(pk=pk).exists():
        instance = Place.objects.get(pk=pk)
        context = {
            "request":request
        }
        serializer = PlaceDetailSerializer(instance,context=context)
        response_data = {
            "status_code":6000,
            "data": serializer.data,
        }
        return Response(response_data)
    else:
        response_data = {
            "status_code":6001,
            "message": "place not exist",
        }
        return Response(response_data)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_comment(request,pk):
    if Place.objects.filter(pk=pk).exists():
        place = Place.objects.get(pk=pk)
        comment = request.data["comment"]
        try:
            parent_comment = request.data["parent_comment"]
        except:
            parent_comment = None
    
        instance = Comment.objects.create(
            user=request.user,
            comment = comment,
            place = place,
            date = datetime.datetime.now()
        )

        if parent_comment:
            if Comment.objects.filter(pk = parent_comment).exists():
                parent = Comment.objects.get(pk = parent_comment)
                instance.parent_comment = parent
                instance.save()

        response_data = {
            "status_code":6000,
            "message": "succesfully added",
        }

        return Response(response_data)

    else:
        response_data = {
            "status_code":6001,
            "message": "place not exist",
        }
        return Response(response_data)


@api_view(["GET"])
@permission_classes([AllowAny])
def comments(request,pk):
    if Place.objects.filter(pk=pk).exists():
        place = Place.objects.get(pk = pk)

        instances = Comment.objects.filter(place = place , parent_comment = None)
        context = {
            "request":request
        }

        serializer = CommentSerializer(instances,many=True,context=context)

        response_data = {
            "status_code":6000,
            "data": serializer.data,
        }
        

    else:
        response_data = {
            "status_code":6001,
            "message": "place not exist",
        }
    
    return Response(response_data)
   
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like(request, pk):
    if Place.objects.filter(pk=pk).exists():
        instance = Place.objects.get(pk=pk)

        if instance.likes.filter(username = request.user.username).exists():
            instance.likes.remove(request.user)
            message = "like removed"
        
        else:
            instance.likes.add(request.user)
            message = "liked"

        response_data = {
            "status_code":6000,
            "message": message,
        }
        

    else:
        response_data = {
            "status_code":6001,
            "message": "place not exist",
        }
    
    return Response(response_data)