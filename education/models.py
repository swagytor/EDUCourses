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
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='Курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, verbose_name='Урок', **NULLABLE)
    price = models.PositiveBigIntegerField(verbose_name='Цена')
    payment_type = models.CharField(choices=PAYMENT_CHOICES, verbose_name='Способ оплаты')

    def __str__(self):
        return f"{self.user.email} {'Курс: ' + self.course.title if self.course else 'Урок: ' + self.lesson.title}"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('-purchase_date',)
