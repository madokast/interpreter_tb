#include <utils.h>
#include <tokenizer.hpp>
#include <gtest/gtest.h>
#include <string>
#include <sstream>

TEST(Tokenizer, ReadChar)
{
    char c;
    std::string h{"ab123"};
    const char* s = h.c_str();
    std::stringstream ss {h};
    tokenizer::Tokenizer t {ss};

    for (size_t i = 0; i < h.size(); i++)
    {
        c = t.next();
        debug_print(c);
        ASSERT_EQ(c, *(s+i));
    }
}

TEST(Tokenizer, UNREAD)
{
    char c;
    std::string h{"mdk321"};
    const char* s = h.c_str();
    std::stringstream ss;
    tokenizer::Tokenizer t {ss};

    for (size_t i = 0; i < h.size(); i++)
    {
        t.unread(*(s+i));
    }

    for (size_t i = 0; i < h.size(); i++)
    {
        c = t.next();
        debug_print(c);
        ASSERT_EQ(c, *(s+i));
    }
}

TEST(Tokenizer, READ_END)
{
    char c;
    std::string h{"zrx987"};
    const char* s = h.c_str();
    std::stringstream ss;
    tokenizer::Tokenizer t {ss};

    for (size_t i = 0; i < h.size(); i++)
    {
        c = t.next();
        debug_print(std::to_string(int{c}));
        ASSERT_EQ(c, EOF);
    }
}