# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_j8_model_xacro_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED j8_model_xacro_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(j8_model_xacro_FOUND FALSE)
  elseif(NOT j8_model_xacro_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(j8_model_xacro_FOUND FALSE)
  endif()
  return()
endif()
set(_j8_model_xacro_CONFIG_INCLUDED TRUE)

# output package information
if(NOT j8_model_xacro_FIND_QUIETLY)
  message(STATUS "Found j8_model_xacro: 0.0.0 (${j8_model_xacro_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'j8_model_xacro' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${j8_model_xacro_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(j8_model_xacro_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${j8_model_xacro_DIR}/${_extra}")
endforeach()
