from Products.CMFPlone.utils import safe_unicode


def add_tags(obj, tags_to_add=[]):

    tags = list(obj.Subject()) + tags_to_add

    tags = list(set(tags))

    clear_tags = []

    for tag in tags:

        try:
            int(tag)
        except ValueError:
            pass
        else:
            continue

        try:
            clear_tag = safe_unicode(tag)
        except UnicodeDecodeError:
            continue

        if len(clear_tag) < 100:
            clear_tags.append(clear_tag)

    obj.setSubject(clear_tags)
    obj.reindexObject()