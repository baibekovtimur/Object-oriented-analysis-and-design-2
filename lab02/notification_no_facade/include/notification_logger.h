#pragma once

#include <QObject>
#include <QString>

#include <string>

class NotificationLogger : public QObject {
    Q_OBJECT

public:
    explicit NotificationLogger(QObject* parent = nullptr);

    void log(const std::string& channel,
             const std::string& recipient,
             const std::string& message,
             bool status,
             const std::string& error_msg = "");

signals:
    void newLogMessage(const QString& message);
};
