from django.test import TestCase
from comments.models import Comment


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Comment.objects.create(name='TestComm',
                               text='TestText',
                               parent_id='',
                               topic_id='1',
                               )

    def test_name_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('name').verbose_name
        self.assertAlmostEqual(field_label, 'name')