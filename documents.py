from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from articles.models import Article


class BaseDocument(Document):

    @classmethod
    def exact_match(cls, search_term):
        return cls.search().query({
            "query_string": {
                "query": f"*{search_term}*",
            }
        })

@registry.register_document
class ArticleDocument(BaseDocument):
    class Index:
        name = 'articles'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Article
        fields = ['title']
