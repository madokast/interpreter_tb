#include "asserts.h"
#include <iostream>

namespace test_hello {
    void hello() {
        std::cout << "hello it-test" << std::endl;
        it_test::assert_true(true);
    }

    void run() {
        ITTEST(test_hello, hello);
    }
}