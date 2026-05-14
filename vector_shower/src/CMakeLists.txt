cmake_minimum_required(VERSION 3.28)
project(vector_shower)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)


find_package(Qt6 COMPONENTS
        Core
        Gui
        Widgets
        REQUIRED)

add_executable(vector_shower main.cpp
        vectorview2d.cpp
        vectorview2d.h
        ObjectsRepository2D.cpp
        ObjectsRepository2D.h
        StdinCommandListener.cpp
        StdinCommandListener.h
)
target_link_libraries(vector_shower
        Qt::Core
        Qt::Gui
        Qt::Widgets
)

