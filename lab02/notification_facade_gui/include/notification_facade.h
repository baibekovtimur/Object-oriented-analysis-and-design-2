#pragma once

#include <memory>
#include <string>
#include <vector>

class EmailService;
class SmsService;
class PushService;
class Validator;
class NotificationLogger;

class NotificationFacade {
public:
    struct Recipient {
        std::string email;
        std::string phone;
        std::string push_token;
    };

    NotificationFacade(std::shared_ptr<EmailService> email_service,
                       std::shared_ptr<SmsService> sms_service,
                       std::shared_ptr<PushService> push_service,
                       std::shared_ptr<Validator> validator,
                       std::shared_ptr<NotificationLogger> logger);

    void send_notification(const Recipient& recipient,
                           const std::string& message,
                           const std::vector<std::string>& channels) const;

private:
    std::shared_ptr<EmailService> email_service_;
    std::shared_ptr<SmsService> sms_service_;
    std::shared_ptr<PushService> push_service_;
    std::shared_ptr<Validator> validator_;
    std::shared_ptr<NotificationLogger> logger_;
};
