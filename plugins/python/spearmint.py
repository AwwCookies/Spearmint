import os
import json
import re


def get_data(argv):
    """ Returns a dict containg details of the IRC event"""
    return json.loads(argv[1])

def get_config(argv):
    """ Returns a dict containg the configuration properties"""
    return json.loads(argv[2])

def get_dc(argv):
    """Returns both data and config as a tuple"""
    return (get_data(argv), get_config(argv))

def init(argv, filename):
    """Returns data, the config, and gets the json data from the file"""
    return (get_data(argv), get_config(argv), load(filename))

def quit(message="quit"):
    """
    Disconnects you from the server
    """
    print("quit %s" % message)

def nick(nick):
    """
    Changes your nick
    """
    print("nick %s" % nick)

def usernote(nick, message):
    """
    Leave a note for a registered user
    while they're away
    """
    print("usernote %s %s" % (nick, message))

def userflag(switch, flag):
    """
    Add or remove a flag from yourself
    """
    print("userflag %s %s" % (switch, flag))

def chanlist(self):
    """
    Returns a list of all public channels
    All channels if oper
    """
    print("chanlist")

def register(password, email):
    """
    Register an account on the server
    """
    print("register %s %s" % (password, email))

def login(password):
    """
    Login to your account
    """
    print("login %s" % password)

def logout(password):
    """
    Logout of your account
    """
    print("logout")

def setpass(password):
    """
    Change your account password
    """
    print("setpass %s" % password)

def usermsg(nick, message):
    """
    Send a message to another client on
    the server
    """
    print("usermsg %s %s" % (nick, message))

def whois(nick):
    """
    Gives you information on a client
    """
    print("whois %s" % nick)

def chanjoin(channel, password=None):
    """
    Join a channel
    """
    if password:
        print("chanjoin %s %s" % (channel, password))
    else:
        print("chanjoin %s" % channel)

def chanpart(channel, message="bye"):
    """
    Leave a channel
    """
    print("chanpart %s %s" % (channel, message))

def chanmsg(channel, message):
    """
    Send a message to a channel
    """
    print("chanmsg %s %s" % (channel, message))

def chankick(channel, nick, reason):
    """
    Kick a user from the channel
    """
    print("chankick %s %s %s" % (channel, nick, reason))

def chanflag(channel, switch, flag, args):
    """
    Set a channel flag
    """
    print("chanflag %s %s %s %s" % (channel, switch, flag, args))

def chanban(channel, nick):
    """
    Bans a user form the channel
    """
    print("chanban %s %s" % (channel, nick))

def chanunban(channel, IP):
    """
    Unbans an IP from the channel
    """
    print("chanunban %s %s" % (channel, IP))

def chanregister(channel):
    """
    Registers a channel to you
    """
    print("chanregister %s" % channel)

def chanbadword(channel, switch, word):
    """
    Add or remove a badword
    """
    print("chanbanword %s %s %s" % (channel, switch, word))

def chanclientflag(channel, switch, nick, flag):
    """
    Add or remove a channel client flag
    """
    print("chanclientflag %s %s %s %s" % (channel, switch, nick, flag))

def chanusers(channel):
    """
    Gives a list of users in a channel
    """
    print("chanusers %s" % channel)

def oper(password):
    """
    login as an oper
    """
    print("oper %s" % password)

def kill(nick):
    """
    Removes a client from the server
    """
    print("kill %s" % nick)

def sanick(nick, newnick):
    """
    Forcefully change a users nick
    """
    print("sanick %s %s" % (nick, newnick))

def sajoin(nick, channel):
    """
    Force a client into a channel
    """
    print("sajoin %s %s" % (nick, channel))

def sapart(nick, channel):
    """
    Force a client to leave a channel
    """
    print("sapart %s %s" % (nick, channel))

def serverban(IP):
    """
    Ban an IP from the server
    """
    print("serverban %s" % IP)

def globalmsg(message):
    """
    Send a message to all clients connected to the server
    """
    print("globalmsg %s" % message)

def opermsg(message):
    """
    Send a message to all opers on the server
    """
    print("opermsg %s" % message)

# ----- Files ----- #

def load(filename):
    fpath = "storage/" + filename + ".json"
    if os.path.exists(fpath):
        return json.loads(open(fpath, 'r').read())
    else:
        return {}

def save(filename, data):
    fpath = "storage/" + filename + ".json"
    with open(fpath, 'w') as f:
        f.write(json.dumps(data, sort_keys=True, indent=2, separators=(',', ': ')))

def remove(filename):
    fpath = "storage/" + filename + ".json"
    os.remove(fpath)
