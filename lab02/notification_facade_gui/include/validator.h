#pragma once

#include <string>

class Validator {
public:
    bool is_valid_email(const std::string& value) const;
    bool is_valid_phone(const std::string& value) const;
    bool is_valid_push_token(const std::string& value) const;
};
