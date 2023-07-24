namespace token {
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
        K_FUNC, K_LET
    };
}