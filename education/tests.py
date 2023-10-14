from rest_framework import status
from rest_framework.test import APITestCase

from education.models import Lesson, Course, Subscribe
from users.models import User


# Create your tests here.
class LessonTestCase(APITestCase):
    def setUp(self):
        self.lesson_url = '/education/lesson/'

        self.user = User.objects.create(email='user@sky.pro', password='12345', is_staff=False, is_superuser=False)

        self.course = Course.objects.create(
            title='test course',
            description='description of course',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title='test lesson',
            description='description of lesson',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            owner=self.user,
            course=self.course
        )

        self.client.force_authenticate(user=self.user)

    def test_get_lesson_list(self):
        response = self.client.get(self.lesson_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json()['results'],
            [
                {
                    'course': self.lesson.course.pk,
                    'description': self.lesson.description,
                    'owner': self.lesson.owner.pk,
                    'title': self.lesson.title,
                    'video_url': self.lesson.video_url,
                }
            ]
        )

    def test_create_lesson(self):
        data_for_post = {
            'course': self.course.pk,
            'description': 'create description',
            'title': 'created title',
            'video_url': self.lesson.video_url,
        }

        post_response = self.client.post(self.lesson_url + "create/", data=data_for_post)

        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        get_response = self.client.get(self.lesson_url)

        self.assertEqual(
            get_response.json()['results'],
            [
                {
                    'course': self.lesson.course.pk,
                    'description': self.lesson.description,
                    'owner': self.lesson.owner.pk,
                    'title': self.lesson.title,
                    'video_url': self.lesson.video_url,
                },
                {
                    'course': self.lesson.course.pk,
                    'description': 'create description',
                    'owner': self.lesson.owner.pk,
                    'title': 'created title',
                    'video_url': self.lesson.video_url,
                }
            ]
        )

    def test_retrieve_lesson(self):
        response = self.client.get(self.lesson_url + f"{self.lesson.pk}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), {
            'course': self.lesson.course.pk,
            'description': self.lesson.description,
            'owner': self.lesson.owner.pk,
            'title': self.lesson.title,
            'video_url': self.lesson.video_url,
        })

    def test_update_lesson(self):
        updated_data = {
            'course': self.course.pk,
            'description': 'updated description',
            'owner': self.user.pk,
            'title': 'updated title',
            'video_url': 'https://www.youtube.com/watch?v=kwAAMLxY3sY',
        }

        put_response = self.client.put(self.lesson_url + f'update/{self.lesson.pk}/', data=updated_data)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.lesson_url)

        self.assertEqual(
            response.json()['results'],
            [
                {
                    'course': self.lesson.course.pk,
                    'description': updated_data['description'],
                    'owner': self.lesson.owner.pk,
                    'title': updated_data['title'],
                    'video_url': updated_data['video_url'],
                }
            ]
        )

        patch_response = self.client.patch(self.lesson_url + f'update/{self.lesson.pk}/', data={'title': 'new title'})
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.lesson_url)

        self.assertEqual(
            response.json()['results'],
            [
                {
                    'course': self.lesson.course.pk,
                    'description': updated_data['description'],
                    'owner': self.lesson.owner.pk,
                    'title': 'new title',
                    'video_url': updated_data['video_url'],
                }
            ]
        )

    def test_delete_lesson(self):
        delete_response = self.client.delete(self.lesson_url + f'delete/{self.lesson.pk}/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(self.lesson_url)

        self.assertEqual(response.json()['results'],
                         [])


class SubcribeTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email='user@sky.pro', password='12345', is_staff=False, is_superuser=False)

        self.course = Course.objects.create(
            title='test course',
            description='description of test course',
            owner=self.user
        )

        self.url = f'/education/course_subscription/{self.course.pk}/'

        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'message': 'Вы подписались на курс!'})
        is_subscribed = Subscribe.objects.filter(course=self.course, user=self.user).exists()
        self.assertEqual(is_subscribed, True)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'Подписка на курс отменена!'})
        is_subscribed = Subscribe.objects.filter(course=self.course, user=self.user).exists()
        self.assertEqual(is_subscribed, False)
