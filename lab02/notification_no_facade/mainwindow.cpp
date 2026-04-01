#include "mainwindow.h"

#include <QCheckBox>
#include <QFormLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QTextEdit>
#include <QVBoxLayout>
#include <QWidget>

MainWindow::MainWindow(std::shared_ptr<EmailService> email_service,
                       std::shared_ptr<SmsService> sms_service,
                       std::shared_ptr<PushService> push_service,
                       std::shared_ptr<Validator> validator,
                       std::shared_ptr<NotificationLogger> logger,
                       QWidget* parent)
    : QMainWindow(parent),
      email_service_(std::move(email_service)),
      sms_service_(std::move(sms_service)),
      push_service_(std::move(push_service)),
      validator_(std::move(validator)),
      logger_(std::move(logger)),
      email_input_(nullptr),
      phone_input_(nullptr),
      push_token_input_(nullptr),
      message_input_(nullptr),
      email_checkbox_(nullptr),
      sms_checkbox_(nullptr),
      push_checkbox_(nullptr),
      log_output_(nullptr) {
    buildUi();

    connect(logger_.get(), &NotificationLogger::newLogMessage,
            this, &MainWindow::appendLog);
}

void MainWindow::buildUi() {
    auto* central = new QWidget(this);
    auto* root_layout = new QVBoxLayout(central);

    auto* title = new QLabel("Notification Service (No Facade)", central);
    QFont title_font = title->font();
    title_font.setPointSize(13);
    title_font.setBold(true);
    title->setFont(title_font);

    auto* form_layout = new QFormLayout();

    email_input_ = new QLineEdit(central);
    email_input_->setPlaceholderText("user@example.com");

    phone_input_ = new QLineEdit(central);
    phone_input_->setPlaceholderText("+12345678901");

    push_token_input_ = new QLineEdit(central);
    push_token_input_->setPlaceholderText("fcm_token_123456");

    message_input_ = new QLineEdit(central);
    message_input_->setPlaceholderText("Message text");

    form_layout->addRow("Email:", email_input_);
    form_layout->addRow("Phone:", phone_input_);
    form_layout->addRow("Push token:", push_token_input_);
    form_layout->addRow("Message:", message_input_);

    auto* channel_layout = new QHBoxLayout();
    email_checkbox_ = new QCheckBox("Email", central);
    sms_checkbox_ = new QCheckBox("SMS", central);
    push_checkbox_ = new QCheckBox("Push", central);

    email_checkbox_->setChecked(true);

    channel_layout->addWidget(email_checkbox_);
    channel_layout->addWidget(sms_checkbox_);
    channel_layout->addWidget(push_checkbox_);
    channel_layout->addStretch(1);

    auto* send_button = new QPushButton("Send notification", central);

    log_output_ = new QTextEdit(central);
    log_output_->setReadOnly(true);
    log_output_->setPlaceholderText("Notification logs will appear here...");

    root_layout->addWidget(title);
    root_layout->addLayout(form_layout);
    root_layout->addLayout(channel_layout);
    root_layout->addWidget(send_button);
    root_layout->addWidget(log_output_, 1);

    setCentralWidget(central);
    setWindowTitle("Notification Service Without Facade");

    connect(send_button, &QPushButton::clicked,
            this, &MainWindow::onSendClicked);
}

void MainWindow::onSendClicked() {
    const std::string email = email_input_->text().toStdString();
    const std::string phone = phone_input_->text().toStdString();
    const std::string push_token = push_token_input_->text().toStdString();
    const std::string message = message_input_->text().toStdString();

    const bool email_selected = email_checkbox_->isChecked();
    const bool sms_selected = sms_checkbox_->isChecked();
    const bool push_selected = push_checkbox_->isChecked();

    if (!email_selected && !sms_selected && !push_selected) {
        appendLog("[UI] Select at least one delivery channel.");
        return;
    }

    if (email_selected) {
        if (email.empty()) {
            logger_->log("email", email, message, false, "Email is empty");
        } else if (!validator_->is_valid_email(email)) {
            logger_->log("email", email, message, false, "Invalid email format");
        } else if (message.empty()) {
            logger_->log("email", email, message, false, "Message is empty");
        } else {
            const bool sent = email_service_->send(email, message);
            logger_->log("email", email, message, sent, sent ? "" : "Email service failed");
        }
    }

    if (sms_selected) {
        if (phone.empty()) {
            logger_->log("sms", phone, message, false, "Phone is empty");
        } else if (!validator_->is_valid_phone(phone)) {
            logger_->log("sms", phone, message, false, "Invalid phone format");
        } else if (message.empty()) {
            logger_->log("sms", phone, message, false, "Message is empty");
        } else {
            const bool sent = sms_service_->send(phone, message);
            logger_->log("sms", phone, message, sent, sent ? "" : "SMS service failed");
        }
    }

    if (push_selected) {
        if (push_token.empty()) {
            logger_->log("push", push_token, message, false, "Push token is empty");
        } else if (!validator_->is_valid_push_token(push_token)) {
            logger_->log("push", push_token, message, false, "Invalid push token format");
        } else if (message.empty()) {
            logger_->log("push", push_token, message, false, "Message is empty");
        } else {
            const bool sent = push_service_->send(push_token, message);
            logger_->log("push", push_token, message, sent, sent ? "" : "Push service failed");
        }
    }
}

void MainWindow::appendLog(const QString& message) {
    log_output_->append(message);
}
