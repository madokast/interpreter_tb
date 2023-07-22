#include <utils.h>
#include <gtest/gtest.h>
#include <string>
#include <sstream>

TEST(ISteam, FromString)
{
    std::string h{"hello, world"};
    std::basic_stringbuf ss {h};
    debug_print(ss.str());
    debug_print(h);
    ASSERT_EQ(ss.str(), h);
}

TEST(ISteam, ReadChar)
{
    char c;
    std::string h{"hello, world"};
    std::stringstream ss {h};
    const char * s = h.c_str();

    for (size_t i = 0; i < h.size(); i++)
    {
        c = ss.get();
        debug_print(c);
        ASSERT_EQ(c, *(s+i));
    }
}