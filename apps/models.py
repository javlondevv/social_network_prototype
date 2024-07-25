from django.contrib.auth.models import AbstractUser
from django.db.models import (
    Model,
    ManyToManyField,
    ForeignKey,
    PositiveIntegerField,
    CharField,
    CASCADE,
    DateTimeField,
    ImageField,
    FileField,
)
from django.utils import timezone

from apps.utils import generate_unique_filename


class CreatedBaseModel(Model):
    """
    Abstract base model with created and updated timestamps.
    """

    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta class to mark this model as abstract.
        """

        abstract = True


class User(AbstractUser):
    """
    Represents a user with additional fields like avatar, liked posts, phone number, and date joined.

    Attributes:
        avatar (ImageField): The user's avatar image.
        liked_posts (ManyToManyField): Posts that the user has liked.
        phone (CharField): The user's phone number.
        date_joined (DateTimeField): The date and time when the user joined.
    """

    avatar = ImageField(upload_to=generate_unique_filename, blank=True, null=True)
    liked_posts = ManyToManyField("Post", related_name="liked_by", blank=True)
    phone = CharField(max_length=15, blank=True, null=True)
    date_joined = DateTimeField(default=timezone.now)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Like(CreatedBaseModel):
    """
    Model representing a like by a user on a post.

    Attributes:
        user (ForeignKey): The user who liked the post.
        post (ForeignKey): The post that was liked.

    Meta:
        unique_together (tuple): Ensures each user can like a post only once.
    """

    user = ForeignKey("User", on_delete=CASCADE, related_name="likes")
    post = ForeignKey("Post", on_delete=CASCADE, related_name="likes")

    class Meta:
        unique_together = ("user", "post")


class Post(CreatedBaseModel):
    """
    Represents a post with title, content, author, and like count.

    Attributes:
        title (str): The title of the post.
        content (str): The content of the post.
        author (User): The author of the post.
        likes_count (int): The number of likes the post has.

    Methods:
        update_likes_count: Updates the likes count of the post.
        number_of_likes: Returns the number of likes the post has.
    """

    title = CharField(max_length=255)
    content = FileField(upload_to=generate_unique_filename, blank=True, null=True)
    author = ForeignKey("User", related_name="posts", on_delete=CASCADE)
    likes_count = PositiveIntegerField(default=0)

    @property
    def is_image(self):
        return self.content.name.lower().endswith(("png", "jpg", "jpeg", "gif"))

    @property
    def is_video(self):
        return self.content.name.lower().endswith(("mp4", "mov", "avi"))

    def update_likes_count(self):
        self.likes_count = self.likes.count()
        self.save()

    @property
    def number_of_likes(self):
        return self.likes.count()


class Notification(CreatedBaseModel):
    TYPE_CHOICES = [
        ("like", "Like"),
    ]
    type = CharField(max_length=10, choices=TYPE_CHOICES)
    post = ForeignKey("Post", related_name="notifications", on_delete=CASCADE)
    liked_by = ForeignKey("User", related_name="notifications", on_delete=CASCADE)
