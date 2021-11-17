from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100, verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=10, verbose_name='Еденица измерения'
    )

    class Meta:
        indexes = [
           models.Index(fields=['name']),
        ]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя тега',)
    color = models.CharField(max_length=7, verbose_name='Цвет в HEX')
    slug = models.SlugField(
        max_length=200,
        verbose_name='Уникальный слаг',
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag, verbose_name='Теги', related_name='recipes'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='resipes',
        through='QuantityIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингридиенты',
    )
    name = models.CharField(max_length=200, verbose_name='Название рецепта',)
    image = models.ImageField(
        upload_to='recipes/image/', verbose_name='Изображение рецепта',
    )
    text = models.TextField(max_length=500, verbose_name='Описание',)
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(1, 'Минимальное значение: 1 минута'),
        ], verbose_name='Время приготовления',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации рецепта',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['pub_date']

    def __str__(self):
        return self.name


class QuantityIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='amount'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='amount'
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1, 'Минимальное значение: 1')],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'], name='unicue_ingredient'
            ),
        ]

    def __str__(self):
        return f'{self.ingredient}, {self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='add_favirite'
            ),
        ]


class Shopping_cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shoping_cart'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shoping_cart'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='add_shopping_cart'
            ),
        ]
