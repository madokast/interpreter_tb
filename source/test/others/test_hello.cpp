#include <gtest/gtest.h>
#include <string>

TEST(HelloTest, StringEq) {
    std::string h {"hello"};
    std::string w {"world"};
    EXPECT_STREQ(h.c_str(), "hello");
    EXPECT_STREQ(w.c_str(), "world");
}

TEST(HelloTest, NormalEq) {
    std::string h {"hello"};
    std::string w {"world"};
    EXPECT_EQ(h, "hello");
    EXPECT_EQ(w, "world");
}