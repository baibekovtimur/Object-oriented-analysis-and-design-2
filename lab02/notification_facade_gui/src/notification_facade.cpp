#include "notification_facade.h"

#include "email_service.h"
#include "notification_logger.h"
#include "push_service.h"
#include "sms_service.h"
#include "validator.h"

NotificationFacade::NotificationFacade(std::shared_ptr<EmailService> email_service,
                                       std::shared_ptr<SmsService> sms_service,
                                       std::shared_ptr<PushService> push_service,
                                       std::shared_ptr<Validator> validator,
                                       std::shared_ptr<NotificationLogger> logger)
    : email_service_(std::move(email_service)),
      sms_service_(std::move(sms_service)),
      push_service_(std::move(push_service)),
      validator_(std::move(validator)),
      logger_(std::move(logger)) {
}

void NotificationFacade::send_notification(const Recipient& recipient,
                                           const std::string& message,
                                           const std::vector<std::string>& channels) const {
    if (channels.empty()) {
        logger_->log("system", "-", message, false, "No channels selected");
        return;
    }

    if (message.empty()) {
        for (const auto& channel : channels) {
            logger_->log(channel, "-", message, false, "Message is empty");
        }
        return;
    }

    for (const auto& channel : channels) {
        if (channel == "email") {
            if (!validator_->is_valid_email(recipient.email)) {
                logger_->log("email", recipient.email, message, false, "Invalid email format");
                continue;
            }

            const bool result = email_service_->send(recipient.email, message);
            logger_->log("email",
                         recipient.email,
                         message,
                         result,
                         result ? "" : "Email service send failed");
            continue;
        }

        if (channel == "sms") {
            if (!validator_->is_valid_phone(recipient.phone)) {
                logger_->log("sms", recipient.phone, message, false, "Invalid phone format");
                continue;
            }

            const bool result = sms_service_->send(recipient.phone, message);
            logger_->log("sms",
                         recipient.phone,
                         message,
                         result,
                         result ? "" : "SMS service send failed");
            continue;
        }

        if (channel == "push") {
            if (!validator_->is_valid_push_token(recipient.push_token)) {
                logger_->log("push", recipient.push_token, message, false, "Invalid push token format");
                continue;
            }

            const bool result = push_service_->send(recipient.push_token, message);
            logger_->log("push",
                         recipient.push_token,
                         message,
                         result,
                         result ? "" : "Push service send failed");
            continue;
        }

        logger_->log(channel, "-", message, false, "Unknown notification channel");
    }
}
