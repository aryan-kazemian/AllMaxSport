from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Blog, Tag, Category, SEOStatus
from .serializers import BlogSerializer, TagSerializer, CategorySerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class BlogModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Tech")
        self.tag1 = Tag.objects.create(name="Python")
        self.tag2 = Tag.objects.create(name="Django")
        self.blog = Blog.objects.create(
            title="Test Blog",
            author="Author Name",
            content="Some content",
            category=self.category,
            status="draft",
            seo_score=50,
            seo_score_color="text-gray-500",
        )
        self.blog.tags.set([self.tag1, self.tag2])
        self.seo_status = SEOStatus.objects.create(
            blog=self.blog,
            title_length_status="ok",
            title_length_message="Good title",
            content_length_status="ok",
            content_length_message="Content ok",
            keyword_density_status="ok",
            keyword_density_message="Density ok",
            meta_description_status="ok",
            meta_description_message="Meta ok",
            headings_status="ok",
            headings_message="Headings ok",
            images_status="ok",
            images_message="Images ok",
            internal_links_status="ok",
            internal_links_message="Links ok",
        )

    def test_blog_creation(self):
        self.assertEqual(self.blog.title, "Test Blog")
        self.assertEqual(self.blog.category.name, "Tech")
        self.assertEqual(self.blog.tags.count(), 2)
        self.assertTrue(hasattr(self.blog, 'seo_status'))

    def test_tag_str(self):
        self.assertEqual(str(self.tag1), "Python")

    def test_category_str(self):
        self.assertEqual(str(self.category), "Tech")

    def test_seo_status_str(self):
        self.assertEqual(str(self.seo_status), f"SEO Status for {self.blog.title}")


class BlogSerializerTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Lifestyle")
        self.tag = Tag.objects.create(name="Health")
        self.blog_data = {
            "title": "Healthy Life",
            "author": "John Doe",
            "content": "Content about health",
            "category": {"name": "Lifestyle"},
            "tags": [{"name": "Health"}],
            "status": "draft",
            "seo_status": {
                "title_length_status": "ok",
                "title_length_message": "Good",
                "content_length_status": "ok",
                "content_length_message": "Good",
                "keyword_density_status": "ok",
                "keyword_density_message": "Good",
                "meta_description_status": "ok",
                "meta_description_message": "Good",
                "headings_status": "ok",
                "headings_message": "Good",
                "images_status": "ok",
                "images_message": "Good",
                "internal_links_status": "ok",
                "internal_links_message": "Good",
            }
        }

    def test_blog_serializer_create(self):
        from .serializers import BlogSerializer
        serializer = BlogSerializer(data=self.blog_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        blog = serializer.save()
        self.assertEqual(blog.title, "Healthy Life")
        self.assertEqual(blog.category.name, "Lifestyle")
        self.assertEqual(blog.tags.first().name, "Health")
        self.assertTrue(hasattr(blog, "seo_status"))


class BlogAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="staffuser", password="testpass", user_type="staff", is_staff=True)
        self.blog = Blog.objects.create(title="API Blog", content="API content", status="draft")
        self.category = Category.objects.create(name="API Category")
        self.tag = Tag.objects.create(name="API Tag")

    def test_get_blogs_public(self):
        response = self.client.get(reverse("blog-api"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)

    def test_create_blog_requires_staff(self):
        self.client.login(username="staffuser", password="testpass")
        data = {
            "title": "New Blog",
            "content": "Some content",
            "status": "draft",
            "category": {"name": "API Category"},
            "tags": [{"name": "API Tag"}]
        }
        response = self.client.post(reverse("blog-api"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.json())

    def test_create_blog_without_login_forbidden(self):
        data = {"title": "Fail Blog", "content": "No login"}
        response = self.client.post(reverse("blog-api"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_blog(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("blog-api") + f"?id={self.blog.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Blog.objects.filter(id=self.blog.id).exists())

    def test_tag_creation_via_api(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("blog-api") + "?tag=true", {"tag_name": "NewTag"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Tag.objects.filter(name="NewTag").exists())
