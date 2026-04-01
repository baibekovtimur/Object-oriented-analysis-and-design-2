#pragma once

#include <string>

class EmailService {
public:
    EmailService(std::string host, int port, std::string username, std::string password);

    bool send(const std::string& to, const std::string& message) const;

private:
    std::string host_;
    int port_;
    std::string username_;
    std::string password_;
};
