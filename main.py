"""CCBot."""
import urllib
import json
import os


def lambda_handler(event='', context=''):
    """handler."""
    response = Telegram(json.loads(event['body'])).parse()
    return {"statusCode": '200', "body": response}


"""Change."""


class Change:
    """Change.class."""

    PRICE_API = "https://min-api.cryptocompare.com/data/price"

    f = 'BTC'
    t = 'USD'

    def __init__(self, f='', t=''):
        """Change.__init__."""
        if(f != ''):
            self.f = f.upper()
        if(t != ''):
            self.t = t.upper()

    def get_value(self):
        """Change.get_value."""
        query = "?fsym={}&tsyms={}".format(self.f, self.t)
        value = json.loads(urllib.urlopen(self.PRICE_API + query).read())
        try:
            return "1 {} is worth {} {}".format(self.f, value[self.t], self.t)
        except KeyError:
            return value['Message']


"""Telegram."""


class Telegram:
    """Telegram.class."""

    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
    TELEGRAM_API = "https://api.telegram.org/bot{}".format(TELEGRAM_TOKEN)
    TELEGRAM_UPDATES = TELEGRAM_API + '/getUpdates'
    TELEGRAM_REPLY = TELEGRAM_API + '/sendMessage'

    update = {}

    def __init__(self, update):
        """Telegram.__init__."""
        self.update = update

    def parse(self):
        """Telegram.parse."""
        response = ''
        if 'message' in self.update and 'text' in self.update['message']:
            words = self.update['message']['text'].split(' ')
            mode = words.pop(0)
            if mode.lower() == 'value':
                text = Change(*words).get_value()
                response = self.__reply(text)
        return response

    def __reply(self, text):
        """Telegram.reply."""
        chat = self.update['message']['chat']['id']
        query = "?text={}&chat_id={}".format(text, chat)
        return urllib.urlopen(self.TELEGRAM_REPLY + query).read()
