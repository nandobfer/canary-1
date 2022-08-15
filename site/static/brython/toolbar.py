from browser import document, ajax, html, bind, window, alert, timer

jQuery = window.jQuery


class Tool():
    def __init__(self, toolbar, content_id):
        self.toolbar = toolbar
        self.name = content_id
        self.content_id = f'{content_id}-container'
        self.content = document[f'{content_id}-container']

        self.toolbar.bind('click', self.switchTool)

    def switchTool(self, ev):
        if not self.content.style.display == 'none':
            return None

        jQuery('.main-container').hide()
        jQuery('.toolbar').removeClass('toolbar-active')

        jQuery(self.toolbar).addClass('toolbar-active')
        jQuery(self.content).fadeToggle('slow')


def initialRender():
    jQuery('.main-container').hide()
    jQuery('#home-container').show()

    for element in document.select('.toolbar'):
        tool = Tool(element, element.attrs['id'][8:])


initialRender()
