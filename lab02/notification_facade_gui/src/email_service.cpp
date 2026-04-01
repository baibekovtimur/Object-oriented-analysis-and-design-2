#include "email_service.h"

EmailService::EmailService(std::string host, int port, std::string username, std::string password)
    : host_(std::move(host)),
      port_(port),
      username_(std::move(username)),
      password_(std::move(password)) {
}

bool EmailService::send(const std::string& to, const std::string& message) const {
    return !host_.empty() && port_ > 0 && !username_.empty() && !password_.empty() &&
           !to.empty() && !message.empty();
}
