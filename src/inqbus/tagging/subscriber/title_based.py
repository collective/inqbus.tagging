from inqbus.tagging.functions import add_tags

def image_title_to_tag(context, event):
    image = context.image

    filename = image.filename
    filename = filename.replace(' ', '.').replace('_', '.').replace('/', '.')

    name_tags = filename.split('.')

    name_tags.pop(-1)

    add_tags(context, tags_to_add=name_tags)


def title_to_tag(event):

    context = event.object

    title = context.title
    title = title.replace(' ', '.').replace('_', '.').replace('/', '.')

    name_tags = title.split('.')

    add_tags(context, tags_to_add=name_tags)
