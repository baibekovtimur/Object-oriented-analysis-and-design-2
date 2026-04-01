#include "push_service.h"

PushService::PushService(std::string fcm_key)
    : fcm_key_(std::move(fcm_key)) {
}

bool PushService::send(const std::string& token, const std::string& message) const {
    return !fcm_key_.empty() && !token.empty() && !message.empty();
}
