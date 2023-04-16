from haystack import indexes

from books.models import Book


class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    title = indexes.CharField(model_attr="title")
    author = indexes.CharField(model_attr="author")
    description = indexes.CharField(model_attr="description")

    def get_model(self):
        return Book
