#include "sms_service.h"

SmsService::SmsService(std::string api_key, std::string from_number)
    : api_key_(std::move(api_key)),
      from_number_(std::move(from_number)) {
}

bool SmsService::send(const std::string& phone, const std::string& message) const {
    return !api_key_.empty() && !from_number_.empty() && !phone.empty() && !message.empty();
}
