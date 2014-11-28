def message(channel, message):
    print "/message %s %s" % (channel, message)

def me(channel, message):
    print "/me %s %s" % (channel, message)

def join(channel, password=""):
    if not password == "":
        print "/join %s %s" % (channel, password)
    else:
        print "/join %s" % channel
    
def part(channel, message="Mmm Fresh!"):
    print "/part %s %s" % (channel, message)

def nick(newnick):
    print "/nick %s" % newnick

def invite(channel, nick):
    print "/invite %s %s" % (channel, nick)

def op(channel, nick):
    print "/op %s %s" % (channel, nick)

def deop(channel, nick):
    print "/deop %s %s" % (channel, nick)

def voice(channel, nick):
    print "/voice %s %s" % (channel, nick)

def devoice(channel, nick):
    print "/devoice %s %s" % (channel, nick)

def kick(channel, nick, msg="GTFO"):
    print "/kick %s %s %s" % (channel, nick, msg)

def ban(channel, host):
    print "/ban %s %s" % (channel, host)

def unban(channel, host):
    print "/unban %s %s" % (channel, host)