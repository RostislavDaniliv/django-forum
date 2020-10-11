from django.test import TestCase
from comments.models import Comment
from topic.models import Topic
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
            slug='testSlug',
        )
        Comment.objects.create(
            name='TestComm',
            text='TestText',
            parent_id='',
            topic_id='1',
            )

    def test_title_label(self):
        topic = Topic.objects.get(id=1)
        field_label = topic._meta.get_field('title').verbose_name
        self.assertAlmostEqual(field_label, 'title')

    def test_text_label(self):
        topic = Topic.objects.get(id=1)
        field_label = topic._meta.get_field('creator').verbose_name
        self.assertTrue(field_label == 'creator')

    def test_content_label(self):
        topic = Topic.objects.get(id=1)
        field_label = topic._meta.get_field('content').verbose_name
        self.assertAlmostEqual(field_label, 'content')

    def test_creator_label(self):
        topic = Topic.objects.get(id=1)
        field_label = topic._meta.get_field('creator').verbose_name
        self.assertTrue(field_label == 'creator')

    def test_moderator_label(self):
        topic = Topic.objects.get(id=1)
        field_label = topic._meta.get_field('moderator').verbose_name
        self.assertTrue(field_label == 'moderator')

    def test_slug_label(self):
        topic = Topic.objects.get(id=1)
        field_label = topic._meta.get_field('slug').verbose_name
        self.assertAlmostEqual(field_label, 'slug')

    def test_title_max_length(self):
        topic = Topic.objects.get(id=1)
        max_length = topic._meta.get_field('title').max_length
        self.assertEquals(max_length, 2000)

    def test_slug_max_length(self):
        topic = Topic.objects.get(id=1)
        max_length = topic._meta.get_field('slug').max_length
        self.assertEquals(max_length, 500)