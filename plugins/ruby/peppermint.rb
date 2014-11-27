module Peppermint
    def Peppermint.message(channel, message)
        puts "/message #{channel} #{message}"
    end

    def Peppermint.me(channel, message)
        puts "/me #{channel} #{message}"
    end

    def Peppermint.join(channel, password="")
        if password != ""
            puts "/join #{channel} #{password}"
        else
            puts "/join #{channel}"
        end
    end

    def Peppermint.part(channel, message="Mmm Fresh!")
        puts "/part #{channel} #{message}"
    end

    def Peppermint.nick(newnick)
        puts "/nick #{newnick}"
    end

    def Peppermint.invite(channel, nick)
        puts "/invite #{channel} #{nick}"
    end

    def Peppermint.op(channel, nick)
        puts "/op #{channel} #{nick}"
    end

    def Peppermint.deop(channel, nick)
        puts "/deop #{channel} #{nick}"
    end

    def Peppermint.voice(channel, nick)
        puts "/voice #{channel} #{nick}"
    end

    def Peppermint.devoice(channel, nick)
        puts "/devoice #{channel} #{nick}"
    end
end