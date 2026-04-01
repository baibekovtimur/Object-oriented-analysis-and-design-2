#pragma once

#include <QMainWindow>

#include <memory>

#include "notification_facade.h"
#include "notification_logger.h"

class QCheckBox;
class QLineEdit;
class QTextEdit;

class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    explicit MainWindow(std::shared_ptr<NotificationFacade> facade,
                        std::shared_ptr<NotificationLogger> logger,
                        QWidget* parent = nullptr);

private slots:
    void onSendClicked();
    void appendLog(const QString& message);

private:
    void buildUi();

    std::shared_ptr<NotificationFacade> facade_;
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
