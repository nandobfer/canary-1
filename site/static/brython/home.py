from browser import document, ajax, html, bind, window, alert, timer

jQuery = window.jQuery
POPUP = jQuery('#floating-popup')

containers = '#home-container>div:not(.moonlight-wolf)'


def toggleContainer(selection=['.main-container', '.body-toolbar'], mode=None):
    if mode == 'blur':
        for item in selection:
            jQuery(item).css('filter', 'blur(2px)')
            jQuery(item).css('pointer-events', 'none')
    else:
        for item in selection:
            jQuery(item).css('filter', 'blur(0)')
            jQuery(item).css('pointer-events', 'auto')


def resizePopUp(width_factor=1, height_factor=3.5, translate_factor=1.75/2):
    jQuery('#floating-popup').height(jQuery('#floating-popup').height() * height_factor)


def renderPopUp():
    height = jQuery('#home-container').height()
    width = jQuery('#home-container').width()
    POPUP.css('transform',
              f'translateY({height/2}px) translateX({width/3}px)')

    POPUP.fadeToggle()

    @bind('#floating-popup > button', 'click')
    def togglePopUp(ev):
        POPUP.fadeToggle()
        toggleContainer()


def initialRender():
    renderPopUp()

    @bind(containers, 'mouseenter')
    def mousein(ev):
        container = jQuery(ev.target)
        container.find('h2').hide()
        container.find('p:last-of-type').hide()
        container.find('p:first-of-type').fadeIn()
        container.find('img').addClass('active-img')
        container.addClass('active-home-container')

    @bind(containers, 'mouseleave')
    def mouseout(ev):
        container = jQuery(ev.target)
        container.find('h2').fadeIn()
        container.find('p:last-of-type').fadeIn()
        container.find('p:first-of-type').hide()
        container.find('img').removeClass('active-img')
        container.removeClass('active-home-container')

    jQuery('#loading-screen').slideToggle('slow')


def _ajax(url, onComplete, method='GET', data={}):
    req = ajax.Ajax()
    req.bind('complete', onComplete)
    req.open(method, url, True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send(data)


initialRender()
