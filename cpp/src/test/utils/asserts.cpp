#include <iostream>

namespace it_test {
    void assert_true(bool b) {
        if (!b) {
            throw "assert fail";
        }
    }
}