from django.test import TestCase
from comments.models import Comment, Topic
from django.contrib.auth.models import User


class CommentsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username='TestName',
        )
        Topic.objects.create(
            creator_id='1',
            title='TestTitle',
            content='TestContent',
            moderator_id='1',
            slug='test_slug',
        )
        Comment.objects.create(
            name='TestComm',
            text='TestText',
            parent_id='',
            topic_id='1',
            )

    def test_name_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('name').verbose_name
        self.assertAlmostEqual(field_label, 'name')

    def test_text_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('text').verbose_name
        self.assertAlmostEqual(field_label, 'text')

    def test_name_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_text_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('text').max_length
        self.assertEquals(max_length, 5000)