from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=200, unique=True
    )
    color = models.CharField(
        unique=True, max_length=7
    )
    slug = models.SlugField(
        max_length=200, unique=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, unique=True
    )
    measurement_unit = models.CharField(
        max_length=200
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='recipes/'
    )
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient, through='NumberOfIngredients'
    )
    tags = models.ManyToManyField(Tag)
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1, message='Время приготовления должно быть больше 0!'
            )
        ]
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class NumberOfIngredients(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Количество должно быть больше 0!')
        ]
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredients_in_recipe'
            )
        ]
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_recipe_in_favorite'
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='shopping_lists'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='shopping_lists'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_in_shopping_list'
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
