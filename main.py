import socket
import json
import time
import subprocess
from termcolor import cprint


class Spearmint:
    def __init__(self, config="config.json", logfile="spearmint.log"):
        self.config = json.loads(open(config, 'r').read())  # Load in the config file (Should be in JSON)
        self.log_file = logfile
        self.socket = socket.socket()
        self.buffer = ""
        self.channels = []

    def parser(self, data):
        for plugin in self.config["Plugins"]:
            # print data
            output = subprocess.check_output([plugin, data, json.dumps(self.config)])
            # print output #DEBUG
            for cmd in output.split("\n"):
                args = cmd.split()
                if len(args) > 0:
                    if args[0] == "quit":
                        self.quit(message=' '.join(args[1:]))
                    elif args[0] == "nick":
                        self.nick(nick=args[1])
                    elif args[0] == "usernote":
                        self.usernote(nick=args[1], message=' '.join(args[2:]))
                    elif args[0] == "userflag":
                        self.userflag(switch=args[1], flag=args[2])
                    elif args[0] == "chanlist":
                        self.chanlist()
                    elif args[0] == "register":
                        self.register(password=args[1], email=args[2])
                    elif args[0] == "login":
                        self.login(password=args[1])
                    elif args[0] == "logout":
                        self.logout()
                    elif args[0] == "setpass":
                        self.setpass(password=args[1])
                    elif args[0] == "usermsg":
                        self.usermsg(nick=args[1], message=' '.join(args[2:]))
                    elif args[0] == "whois":
                        self.whois(nick=args[1])
                    elif args[0] == "chanjoin":
                        self.chanjoin(channel=args[1], password=' '.join(args[2:]))
                    elif args[0] == "chanpart":
                        self.chanpart(channel=args[1], message=' '.join(args[2:]))
                    elif args[0] == "chanmsg":
                        self.chanmsg(channel=args[1], message=' '.join(args[2:]))
                    elif args[0] == "chankick":
                        self.chankick(channel=args[1], nick=args[2], reason=' '.join(args[3:]))
                    elif args[0] == "chanflag":
                        self.chanflag(channel=args[1], switch=args[2], flag=args[3], args=' '.join(args[4:]))
                    elif args[0] == "chanban":
                        self.chanban(channel=args[1], nick=args[2])
                    elif args[0] == "chanunban":
                        self.chanunban(channel=args[1], IP=args[2])
                    elif args[0] == "chanregister":
                        self.chanregister(channel=args[1])
                    elif args[0] == "chanbadword":
                        self.chanbadword(channel=args[1], switch=args[2], word=args[3])
                    elif args[0] == "chanclientflags":
                        self.chanclientflag(channel=args[1], switch=args[2], nick=args[3], flag=args[4])
                    elif args[0] == "chanusers":
                        self.chanusers(channel=args[1])
                    elif args[0] == "oper":
                        self.oper(password=' '.join(args[1:]))
                    elif args[0] == "kill":
                        self.kill(nick=args[1])
                    elif args[0] == "sanick":
                        self.sanick(nick=args[1], newnick=args[2])
                    elif args[0] == "sajoin":
                        self.sajoin(nick=args[1], channel=args[2])
                    elif args[0] == "sapart":
                        self.sapart(nick=args[1], channel=args[2])
                    elif args[0] == "serverban":
                        self.serverban(IP=args[1])
                    elif args[0] == "globalmsg":
                        self.globalmsg(message=' '.join(args[1:]))
                    elif args[0] == "opermsg":
                        self.opermsg(message=' '.join(args[1:]))

    def connect(self):
        """ Does the initial connection to the IRC Server"""
        cprint("Connecting to %s:%i as %s" % (self.config["Server"], self.config["Server Port"], self.config["Nick"]))
        if len(self.config["Bind"]) > 0:
            self.socket.bind(self.config["Bind"], 0)  # BIND to an specific IP
        self.socket.connect((self.config["Server"], self.config["Server Port"]))  # Connect to IRC Server
        self.send("%s" % self.config["Nick"])
        time.sleep(1)

    def send(self, text):
        # self.log("SEND", text)
        self.socket.send(text)

    def log(self, name, text):
        cprint("[%s]: %s" % (name, text), "yellow")
        with open(self.log_file, 'a') as log:
            log.write("[%s]: %s" % (name, text) + "\n")

    # ----------------------------------------- #

    def run(self):
        first_run = True
        self.connect()
        while True:
            if first_run:
                self.send("chanjoin #test")
            self.buffer = self.socket.recv(9999)
            for line in self.buffer.split("\n"):
                if not line == "":
                    try:
                        self.parser(line)
                    except:
                        pass
            first_run = False
    # ---- Builtin Functions ---- #
    def quit(self, message="quit"):
        """
        Disconnects you from the server
        """
        self.send("quit %s" % message)

    def nick(self, nick):
        """
        Changes your nick
        """
        self.send("nick %s" % nick)

    def usernote(self, nick, message):
        """
        Leave a note for a registered user
        while they're away
        """
        self.send("usernote %s %s" % (nick, message))

    def userflag(self, switch, flag):
        """
        Add or remove a flag from yourself
        """
        self.send("userflag %s %s" % (switch, flag))

    def chanlist(self):
        """
        Returns a list of all public channels
        All channels if oper
        """
        self.send("chanlist")

    def register(self, password, email):
        """
        Register an account on the server
        """
        self.send("register %s %s" % (password, email))

    def login(self, password):
        """
        Login to your account
        """
        self.send("login %s" % password)

    def logout(self, password):
        """
        Logout of your account
        """
        self.send("logout")

    def setpass(self, password):
        """
        Change your account password
        """
        self.send("setpass %s" % password)

    def usermsg(self, nick, message):
        """
        Send a message to another client on
        the server
        """
        self.send("usermsg %s %s" % (nick, message))

    def whois(self, nick):
        """
        Gives you information on a client
        """
        self.send("whois %s" % nick)

    def chanjoin(self, channel, password=None):
        """
        Join a channel
        """
        if password:
            self.send("chanjoin %s %s" % (channel, password))
        else:
            self.send("chanjoin %s" % channel)

    def chanpart(self, channel, message="bye"):
        """
        Leave a channel
        """
        self.send("chanpart %s %s" % (channel, message))

    def chanmsg(self, channel, message):
        """
        Send a message to a channel
        """
        self.send("chanmsg %s %s" % (channel, message))

    def chankick(self, channel, nick, reason):
        """
        Kick a user from the channel
        """
        self.send("chankick %s %s %s" % (channel, nick, reason))

    def chanflag(self, channel, switch, flag, args):
        """
        Set a channel flag
        """
        self.send("chanflag %s %s %s %s" % (channel, switch, flag, args))

    def chanban(self, channel, nick):
        """
        Bans a user form the channel
        """
        self.send("chanban %s %s" % (channel, nick))

    def chanunban(self, channel, IP):
        """
        Unbans an IP from the channel
        """
        self.send("chanunban %s %s" % (channel, IP))

    def chanregister(self, channel):
        """
        Registers a channel to you
        """
        self.send("chanregister %s" % channel)

    def chanbadword(self, channel, switch, word):
        """
        Add or remove a badword
        """
        self.send("chanbanword %s %s %s" % (channel, switch, word))

    def chanclientflag(self, channel, switch, nick, flag):
        """
        Add or remove a channel client flag
        """
        self.send("chanclientflag %s %s %s %s" % (channel, switch, nick, flag))

    def chanusers(self, channel):
        """
        Gives a list of users in a channel
        """
        self.send("chanusers %s" % channel)

    def oper(self, password):
        """
        login as an oper
        """
        self.send("oper %s" % password)

    def kill(self, nick):
        """
        Removes a client from the server
        """
        self.send("kill %s" % nick)

    def sanick(self, nick, newnick):
        """
        Forcefully change a users nick
        """
        self.send("sanick %s %s" % (nick, newnick))

    def sajoin(self, nick, channel):
        """
        Force a client into a channel
        """
        self.send("sajoin %s %s" % (nick, channel))

    def sapart(self, nick, channel):
        """
        Force a client to leave a channel
        """
        self.send("sapart %s %s" % (nick, channel))

    def serverban(self, IP):
        """
        Ban an IP from the server
        """
        self.send("serverban %s" % IP)

    def globalmsg(self, message):
        """
        Send a message to all clients connected to the server
        """
        self.send("globalmsg %s" % message)

    def opermsg(self, message):
        """
        Send a message to all opers on the server
        """
        self.send("opermsg %s" % message)
    # ---- --------------- ---- #


bot = Spearmint(config="config.json", logfile="spearmint.log")
bot.run()
