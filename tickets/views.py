
from django.shortcuts import get_object_or_404 
#---------------------------
from rest_framework.decorators import api_view
from rest_framework.views import APIView
#---------------------------
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Guest , Movie, Reservation
from .serializers import GuestSerializer,MovieSerializer,ReservationSerializer
from .pagination import MoivPagintion

#######################################################
#############     functions base v     ###############
#######################################################

@api_view(["GET", "POST"])
def movie_list(request):
  if request.method == "GET":
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies , many=True)
    return Response(serializer.data)
  elif request.method == "POST":
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data , stats=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve
@api_view(["GET", "PUT"])
def movie_detail(request, pk):
  try :
    movie = Movie.objects.get(pk =pk)
  except Movie.DoesNotExist:
    Response("not found" , status=status.HTTP_404_NOT_FOUND)
  
  if request.method == "GET":
    serializer = MovieSerializer(movie)
    return Response(serializer.data)
  
  elif request.method == "PUT":
    serializer = MovieSerializer(movie, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
@api_view(["DELETE"])
def delete_movie(request, pk):

    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(
            {"error": "Movie not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    movie.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)

#######################################################
#############   CLASS BASE VIEW         ###############
#######################################################

class MovieList(APIView):
  permission_classes = [IsAuthenticatedOrReadOnly]
  def get(self, request):
    movie = Movie.objects.all()
    paginator = MoivPagintion()
    page = paginator.paginate_queryset(movie,request)
    serializer = MovieSerializer(page , many=True)
    return paginator.get_paginated_response(serializer.data)
  def post(self, request):
    serialzer =  MovieSerializer(data=request.data)
    if serialzer.is_valid():
      serialzer.save()
      return Response(serialzer.data)
    return Response(serialzer.errors)
  
class MovieDetils(APIView):
  permission_classes = [IsAuthenticatedOrReadOnly]
  def get_object(self,pk):
    try:
      return Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
      return None
    
  def get(self, request,pk):
    movie = self.get_object(pk)
    if movie is None:
      return Response(status=status.HTTP_404_NOT_FOUND)
    serialzer = MovieSerializer(movie)
    return Response(serialzer.data)
  
  def put(self,request,pk):
    movie = self.get_object(pk)
    if movie is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = MovieSerializer(movie,data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)
  
  def delete(self, request, pk):
    movie = self.get_object(pk)
    movie.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

#######################################################
############# guest     ###############
#######################################################
class GuestView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self, request):
    guests = Guest.objects.filter(user=request.user)
    serializer = GuestSerializer(guests, many=True)
    return Response(serializer.data)
  def post(self, request):
    serializer = GuestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
  def delete(self, request, pk):
    guest = get_object_or_404(Guest, pk=pk, user=request.user)
    guest.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)