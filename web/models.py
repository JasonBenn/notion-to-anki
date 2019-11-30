from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import BooleanField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import IntegerField
from django.db.models import ManyToManyField
from django.db.models import Model
from django.db.models import TextField

from web.utils import now


class BaseModel(Model):
    created_at = DateTimeField(default=now, editable=False)
    updated_at = DateTimeField(default=now, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super().save(*args, **kwargs)


class GoodreadsEntity(BaseModel):
    goodreads_id = IntegerField()
    url = TextField()

    class Meta:
        abstract = True


class GoodreadsSeries(GoodreadsEntity):
    title = TextField()

    def __str__(self):
        return f"<GoodreadsSeries: {self.title}>"


class GoodreadsAuthor(GoodreadsEntity):
    first_name = TextField()
    last_name = TextField(null=True, blank=True)

    def __str__(self):
        return f"<GoodreadsAuthor: {self.first_name} {self.last_name}>"


class GoodreadsBook(GoodreadsEntity):
    title = TextField()
    series = ForeignKey(GoodreadsSeries, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="books")
    authors = ManyToManyField(GoodreadsAuthor, related_name="books")

    def __str__(self):
        return f"<GoodreadsBook: {self.title}>"


class GoodreadsUser(GoodreadsEntity):
    first_name = TextField()
    last_name = TextField(null=True, blank=True)

    def __str__(self):
        return f"<GoodreadsUser: {self.first_name} {self.last_name}>"


class GoodreadsShelf(GoodreadsEntity):
    books = ManyToManyField(GoodreadsBook)

    def __str__(self):
        return f"<GoodreadsShelf: {len(self.books)} books>"


class NotionDocument(BaseModel):
    notion_id = TextField(null=True, blank=True, unique=True)
    parent_notion_document = ForeignKey("NotionDocument", on_delete=models.CASCADE, related_name="parent_document", null=True, blank=True)
    title = TextField(null=True, blank=True)
    url = TextField()
    bookmarked = BooleanField(default=False)
    embedding = JSONField(null=True, blank=True)

    def __str__(self):
        if self.title is None:
            title = "[not yet scraped] " + self.url
        elif self.title == "":
            title = "[empty title]"
        else:
            title = self.title
        return f"<NotionDocument: {title}>"


class Text(BaseModel):
    class Meta:
        unique_together = ('text', 'source_book', 'source_notion_document')

    text = TextField()
    embedding = JSONField(null=True, blank=True)
    projection = JSONField(null=True, blank=True)
    source_author = ForeignKey(GoodreadsAuthor, null=True, blank=True, on_delete=models.CASCADE)
    source_series = ForeignKey(GoodreadsSeries, null=True, blank=True, on_delete=models.CASCADE)
    source_book = ForeignKey(GoodreadsBook, null=True, blank=True, on_delete=models.CASCADE)
    source_notion_document = ForeignKey(NotionDocument, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        maybe_ellipsis = "..." if len(self.text) > 25 else ""
        return f"<Text: {self.text[:25]}{maybe_ellipsis}>"
