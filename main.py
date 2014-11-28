"""
File Name: Main
File: main.py
Project: Peppermint
Created: Nov 22 2014
Author: Emma Jones (AwwCookies)
Version 0.1~Beta
"""
import socket
import json
import time
import thread
import subprocess
import string
import jrpc
from termcolor import cprint


class Peppermint:
    def __init__(self, config="config.json", logfile="peppermint.log"):
        self.config = json.loads(open(config, 'r').read())  # Load in the config file (Should be in JSON)
        self.log_file = logfile
        self.socket = socket.socket()
        self.__buffer = ""
        self.message_q = []
        self.channels = []
        thread.start_new_thread(self.__send_message, (self.config["Message Rate Limit"],))

    def __send_message(self, x):
        while True:
            if len(self.message_q) > 0:
                for msg in self.message_q:
                    self.__send("PRIVMSG %s :%s" % (msg["Channel"], msg["Message"]))
                    self.message_q.pop()
                    time.sleep(x)

    def __parser(self, data):
        for plugin in self.config["Plugins"]:
            output = subprocess.check_output([plugin, json.dumps(data), json.dumps(self.config)])
            # print output #DEBUG
            for cmd in output.split("\n"):
                args = cmd.split()
                if len(args) > 0:
                    # Command: JOIN
                    if args[0] == "/join":
                        if len(args) == 3:
                            self.join(args[1], args[2])
                        else:
                            self.join(args[1])
                    # Command: PART
                    elif args[0] == "/part":
                        if len(args) == 3:
                            self.part(args[1], args[2])
                        else:
                            self.part(args[1])
                    # Command MESSAGE
                    elif args[0] == "/message":
                        self.message(args[1], ' '.join(args[2:]))
                    # Command ME
                    elif args[0] == "/me":
                        self.me(args[1], ' '.join(args[2:]))
                    # Command NICK
                    elif args[0] == "/nick":
                        self.nick(args[1])
                    # Command INVITE
                    elif args[0] == "/invite":
                        self.invite(args[1], args[2])
                    # Command OP
                    elif args[0] == "/op":
                        self.op(args[1], args[2])
                    # Command DEOP
                    elif args[0] == "/deop":
                        self.deop(args[1], args[2])
                    # Command VOICE
                    elif args[0] == "/voice":
                        self.voice(args[1], args[2])
                    # Command DEVOICE
                    elif args[0] == "/devoie":
                        self.devoice(args[1], args[2])
                    # Command BAN
                    elif args[0] == "/ban":
                        self.ban(args[1], args[2])
                    # Command UNBAN
                    elif args[0] == "/unban":
                        self.unban(args[1], args[2])
                    # Command KICK
                    elif args[0] == "/kick":
                        if len(args) == 3:
                            self.kick(args[1], args[2])
                        elif len(args) >= 4:
                            self.kick(args[1], args[2], ' '.join(args[3:]))

    def __connect(self):
        """ Does the initial connection to the IRC Server"""
        cprint("Connecting to %s:%i as %s" % (self.config["Server"], self.config["Server Port"], self.config["Nick"]))
        if len(self.config["Bind"]) > 0:
            self.socket.bind(self.config["Bind"], 0)  # BIND to an specific IP

        self.socket.connect((self.config["Server"], self.config["Server Port"]))  # Connect to IRC Server

        if len(self.config["Server Password"]) > 0:  # If there is a server password
            self.__send("PASS %s" % self.config["Server Password"])

        self.__send("NICK %s" % self.config["Nick"])
        self.__send(
            "USER %s %s %s %s" % (self.config["Nick"], self.config["Server"], "UNUSED", self.config["Real Name"]))

    def __send(self, text):
        self.__log("SEND", text)
        self.socket.send(text + "\r\n")

    def __log(self, name, text):
        cprint("[%s]: %s" % (name, text), "yellow")
        with open(self.log_file, 'a') as log:
            log.write("[%s]: %s" % (name, text) + "\n")

    # ----------------------------------------- #

    def __nick_in_use(self):
        cprint("%s is already in use. Please choose another nick")
        self.nick(str(raw_input("Nick: ")).strip())

    # ----------------------------------------- #

    def __process(self, data):
        if data["Type"] == "*" and "Nickname is already in use" in data["Message"]:
            self.__nick_in_use()
        if data["Type"] == "PRIVMSG" and data["Host"] in self.config["Owner"]:
            args = data["Message"].split()
            if args[0] == "~join":
                self.join(args[1])
            elif args[0] == "~part":
                self.part(args[1])


        self.__parser(data)

    def run(self):
        first_run = True
        self.__connect()
        while True:
            self.__buffer += self.socket.recv(1024)
            tempdata = self.__buffer.replace("!", " !").split()
            try:
                data = {
                    "Nick": tempdata[0].lstrip(":"),
                    "Host": tempdata[1].replace("!", ""),
                    "Type": tempdata[2],
                    "Channel": tempdata[3],
                    "Message": ' '.join(tempdata[4:]).lstrip(":")
                }
            except:
                pass

            data["First Run"] = first_run
            self.__process(data)
            first_run = False

            # Check For PING!
            temp = string.split(self.__buffer, "\n")
            self.__buffer = temp.pop()

            for line in temp:
                line = string.rstrip(line)
                line = string.split(line)

                if line[0] == "PING":
                    self.__send("PONG %s" % line[1])
            print data
            self.__buffer = ""
            data = {"Nick": "", "Host": "", "Type": "", "Channel": "", "Message": ""}

    # ---- Builtin Functions ---- #
    def me(self, channel, message):
        self.message(channel, "\x01ACTION " + message + "\x01")

    def message(self, channel, message):
        if self.config["Approved Channels"]:
            self.message_q.append({"Channel": channel, "Message": message})

    def join(self, channel, password=None):
        if password:
            self.__send("JOIN %s %s" % (channel, password))
        else:
            self.__send("JOIN %s" % channel)

    def part(self, channel, message="Mmm Fresh!"):
        self.__send("PART %s :%s" % (channel, message))

    def nick(self, newnick):
        """Change the bots nick. Returns the old bot nick"""
        old_nick = self.config["Nick"]
        self.config["Nick"] = newnick
        self.__send("NICK %s" % newnick)
        return old_nick

    def invite(self, channel, nick):
        self.__send("INVITE %s %s" % (nick, channel))

    def op(self, channel, nick):
        self.__send("MODE %s +o %s" % (channel, nick))

    def deop(self, channel, nick):
        self.__send("MODE %s -o %s" % (channel, nick))

    def voice(self, channel, nick):
        self.__send("MODE %s +v %s" % (channel, nick))

    def devoice(self, channel, nick):
        self.__send("MODE %s -v %s" % (channel, nick))

    def kick(self, channel, nick, msg="GTFO"):
        self.__send("KICK %s %s :%s" % (channel, nick, msg))

    def ban(self, channel, host):
        self.__send("MODE %s +b %s" % (channel, host))

    def unban(self, channel, host):
        self.__send("MODE %s -b %s" % (channel, host))

    def mute(self, channel, host):
        pass


    # ---- --------------- ---- #


bot = Peppermint()
bot.run()