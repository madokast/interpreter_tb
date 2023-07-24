#include "tokenizer.hpp"
#include "asserts.h"
#include <iostream>
#include <string>
#include <sstream>

namespace test_tokenizer {
    void read_empty() {
        std::string empty_str;
        std::stringstream ss {empty_str};
        tokenizer::SourceReader sr {ss};
        char c = sr.next();
        std::cout << std::to_string(int{c}) << std::endl;
        it_test::assert_true(c == EOF);
    }

    void read() {
        const char* str = "hello";
        std::string empty_str {str};
        std::stringstream ss {empty_str};
        tokenizer::SourceReader sr {ss};
        char r[] = {0, '\0'};
        for (size_t i = 0; i < empty_str.size(); i++) {
            char c = sr.next();
            r[0] = c;
            std::cout << r << std::endl;
            it_test::assert_true(c == *(str+i));
        }
    }

    void run() {
        ITTEST(test_tokenizer, read_empty);
        ITTEST(test_tokenizer, read);
    }
}