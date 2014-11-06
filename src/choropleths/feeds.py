from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from choropleths.models import Choropleth

class ChoroplethFeed(Feed):
    title = "Choropleths"
    link = '/feed/'

    def items(self):
        return Choropleth.objects \
                .filter(published=1) \
                .order_by('-created_at') \
                .select_related('dataset')[0:10]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.dataset.description

    def item_link(self, item):
        return reverse('choropleths:view', args=[item.id])
