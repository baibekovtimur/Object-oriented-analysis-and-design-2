# Additional clean files
cmake_minimum_required(VERSION 3.16)

if("${CONFIG}" STREQUAL "" OR "${CONFIG}" STREQUAL "")
  file(REMOVE_RECURSE
  "CMakeFiles\\notification_no_facade_autogen.dir\\AutogenUsed.txt"
  "CMakeFiles\\notification_no_facade_autogen.dir\\ParseCache.txt"
  "notification_no_facade_autogen"
  )
endif()
