from handlers.ca_action import lang_setter 


async def setter_lang(language):
    
    lang_setter.lang = language

async def getter_lang():
    # language = lang_setter()
    return lang_setter.lang


