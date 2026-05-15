//
// Created by quazyrog on 08/04/2026.
//

#ifndef VECTOR_SHOWER_OBJECTSREPOSITORY2D_H
#define VECTOR_SHOWER_OBJECTSREPOSITORY2D_H
#include <qcolor.h>

#include <QObject>

template <class T>
class Array2D {
 public:
  Array2D(uint32_t width, uint32_t height, const T& init = T())
      : width_(width), height_(height), data_(width * height, init) {}
  uint32_t width() const { return width_; }
  uint32_t height() const { return height_; }
  T& operator()(uint32_t x, uint32_t y) {
    if (x >= width_ || y >= height_) {
      throw std::out_of_range(
          std::format("Array2D: ({}, {}) - out of range {}x{}", x, y, width_, height_));
    }
    return data_[x + y * width_];
  }

 private:
  size_t width_, height_;
  std::vector<T> data_;
};

class ObjectsRepository2D : public QObject {
  Q_OBJECT
 public:
  struct Coords {
    float x, y;
  };
  struct VectorData {
    Coords xy;
    QColor color;
  };
  void addVector(Coords xy, QColor color);
  void addVectorSwarm(QColor color, std::vector<Coords> xy);
  // Computes color map from swarms: for every cell (pixel) in the resulting
  // grid of given size we count how many vectors of every swarm lay in it (if a
  // vector lies between grid centers, it contributes linerrly to all
  // surrounding cells). Then the resulting color is computed as weighted
  // combination of all swarms in the cell, normalized by largest sum over
  // entire grid. Y axe goes bottom to top (carthesian, not screen).
  Array2D<QColor> computeSwarnColorGrid(QRectF clip, uint32_t width, uint32_t height);
  const std::vector<VectorData>& getVectors() const { return vectors_; }
 signals:
  void updated();

 private:
  struct SwarmData {
    QColor color;
    std::vector<Coords> xy;
  };
  std::vector<SwarmData> swarms_;
  std::vector<VectorData> vectors_;
};

#endif  // VECTOR_SHOWER_OBJECTSREPOSITORY2D_H