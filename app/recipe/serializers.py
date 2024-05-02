"""
Serializer for recipes APIS
"""

from rest_framework import serializers
from core.models import Recipe, Tag, Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe"""

    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes',
                  'price', 'link', 'tags', 'ingredients'
                  ]
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags_ingredients,
                            recipe, object_class,
                            the_instance=None):
        """Handle getting or creating tags as needed."""
        auth_user = self.context['request'].user
        for tag in tags_ingredients:
            tag_obj, created = object_class.objects.get_or_create(
                user=auth_user,
                **tag
            )

            if the_instance == 'tags':
                recipe.tags.add(tag_obj)
            elif the_instance == 'ingredients':
                recipe.ingredients.add(tag_obj)

    def create(self, validated_data):
        """Create a recipe."""
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])

        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(
            tags_ingredients=tags, recipe=recipe,
            object_class=Tag, the_instance="tags"
        )
        self._get_or_create_tags(
            tags_ingredients=ingredients, recipe=recipe,
            object_class=Ingredient, the_instance="ingredients"
        )

        return recipe

    def update(self, instance, validated_data):
        """Update recipe."""
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(
                tags_ingredients=tags, recipe=instance,
                object_class=Tag, the_instance="tags"
            )
        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_tags(
                tags_ingredients=ingredients, recipe=instance,
                object_class=Ingredient, the_instance="ingredients"
            )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe details view"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
