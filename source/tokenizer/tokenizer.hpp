#pragma once
#include <string>
#include <queue>
#include <istream>

namespace tokenizer {
    enum class TokenType {
        ILLEGAL, // 非法符号
        END, // 文本结束

        IDENTIFIER, // 标识符

        INTEGER, // 整形

        // 运算符
        OP_ASSIGN,
        OP_PLUS,

        // 分隔符
        COMMA,
        SEMICOLON,

        // 括号
        L_PARAN, R_PARAN,
        L_BRACE, R_BRACE,

        // 关键字
        FUNC, LET
    };

    class Tokenizer {
    public:
        Tokenizer(std::istream& in) :input{in} {}
        char next();
        void unread(char c);

    private:
        std::istream& input;
        std::queue<char> buf;
    };
}

namespace tokenizer {
    char Tokenizer::next() {
        char c;
        if (!this->buf.empty()) {
            c = this->buf.front();
            this->buf.pop();
            return c;
        }
        c = this->input.get();
        return c;
    }

    void Tokenizer::unread(char c) {
        this->buf.push(c);
    }
}