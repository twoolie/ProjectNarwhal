import time, sys, traceback
from optparse import make_option
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower
from threading import Thread, Event


from django.core.management.base import BaseCommand, CommandError

from narwhal.core.torrent.models import Torrent

from djboss.commands import *

#@command(description='Run an ircbot that responds to commands in chat.')
#@argument('host', help='The server to connect to.')
#@argument('port', type=int, default=6667, help="Port irc runs on (default:%(default)s)")
#@argument('channel', help='The channel to join.')
#@argument('nick', default='torrentbot', help='The nick for the bot. (default:%(default)s)')

class Command(BaseCommand):
    args = 'host port channel name'
    help = 'Runs a IRC bot'
    option_list = BaseCommand.option_list + (
        make_option('--host', action='store', dest='server', help='The server to connect to.'),
        make_option('--port', action='store', dest='port', type=int, default=6667, help="Port irc runs on (default:%(default)s)"),
        make_option('--channel', action='store', dest='channel', help='The channel to join.'),
        make_option('--nick', action='store', dest='nickname', default='torrentbot', help='The nick for the bot. (default:%(default)s)'),
        )

    def handle(self, **kwargs):
        try:
            tb = TorrentBot(**kwargs)
            tb.start()
        except KeyboardInterrupt:
            print "Shutting down."

class OutputManager(Thread):
    def __init__(self, connection, delay=.5):
        Thread.__init__(self)
        self.setDaemon(1)
        self.connection = connection
        self.delay = delay
        self.event = Event()
        self.queue = []

    def run(self):
        while 1:
            self.event.wait()
            while self.queue:
                msg,target = self.queue.pop(0)
                self.connection.privmsg(target, msg)
                time.sleep(self.delay)
            self.event.clear()

    def send(self, msg, target):
        self.queue.append((msg,target))
        self.event.set()

class TorrentBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port, **kwargs):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.nickname = nickname
        self.queue = OutputManager(self.connection)
        self.queue.start()
        self.start()

    def on_nicknameinuse(self, c, e):
        self.nickname = c.get_nickname() + "_"
        c.nick(self.nickname)

    def on_welcome(self, c, e):
        c.join(self.channel)
        
    def on_pubmsg(self, c, e):
        from_nick = nm_to_n(e.source())
        a = str.split(e.arguments()[0], ":", 1)
        if len(a) > 1 and irc_lower(a[0]) == irc_lower(self.nickname):
            self.do_command(e, c, str.strip(a[1]), from_nick)
    
    def on_privmsg(self, c, e):
        from_nick = nm_to_n(e.source())
        self.do_command(e, c, str.strip(e.arguments()[0]), from_nick)

    def say_public(self, text):
        "Print TEXT into public channel, for all to see."
        for line in text.split("\n"):
            self.queue.send(line, self.channel)

    def say_private(self, nick, text):
        "Send private message of TEXT to NICK."
        for line in text.split("\n"):
            self.queue.send(line, nick)

    def reply(self, e, text):
        "Send TEXT to public channel or as private msg, in reply to event E."
        if e.eventtype() == "pubmsg":
            self.say_public("%s: %s" % (nm_to_n(e.source()), text))
        else:
            self.say_private(nm_to_n(e.source()), text)

    def do_command(self, e, c, cmd, from_nick):
        try:
            if cmd == 'echo':
                self.reply(e, "Wow, there is an echo here")
            
            if cmd.startswith('count'):
                ans =""
                words = cmd.split(" ")
                while True:
                    mcmd = words.pop(0)
                    model = words.pop(0)
                    if model=='torrents':
                        qs = Torrent.objects.all()
                    #if model=='anime':
                    #    qs = Anime.objects.all()
                    
                    if not words:
                        break
                
                if mcmd == 'count':
                    ans += '%s %s '% (qs.count(), model)
                self.reply(e, ans)
            
            if cmd.startswith('search'):
                from django.utils.text import smart_split
                query = smart_split(cmd.lsplit(" ")[1])
                if len(query) == 1:
                    pass
                
                
            if cmd == 'help':
                self.say_private(from_nick, 
"""Commands:
    help             Display this message.
    search "query"   search the tracker""")
            else:
                self.reply(e, "I don't understand '%s'."%(cmd))
        except:
            self.reply(e, "Ow, you hurt my brain.")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)



