from inqbus.tagging.functions import add_tags, get_tagging_config

import re


def image_title_to_tag(context, event):
    tagging_config = get_tagging_config()
    if tagging_config.use_title:
        image = context.image

        filename = image.filename

        if tagging_config.title_regex:
            regex = tagging_config.title_regex
            regex_compiled = re.compile(regex)
            name_tags = regex_compiled.findall(filename)
        else:
            filename = filename.replace(' ', '.').replace('_', '.').replace('/', '.')

            name_tags = filename.split('.')

            name_tags.pop(-1)

        add_tags(context, tags_to_add=name_tags)


def title_to_tag(event):
    tagging_config = get_tagging_config()
    if tagging_config.use_title:

        context = event.object
        object_title_to_tag(context)


def object_title_to_tag(context):
    title = context.title

    tagging_config = get_tagging_config()

    if tagging_config.title_regex:
            regex = tagging_config.title_regex
            regex_compiled = re.compile(regex)
            name_tags = regex_compiled.findall(title)
    else:

        title = title.replace(' ', '.').replace('_', '.').replace('/', '.')

        name_tags = title.split('.')

    add_tags(context, tags_to_add=name_tags)
