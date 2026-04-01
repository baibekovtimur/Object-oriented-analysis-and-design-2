#pragma once

#include <string>

class SmsService {
public:
    SmsService(std::string api_key, std::string from_number);

    bool send(const std::string& phone, const std::string& message) const;

private:
    std::string api_key_;
    std::string from_number_;
};
