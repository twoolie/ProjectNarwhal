import time
from argparse import make_option
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower
from threading import Thread, Event

from django.core.management.base import BaseCommand, CommandError

from narwhal.core.torrent.models import Torrent

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'
    option_list = (
        make_option('--host', action='store', dest='server', help='The server to connect to.'),
        make_option('--port', action='store', dest='port', default=6667, help="Port irc runs on (default:%(default)s)"),
        make_option('--channel', action='store', dest='channel', help='The channel to join.'),
        make_option('--name', action='store', dest='name', default='torrentbot', help='The nick for the bot. (default:%(default)s)'),
        )
    
    def handle(self, *args):
        try:
            tb = TorrentBot(*args)
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
    self.queue.append((msg.strip(),target))
    self.event.set()

class TorrentBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.nickname = nickname
        self.queue = botcommon.OutputManager(self.connection)
        self.queue.start()
        self.start()

    def on_nicknameinuse(self, c, e):
        self.nickname = c.get_nickname() + "_"
        c.nick(self.nickname)

    def on_welcome(self, c, e):
        c.join(self.channel)
        
    def on_pubmsg(self, c, e):
        from_nick = nm_to_n(e.source())
        a = string.split(e.arguments()[0], ":", 1)
        if len(a) > 1 and irc_lower(a[0]) == irc_lower(self.nickname):
            self.do_command(e, string.strip(a[1]), from_nick)
            
    def do_command(self, e, cmd, from_private):
        """ IMPLEMENT LOGIC HERE """
        pass




