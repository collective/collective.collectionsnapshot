from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFPlone import PloneMessageFactory as _
from AccessControl import Unauthorized
from ZODB.POSException import ConflictError
from OFS.CopySupport import CopyError

from zope.component import getMultiAdapter

from utils import paste_as_related_items, copy_collected


class CopyCollected(BrowserView):

    def __call__(self):
        context = aq_inner(self.context)
        items = context.queryCatalog(batch=True, full_objects=True)
        cp = copy_collected(items, self.request)
        return cp


class Paste(BrowserView):
    """Paste copied objects into the relatedItems field.
    """

    def __call__(self):
        context = aq_inner(self.context)

        # If this is a map, we try the default page.
        view = getMultiAdapter((context, self.request),
                               name='default_page')
        default_page = view.getDefaultPage()
        if default_page:
            target = context.get(default_page)
        else:
            target = context

        if not hasattr(target, 'getField'):
            # Probably Plone Site root.
            return 'nope'
        if not target.getField('relatedItems'):
            return 'No relatedItems field.'

        try:
            result = paste_as_related_items(target, REQUEST=self.request,
                                            fieldname='relatedItems')
        except CopyError:
            return 'invalid data'
        return result or 'no new stuff'
