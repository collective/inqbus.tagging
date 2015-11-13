
def title_to_tag(context, event):
    image = context.image

    filename = image.filename
    filename = filename.replace(' ', '.').replace('_', '.').replace('/', '.')

    name_tags = filename.split('.')

    name_tags.pop(-1)

    tags = list(context.Subject()) + name_tags

    tags = list(set(tags))

    clear_tags = []

    for tag in tags:
        try:
            int(tag)
        except ValueError:
            clear_tags.append(tag)
        else:
            continue

    context.setSubject(clear_tags)
    context.reindexObject()
