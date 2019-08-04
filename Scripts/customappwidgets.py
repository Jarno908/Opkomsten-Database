from pygubu import BuilderObject, register_widget, register_property
from custompathchooser import CustomPathChooser
from customscrolledframe import VerticalScrolledFrame


class CustomPathChooserWidgetBuilder(BuilderObject):
    class_ = CustomPathChooser
    OPTIONS_CUSTOM = ('selection type', 'path', "title", 'image', 'textvariable', "test")
    properties = OPTIONS_CUSTOM


register_widget('customappwidgets.customPathChooserWidget', CustomPathChooserWidgetBuilder,
                'CustomPathChooserWidget', ('ttk', 'customapp'))

props = {
    'selection type': {
        'editor': 'choice',
        'params': {
            'values': (CustomPathChooser.FILE, CustomPathChooser.DIR, CustomPathChooser.FILES), 'state': 'readonly'},
        'default': CustomPathChooser.FILE
        },
    'path': {
        'editor': 'entry'
        },
    'title': {
        'editor': 'entry'
        },
    'image': {
        'editor': 'imageentry'
        },
    'textvariable': {
        'editor': 'tkvarentry'
        },
    'test': {
        'editor': 'entry'
        }
    }

for p in props:
    register_property(p, props[p])

class CustomScrolledFrameWidgetBuilder(BuilderObject):
    class_ = VerticalScrolledFrame

register_widget('customappwidgets.customScrolledFrameWidget', CustomScrolledFrameWidgetBuilder,
                    'CustomScrolledFrameWidget', ('ttk', 'customapp'))
