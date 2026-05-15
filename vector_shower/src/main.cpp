#include <QApplication>
#include <QObject>
#include <QPushButton>

#include "StdinCommandListener.h"
#include "vectorview2d.h"

int main(int argc, char* argv[]) {
  QApplication a(argc, argv);
  auto objects = std::make_shared<ObjectsRepository2D>();
  VectorView2D widget(objects);
  QObject::connect(objects.get(), &ObjectsRepository2D::updated, &widget,
                   &VectorView2D::updateView);
  widget.show();
  StdinCommandListener stdin_listener(objects);
  int exitcode = QApplication::exec();
std:
  _exit(exitcode);  // Terminate the stdin-blocked thread
}
