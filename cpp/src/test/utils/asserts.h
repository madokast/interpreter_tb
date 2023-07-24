#include <iostream>
#include <cstdio>
#define ITTEST(ns, fn) std::printf("%s::%s\n", #ns,#fn); fn();

namespace it_test {
    void assert_true(bool);
}