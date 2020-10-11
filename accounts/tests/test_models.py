from django.test import TestCase
from accounts.models import Profile
from django.contrib.auth.models import User


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username='TestName',
        )
        Profile.objects.create(
            user_id='1',
            name='TestName',
            bio='TestBio',
            avatar='media/2a422c3298b5d3e6157456ae12ad7a4d39d0068c_full_8qlbGjd.jpg',
            is_moderator='False',
            is_ban='False',
            is_mute='False',
            # auth_user_id='1',
            # user='TestName',
            )

    def test_name_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('name').verbose_name
        self.assertAlmostEqual(field_label, 'name')