# Лабораторная работа: Система уведомлений и паттерн Фасад

## 1. Проблема

В системе есть несколько подсистем: EmailService, SmsService, PushService, Validator и NotificationLogger.
Если GUI-клиент напрямую управляет ими всеми, в клиентском коде накапливаются:

1. Дублирование валидации и отправки по каналам.
2. Повторяющееся логирование для каждого сценария.
3. Высокая связанность MainWindow с деталями доменной логики.

Это видно в версии без фасада: логика отправки, валидации и логирования размещена прямо в MainWindow.

## 2. Решение

Использован структурный паттерн Facade: добавлен класс NotificationFacade с единым методом:

send_notification(recipient, message, channels)

Клиент передает входные данные один раз, а фасад внутри:

1. Валидирует данные.
2. Вызывает нужные сервисы по каналам.
3. Логгирует результат по каждому каналу.

## 3. Что представляет собой Facade

Facade предоставляет упрощенный интерфейс к группе связанных классов и скрывает внутреннюю координацию вызовов.

В этом проекте:

1. Client: MainWindow.
2. Facade: NotificationFacade.
3. Подсистема: Validator, EmailService, SmsService, PushService, NotificationLogger.

## 4. UML-диаграммы

Диаграммы находятся в файле [Facade.xml](Facade.xml):

1. Структурная UML-диаграмма фасада.
2. Sequence для подхода без фасада.
3. Sequence для подхода с фасадом.

## 5. Сравнение на конкретных примерах кода

### Пример 1. Клиентский код отправки

Без фасада клиент содержит всю оркестрацию.
Файл: [notification_no_facade/mainwindow.cpp](notification_no_facade/mainwindow.cpp)

```cpp
void MainWindow::onSendClicked() {
  const std::string email = email_input_->text().toStdString();
  const std::string phone = phone_input_->text().toStdString();
  const std::string push_token = push_token_input_->text().toStdString();
  const std::string message = message_input_->text().toStdString();

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

  // Аналогичные блоки для sms и push
}
```

С фасадом клиент только собирает данные и делает один вызов.
Файл: [notification_facade_gui/mainwindow.cpp](notification_facade_gui/mainwindow.cpp)

```cpp
void MainWindow::onSendClicked() {
  NotificationFacade::Recipient recipient;
  recipient.email = email_input_->text().toStdString();
  recipient.phone = phone_input_->text().toStdString();
  recipient.push_token = push_token_input_->text().toStdString();

  const std::string message = message_input_->text().toStdString();
  std::vector<std::string> channels;

  if (email_checkbox_->isChecked()) channels.push_back("email");
  if (sms_checkbox_->isChecked()) channels.push_back("sms");
  if (push_checkbox_->isChecked()) channels.push_back("push");

  facade_->send_notification(recipient, message, channels);
}
```

Вывод: в версии с фасадом MainWindow не знает деталей валидации и отправки.

### Пример 2. Где находится бизнес-логика

В версии с фасадом доменная логика централизована.
Файл: [notification_facade_gui/src/notification_facade.cpp](notification_facade_gui/src/notification_facade.cpp)

```cpp
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
      logger_->log("email", recipient.email, message, result,
             result ? "" : "Email service send failed");
    }
    // sms/push обрабатываются аналогично здесь же
  }
}
```

Вывод: изменения в правилах отправки и обработки ошибок делаются в одном месте, а не в UI.

### Пример 3. Добавление нового канала (например, Telegram)

Без фасада:

1. Добавлять новый checkbox в MainWindow.
2. Добавлять новую ветку в onSendClicked с валидацией, вызовом сервиса и logger->log.
3. Повторять шаблон уже существующих веток.

С фасадом:

1. UI добавляет только выбор канала.
2. Основные изменения в NotificationFacade и новом сервисе TelegramService.
3. Главный обработчик в MainWindow остается компактным.

## 6. Сравнение подходов

### Без фасада

1. MainWindow перегружен доменной логикой.
2. Повышается риск регрессий при изменениях.
3. Сложнее тестировать, потому что UI и бизнес-правила тесно связаны.

### С фасадом

1. MainWindow выполняет роль клиента и не оркестрирует подсистему.
2. Логика централизована в NotificationFacade.
3. Снижается связанность, упрощается расширение и сопровождение.

## 7. Заключение

На практике в этой лабораторной работе паттерн Facade устраняет архитектурную проблему перегруженного клиентского кода.

Итог сравнения:

1. Версия без фасада демонстрирует дублирование и высокую связанность.
2. Версия с фасадом показывает более чистую архитектуру: UI вызывает один метод, а доменная логика сосредоточена в одном компоненте.
3. При эволюции системы (новые каналы, fallback, единые политики ошибок) подход с фасадом масштабируется заметно лучше.
