#include <QApplication>

#include <memory>

#include "email_service.h"
#include "mainwindow.h"
#include "notification_logger.h"
#include "push_service.h"
#include "sms_service.h"
#include "validator.h"

int main(int argc, char* argv[]) {
    QApplication app(argc, argv);

    auto email_service = std::make_shared<EmailService>("smtp.example.com", 587, "user", "password");
    auto sms_service = std::make_shared<SmsService>("sms-api-key", "+10000000000");
    auto push_service = std::make_shared<PushService>("fcm-key");
    auto validator = std::make_shared<Validator>();
    auto logger = std::make_shared<NotificationLogger>();

    MainWindow window(email_service, sms_service, push_service, validator, logger);
    window.resize(720, 540);
    window.show();

    return app.exec();
}
