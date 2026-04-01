#include "validator.h"

#include <regex>

bool Validator::is_valid_email(const std::string& value) const {
    static const std::regex email_pattern(R"(^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$)");
    return std::regex_match(value, email_pattern);
}

bool Validator::is_valid_phone(const std::string& value) const {
    static const std::regex phone_pattern(R"(^\+?[0-9]{10,15}$)");
    return std::regex_match(value, phone_pattern);
}

bool Validator::is_valid_push_token(const std::string& value) const {
    static const std::regex token_pattern(R"(^[A-Za-z0-9:_-]{10,}$)");
    return std::regex_match(value, token_pattern);
}
