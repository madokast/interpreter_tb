#include "utils.h"
#include <iostream>

const char *_debug0 = "[  DEBUG   ] ";
const char *_debug1 = "[   DEBUG  ] ";

void debug_print(std::string_view sv)
{
    static int t = 1;
    if (TEST_DEBUG)
    {
        std::cout << (++t % 2 == 0 ? _debug0 : _debug1) << sv << "\n";
    }
}

void debug_print(char c) {
    std::string s;
    s += c;
    debug_print(s);
}