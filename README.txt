Introduction
============


Collection Snapshot gives two browser views:

- ``@@collection-snapshot``: use this view on a Collection to copy the
  collected contents and put them in a cookie; so this does basically
  the same thing as when using the ``copy`` action.

- ``@@paste-related``: use this view on a Page (or any other content
  with a ``relatedItems`` field, which is true for all default types
  from ``ATContentTypes``) to paste the items from the previous cookie
  as related items in this content.  It works for items copied from a
  Collection with the ``@@collection-snapshot`` action, but also for
  items copied using the normal ``copy`` action.

Note that Folders also have a ``relatedItems`` field (which is
invisible by default).  If you use the ``@@paste-related`` view on a
Folder, we first check if there is a default page and paste the items
there instead.


To do
-----

- Make a GS profile to add these views as proper actions.

- Check that we only take the first batch of results.

- Possibly make available an action to collect *all* items instead of
  just the first batch; it could be good to have this available as
  view but not visible as action, to avoid confusion.

- Add tests.

- Currently tested on Plone 3.3.5; see if this works for Plone 4 as
  well.  Properly registering the ``@@collection-snapshot`` view for
  Collections may be tricky, due to the old-style interfaces in
  ATContentTypes (see the interfaces module versus the interface
  module and see the differences here between Plone 3 and 4).
