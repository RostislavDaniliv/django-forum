from django.test import TestCase
from accounts.models import Profile
from django.contrib.auth.models import User


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username='TestName',
        )
        Profile.objects.update(
            user_id='1',
            name='TestName',
            bio='TestBio',
            avatar='media/2a422c3298b5d3e6157456ae12ad7a4d39d0068c_full_8qlbGjd.jpg',
            is_moderator='False',
            is_ban='False',
            is_mute='False',
            )

    def test_name_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('name').verbose_name
        self.assertAlmostEqual(field_label, 'name')

    def test_bio_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('bio').verbose_name
        self.assertAlmostEqual(field_label, 'bio')

    def test_avatar_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('avatar').verbose_name
        self.assertAlmostEqual(field_label, 'avatar')

    def test_is_moderator_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('is_moderator')
        self.assertFalse(field_label == 'is_moderator')

    def test_is_ban_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('is_ban')
        self.assertFalse(field_label == 'is_ban')

    def test_is_mute_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('is_mute')
        self.assertFalse(field_label == 'is_mute')

    def test_name_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_bio_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('bio').max_length
        self.assertEquals(max_length, 2000)
