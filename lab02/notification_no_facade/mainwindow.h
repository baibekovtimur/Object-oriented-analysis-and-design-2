#pragma once

#include <QMainWindow>

#include <memory>

#include "email_service.h"
#include "notification_logger.h"
#include "push_service.h"
#include "sms_service.h"
#include "validator.h"

class QCheckBox;
class QLineEdit;
class QTextEdit;

class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    explicit MainWindow(std::shared_ptr<EmailService> email_service,
                        std::shared_ptr<SmsService> sms_service,
                        std::shared_ptr<PushService> push_service,
                        std::shared_ptr<Validator> validator,
                        std::shared_ptr<NotificationLogger> logger,
                        QWidget* parent = nullptr);

private slots:
    void onSendClicked();
    void appendLog(const QString& message);

private:
    void buildUi();

    std::shared_ptr<EmailService> email_service_;
    std::shared_ptr<SmsService> sms_service_;
    std::shared_ptr<PushService> push_service_;
    std::shared_ptr<Validator> validator_;
    std::shared_ptr<NotificationLogger> logger_;

    QLineEdit* email_input_;
    QLineEdit* phone_input_;
    QLineEdit* push_token_input_;
    QLineEdit* message_input_;

    QCheckBox* email_checkbox_;
    QCheckBox* sms_checkbox_;
    QCheckBox* push_checkbox_;

    QTextEdit* log_output_;
};
