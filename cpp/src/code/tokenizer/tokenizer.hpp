#pragma once
#include <string>
#include <queue>
#include <istream>

namespace tokenizer {
    // 原代码读取器
    class SourceReader {
    public:
        SourceReader(std::istream& in) :input{in} {}
        char next(); // 读一个字符
        void unread(char c); // 放入一个字符，用于重读

    private:
        std::istream& input;
        std::queue<char> buf;
    };
}

namespace tokenizer {
    char SourceReader::next() {
        char c;
        if (!this->buf.empty()) {
            c = this->buf.front();
            this->buf.pop();
            return c;
        }
        c = this->input.get();
        return c;
    }

    void SourceReader::unread(char c) {
        this->buf.push(c);
    }
}