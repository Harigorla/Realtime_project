from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.decorators import action
from .models import Recipe
from rest_framework.permissions import IsAuthenticated
from .serializer import RecipeSerializer


class RecipeApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        recipes = Recipe.objects.all()
        ser_obj = RecipeSerializer(recipes, many=True)
        return Response(ser_obj.data)

    def put(self, request):
        recipe_id = request.data["recipe_id"]
        name = request.data["name"]
        recipe_obj = Recipe.objects.get(id=recipe_id)
        recipe_obj.recipe_name = name
        recipe_obj.save()
        return Response({"message": "Successfully Updated"})

    def post(self, request):
        serializer_obj = RecipeSerializer(data=request.data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response(serializer_obj.data)
        return Response({"message": serializer_obj.errors})


class RecipeViewset(viewsets.ViewSet):
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    @action(methods=["GET"], detail=False)
    def get_recipes(self, request):
        recipes = list(Recipe.objects.values("id", "recipe_name", "ingredients"))
        return Response(recipes)
