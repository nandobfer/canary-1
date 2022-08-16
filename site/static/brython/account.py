from browser import document, ajax, html, bind, window, alert, timer

jQuery = window.jQuery
user = None
POPUP = jQuery('#floating-popup')

containers = '#home-container>div:not(.moonlight-wolf)'

login_email = jQuery('#login-email')
login_password = jQuery('#login-password')
login_form_text = jQuery('#login-form > p')


class User():
    def __init__(self, data):
        self.id = data['id']
        self.username = data['user']
        self.password = data['password']
        self.name = data['name']
        self.type = data['member']
        self.characters = data['characters']

    def updatePassword(self):
        POPUP.fadeToggle()
        POPUP.find('h1').text('Atualize sua senha')
        POPUP.find('p').text(
            'O sistema foi atualizado e sua senha precisa ser redefinida.')

        pass_input = '<label for="input-new-password-temp">Nova senha</label><input type="password" id="input-new-password-temp" required>'
        pass_input_confirmation = '<label for="input-new-password-temp-conf">Confirme a nova senha</label><input type="password" id="input-new-password-temp-conf" required>'
        button = POPUP.find('button')
        button.remove()
        POPUP.append(pass_input)
        POPUP.append(pass_input_confirmation)
        POPUP.append(button)


def _ajax(url, onComplete, method='GET', data={}):
    req = ajax.Ajax()
    req.bind('complete', onComplete)
    req.open(method, url, True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send(data)


def toggleContainer(selection=['.main-container', '.body-toolbar'], mode=None):
    if mode == 'blur':
        for item in selection:
            jQuery(item).css('filter', 'blur(3px)')
            jQuery(item).css('pointer-events', 'none')
    else:
        for item in selection:
            jQuery(item).css('filter', 'blur(0)')
            jQuery(item).css('pointer-events', 'auto')


def login(req):
    data = (eval(req.text))
    if data:
        global user
        if not login_form_text.css('display') == 'none':
            login_form_text.fadeOut()

        user = User(data)
        if user.characters:

            for character in user.characters:
                div = f'<div pos="{user.characters.index(character)}" id="char-{character["id"]}-container" class="account-characters"></div>'
                jQuery('.account-characters-container').append(div)
                p = f'<p pos="{user.characters.index(character)}" id="char-{character["id"]}">{character["name"]}</p>'
                jQuery(f'#char-{character["id"]}-container').append(p)
                jQuery('.account-characters-container').append('<hr>')

                jQuery(
                    f'#char-{character["id"]}-container').on('click', renderCharacter)

        jQuery('#account-login-container').fadeToggle(
            jQuery('#account-profile-container').fadeToggle)

    else:
        login_form_text.hide()
        login_form_text.text('E-mail ou senha inválidos')
        login_form_text.fadeIn()

        login_password.val('')
        login_password.focus()

    POPUP.fadeToggle()
    toggleContainer()


def sendLogin(ev):
    toggleContainer(mode='blur')
    POPUP.find('button').hide()
    POPUP.fadeToggle()
    POPUP.find('h1').text('Conectando')
    data = {
        'email': login_email.val(),
        'password': login_password.val()
    }
    _ajax('/login/', login, method='POST', data=data)


def chooseNewCharacter(ev):
    if jQuery('.new-character-container').css('display') == 'none':
        jQuery('.character-container').fadeOut(jQuery('.new-character-container').fadeIn)


def renderNewCharacter(ev):
    type = ev.target.attrs['alt']
    new_character_form = jQuery('.new-character-form')
    new_character_form.find('*').remove()
    new_character_form.append(f'<h1>{type}</h1>')
    jQuery('.new-character-choose-type-container').fadeOut(new_character_form.fadeIn)


def renderCharacter(ev):
    index = int(ev.target.attrs['pos'])
    character = user.characters[index]
    document['character-name'].text = character['name']
    document['character-vocation'].text = character['vocation']
    document['character-city'].text = character['city']
    document['character-level'].text = character['level']
    document['character-magic_level'].text = character['magic_level']
    document['character-fist'].text = character['fist']
    document['character-club'].text = character['club']
    document['character-sword'].text = character['sword']
    document['character-axe'].text = character['axe']
    document['character-distance'].text = character['distance']
    document['character-shield'].text = character['shield']
    document['character-fishing'].text = character['fishing']

    jQuery('.new-character-container').fadeOut(jQuery('.character-container').fadeIn)


def initialRender():
    jQuery('.account-containers').hide()
    jQuery('#account-login-container').show()
    jQuery('.character-container').hide()
    jQuery('.new-character-form').hide()
    login_email.val('')

    jQuery('#login-form').on('submit', sendLogin)
    jQuery('#new-character-button').on('click', chooseNewCharacter)
    jQuery('.new-character-choose-type-container').on('click', renderNewCharacter)


initialRender()
