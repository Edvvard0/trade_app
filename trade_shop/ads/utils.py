from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from ads.models import Ad


def q_search(query):
    vector = SearchVector("title", "description")
    query = SearchQuery(query)
    return Ad.objects.annotate(rank=SearchRank(vector, query)).order_by("-rank")