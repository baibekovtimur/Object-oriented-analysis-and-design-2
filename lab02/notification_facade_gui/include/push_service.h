#pragma once

#include <string>

class PushService {
public:
    explicit PushService(std::string fcm_key);

    bool send(const std::string& token, const std::string& message) const;

private:
    std::string fcm_key_;
};
