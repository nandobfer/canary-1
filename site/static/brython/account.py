from browser import document, ajax, html, bind, window, alert, timer

jQuery = window.jQuery
user = None
POPUP = jQuery('#floating-popup')

containers = '#home-container>div:not(.moonlight-wolf)'

login_email = jQuery('#login-email')
login_password = jQuery('#login-password')
login_form_text = jQuery('#login-form > p')

signup_email = jQuery('#signup-email')
signup_password = jQuery('#signup-password')

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

class Character():
    def __init__(self):
        self.name = None
        self.type = None
        self.vocation = None
        self.vocation_id = None
        self.race = None
        self.race_id = None
        self.sex = None

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

def renderCharacterList():
     for character in user.characters:
        div = f'<div pos="{user.characters.index(character)}" id="char-{character["id"]}-container" class="account-characters"></div>'
        jQuery('.account-characters-container').append(div)
        p = f'<p pos="{user.characters.index(character)}" id="char-{character["id"]}">{character["name"]}</p>'
        jQuery(f'#char-{character["id"]}-container').append(p)
        jQuery('.account-characters-container').append('<hr>')

        jQuery(
            f'#char-{character["id"]}-container').on('click', renderCharacter)

def login(req):
    data = (eval(req.text))
    if data:
        global user
        if not login_form_text.css('display') == 'none':
            login_form_text.fadeOut()

        user = User(data)
        if user.characters:
            renderCharacterList()

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
    else:
        jQuery('.new-character-form').fadeOut(jQuery('.new-character-choose-type-container').fadeIn)


def renderNewCharacter(ev):
    type = ev.target.attrs['alt']
    print(type)
    new_character_form = jQuery('.new-character-form')
    new_character_form.find('*').remove()
    new_character_form.append(f'<h1>Escolha sua raça</h1>')
    
    character = Character()
    character.type = type
    
    def renderRaces(req):
        data = eval(req.text)
        for item in data:
            button = html.BUTTON(f'{item[1]}', Id=f'race-{item[0]}', Class=f'race-{item[1]}')
            new_character_form.append(button)
            
            def chooseRace(ev):
                character.race = ev.target.attrs['class'].split('-')[1]
                character.race_id = ev.target.attrs['id'].split('-')[1]
                new_character_form.find('*').remove()
                new_character_form.append(f'<h1>Escolha sua classe, {character.race}</h1>')
                def renderClasses(req):
                    data = eval(req.text)
                    for item in data:
                        button = html.BUTTON(f'{item[1]}', Id=f'class-{item[0]}', Class=f'class-{item[1]}')
                        new_character_form.append(button)

                        def chooseClass(ev):
                            character.vocation = ev.target.attrs['class'].split('-')[1]
                            character.vocation_id = ev.target.attrs['id'].split('-')[1]
                            new_character_form.find('*').remove()
                            new_character_form.append(f'<h1>Qual será o nome desse {character.race} {character.vocation}?</h1>')
                            new_character_form.append(f'<input></input>')
                            button = html.BUTTON('Criar Personagem')
                            new_character_form.append(button)
                            
                            def submitNewCharacter(ev):
                                character.name = new_character_form.find('input').val()
                                data = vars(character)
                                data.update({'account_id': user.id})
                                
                                def reloadCharacters(req):
                                    response = eval(req.text)
                                    print(response)
                                    if response:
                                        user.characters.append(response)
                                        jQuery('.account-characters-container > *:not(button)').remove()
                                        renderCharacterList()
                                        renderCharacter(index = len(user.characters)-1)
                                
                                _ajax('/new_character/', reloadCharacters, method='POST', data=data)
                            
                            button.bind('click', submitNewCharacter)
                            
                        button.bind('click', chooseClass)
                        
                _ajax('/get_classes', renderClasses)
                
                
            button.bind('click', chooseRace)
    _ajax('/get_races/', renderRaces, method='POST', data={'type': type})

    jQuery('.new-character-choose-type-container').fadeOut(new_character_form.fadeIn)


def renderCharacter(ev = None, index = None):
    if not index:
        index = int(ev.target.attrs['pos'])
    character = user.characters[index]
    document['character-name'].text = character['name']
    document['character-race'].text = character['race']
    document['character-vocation'].text = character['vocation']
    document['character-city'].text = character['city']
    if character['guild']:
        document['character-guild'].text = character['guild']
        document['character-guild-position'].text = character['guild_position']
    else:
        document['character-guild'].text = 'Nenhuma'
        document['character-guild-position'].text = 'Nenhum'
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


def sendSignUp(ev):
    data = {
        'email': signup_email.val(),
        'password': signup_password.val()
    }

    def signupComplete(req):
        response = eval(req.text)
        toggleContainer('blur')
        POPUP.fadeToggle()
        if response:
            POPUP.find('h1').text(response[0])
            POPUP.find('p').text(response[1])
        else:
            POPUP.find('h1').text('Erro')
            POPUP.find('p').text('Erro')

    _ajax('/signup/', signupComplete, method='POST', data=data)

def initialRender():
    jQuery('.account-containers').hide()
    jQuery('#account-login-container').show()
    jQuery('.character-container').hide()
    jQuery('.new-character-form').hide()
    login_email.val('')

    jQuery('#login-form').on('submit', sendLogin)
    jQuery('#signup-form').on('submit', sendSignUp)
    jQuery('#new-character-button').on('click', chooseNewCharacter)
    jQuery('.new-character-choose-type-container').on('click', renderNewCharacter)


initialRender()
