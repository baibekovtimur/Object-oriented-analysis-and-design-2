cmake_minimum_required(VERSION 3.16)

project(notification_facade_gui VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets)

add_executable(notification_facade_gui WIN32
    main.cpp
    mainwindow.h
    mainwindow.cpp
    include/email_service.h
    include/sms_service.h
    include/push_service.h
    include/validator.h
    include/notification_logger.h
    include/notification_facade.h
    src/email_service.cpp
    src/sms_service.cpp
    src/push_service.cpp
    src/validator.cpp
    src/notification_logger.cpp
    src/notification_facade.cpp
)

target_include_directories(notification_facade_gui PRIVATE include)

target_link_libraries(notification_facade_gui PRIVATE Qt6::Widgets)
