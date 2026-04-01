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

MainWindow::MainWindow(std::shared_ptr<NotificationFacade> facade,
                       std::shared_ptr<NotificationLogger> logger,
                       QWidget* parent)
    : QMainWindow(parent),
      facade_(std::move(facade)),
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

    auto* title = new QLabel("Notification Service (Facade Pattern)", central);
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
    setWindowTitle("Notification Facade GUI");

    connect(send_button, &QPushButton::clicked,
            this, &MainWindow::onSendClicked);
}

void MainWindow::onSendClicked() {
    NotificationFacade::Recipient recipient;
    recipient.email = email_input_->text().toStdString();
    recipient.phone = phone_input_->text().toStdString();
    recipient.push_token = push_token_input_->text().toStdString();

    const std::string message = message_input_->text().toStdString();
    std::vector<std::string> channels;

    if (email_checkbox_->isChecked()) {
        channels.push_back("email");
    }
    if (sms_checkbox_->isChecked()) {
        channels.push_back("sms");
    }
    if (push_checkbox_->isChecked()) {
        channels.push_back("push");
    }

    if (channels.empty()) {
        appendLog("[UI] Select at least one delivery channel.");
        return;
    }

    facade_->send_notification(recipient, message, channels);
}

void MainWindow::appendLog(const QString& message) {
    log_output_->append(message);
}
