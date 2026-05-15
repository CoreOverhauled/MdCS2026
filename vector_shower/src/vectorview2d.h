#ifndef VECTOR_SHOWER_VECTORVIEW2D_H
#define VECTOR_SHOWER_VECTORVIEW2D_H

#include <QWidget>

#include "ObjectsRepository2D.h"

class VectorView2D : public QWidget {
  Q_OBJECT

 public:
  enum Direction { UP, DOWN, LEFT, RIGHT };

  VectorView2D(std::shared_ptr<ObjectsRepository2D> objects, QWidget* parent = nullptr);

  ~VectorView2D() override = default;

 public slots:
  void scaleViewport(double scale);

  void shiftViewport(double pixels, Direction direction);

  void updateView();

 protected:
  void paintEvent(QPaintEvent* event) override;

  void resizeEvent(QResizeEvent* event) override;

  void keyPressEvent(QKeyEvent* event) override;

  QRectF viewport_location_;
  std::shared_ptr<ObjectsRepository2D> drawing_data_;
  bool update_pending_ = false;
};

#endif  // VECTOR_SHOWER_VECTORVIEW2D_H
