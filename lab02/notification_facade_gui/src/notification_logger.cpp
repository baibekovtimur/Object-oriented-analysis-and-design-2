#include "notification_logger.h"

#include <QDateTime>

NotificationLogger::NotificationLogger(QObject* parent)
    : QObject(parent) {
}

void NotificationLogger::log(const std::string& channel,
                             const std::string& recipient,
                             const std::string& message,
                             bool status,
                             const std::string& error_msg) {
    const QString timestamp = QDateTime::currentDateTime().toString("yyyy-MM-dd HH:mm:ss");
    const QString status_text = status ? "SUCCESS" : "FAIL";

    QString line = QString("[%1] [%2] channel=%3 recipient=%4 message=\"%5\"")
                       .arg(timestamp)
                       .arg(status_text)
                       .arg(QString::fromStdString(channel))
                       .arg(QString::fromStdString(recipient))
                       .arg(QString::fromStdString(message));

    if (!status && !error_msg.empty()) {
        line += QString(" error=\"%1\"").arg(QString::fromStdString(error_msg));
    }

    emit newLogMessage(line);
}
