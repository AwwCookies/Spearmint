//
//  peppermint.h
//  Peppermint
//
//  Created by Emma Jones on 11/25/14.
//  Copyright (c) 2014 AwwCookies. All rights reserved.
//

#ifndef __Peppermint__
#define __Peppermint__

#include <iostream>

namespace Peppermint {
    void message(const char* channel, const char* msg) {
        printf("/message %s %s\n", channel, msg);
    }

    void me(const char* channel, const char* msg) {
        printf("/me %s %s\n", channel, msg);
    }

    void join(const char* channel) {
        printf("/join %s\n", channel);
    }

    void join(const char* channel, const char* password) {
        printf("/join %s %s\n", channel, password);
    }

    void part(const char* channel) {
        printf("/part %s\n", channel);
    }

    void part(const char* channel, const char* msg) {
        printf("/part %s %s\n", channel, msg);
    }

    void nick(const char* newnick) {
        printf("/nick %s\n", newnick);
    }

    void invite(const char* nick, const char* channel) {
        printf("/invite %s %s\n", nick, channel);
    }

    void op(const char* channel, const char* nick) {
        printf("/op %s %s\n", channel, nick);
    }

    void deop(const char* channel, const char* nick) {
        printf("/deop %s %s\n", channel, nick);
    }

    void voice(const char* channel, const char* nick) {
        printf("/voice %s %s\n", channel, nick);
    }

    void devoice(const char* channel, const char* nick) {
        printf("/devoice %s %s\n", channel, nick);
    }
}
#endif /* defined(__Peppermint__) */
