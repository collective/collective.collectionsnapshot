#view_management_screens='View management screens'
#copy_or_move='Copy or Move'

from OFS.CopySupport import CopyError, _cb_decode, _cb_encode, cookie_path
from OFS import Moniker
from ZODB.POSException import ConflictError


def paste_as_related_items(context, cb_copy_data=None, REQUEST=None,
                           fieldname='relatedItems'):
    """Paste previously copied objects into the current object as
    related items.

    Note that this is additive: no currently related items are removed.

    If calling this function from python code, pass the result of a
    previous call to OFS.manage_copyObjects as the first argument.

    Note that the results from a copy are accepted, not from a cut (move).

    This function is mostly a stripped down version of
    manage_pasteObjects from OFS.CopySupport.
    """
    if cb_copy_data is not None:
        cp = cb_copy_data
    elif REQUEST is not None and '__cp' in REQUEST.keys():
        cp = REQUEST['__cp']
    else:
        cp = None
    if cp is None:
        raise CopyError

    if not context.cb_dataValid:
        raise CopyError

    try:
        op, mdatas = _cb_decode(cp)
    except:
        raise CopyError

    if op != 0:
        # We only support pasting from a copy operation, not from a move/cut.
        raise CopyError
    oblist = []
    app = context.getPhysicalRoot()
    for mdata in mdatas:
        m = Moniker.loadMoniker(mdata)
        try:
            ob = m.bind(app)
        except ConflictError:
            raise
        except:
            raise CopyError
        oblist.append(ob)

    field = context.getField(fieldname)
    related = field.getRaw(context)
    new_ids = []
    for ob in oblist:
        uid = ob.UID()
        if uid not in related:
            related.append(uid)
            new_ids.append(ob.getId())

    if new_ids:
        field.set(context, related)

    # Report back
    return new_ids


#def copy_collected(self, ids=None, REQUEST=None, RESPONSE=None):

def copy_collected(objects, REQUEST=None):
    """Put a reference to the objects in the clip board

    This function is derived from manage_copyObjects in
    OFS.CopySupport.
    """
    oblist = []
    for ob in objects:
        if not ob.cb_isCopyable():
            raise CopyError
        m = Moniker.Moniker(ob)
        oblist.append(m.dump())
    cp = (0, oblist)
    cp = _cb_encode(cp)
    if REQUEST is not None:
        resp = REQUEST['RESPONSE']
        resp.setCookie('__cp', cp, path='%s' % cookie_path(REQUEST))
        REQUEST['__cp'] = cp
    return cp
