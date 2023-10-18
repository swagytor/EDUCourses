from django.db import models

from users.models import User

NULLABLE = {
    'null': True,
    'blank': True
}


# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    preview = models.ImageField(upload_to='courses/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)
    price = models.PositiveBigIntegerField(verbose_name='Цена')

    product_id = models.CharField(max_length=200, verbose_name='Идентификатор продукта', **NULLABLE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    preview = models.ImageField(upload_to='lessons/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание')
    video_url = models.URLField(verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Payment(models.Model):
    CASH_TYPE_PAYMENT = 'cash'
    CARD_TYPE_PAYMENT = 'card'

    PAYMENT_CHOICES = [
        (CASH_TYPE_PAYMENT, 'Наличными'),
        (CARD_TYPE_PAYMENT, 'Картой')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    purchase_date = models.DateTimeField(verbose_name='Дата покупки', auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='Курс', null=True)
    payment_type = models.CharField(default=CARD_TYPE_PAYMENT, choices=PAYMENT_CHOICES, verbose_name='Способ оплаты')

    session_id = models.CharField(max_length=100, verbose_name='Идентификатор сессии', **NULLABLE)
    session_url = models.TextField(verbose_name='Ссылка для оплаты', **NULLABLE)

    def __str__(self):
        return f"{self.user.email} 'Курс:' {self.course.title}"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('-purchase_date',)


class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')

    def __str__(self):
        return f"{self.course.title} - {self.user.email}"

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
