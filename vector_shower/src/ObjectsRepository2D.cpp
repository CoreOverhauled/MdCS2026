#include "ObjectsRepository2D.h"

#include <QRect>
#include <iostream>

void ObjectsRepository2D::addVectorSwarm(QColor color, std::vector<Coords> xy) {
  swarms_.push_back({.color = color, .xy = std::move(xy)});
  emit updated();
}

Array2D<QColor> ObjectsRepository2D::computeSwarnColorGrid(const QRectF clip, const uint32_t width,
                                                           const uint32_t height) {
  // Compute densities of swarms: each vector contributes to 4 surrounding cells
  // (like in linear texture interpolation), total of contributed values is one
  // per vector. The cell array has margin of two: +1 because to handle points
  // that are outside clip but still contribute, and another +1 for rounding
  // errors in points close to this "extended clip".
  Array2D<std::vector<float>> densities(width + 4, height + 4,
                                        std::vector<float>(swarms_.size(), 0.0f));
  const float x_cell_size = clip.width() / width;
  const float y_cell_size = clip.height() / height;
  // Extended clip, since points outside clip contribute to border points.
  const float left = clip.left() - x_cell_size;
  const float right = clip.right() + x_cell_size;
  const float bottom = clip.top() - y_cell_size;
  const float top = clip.bottom() + y_cell_size;
  // Actually compute densities
  for (uint32_t swarm_idx = 0; swarm_idx < swarms_.size(); swarm_idx++) {
    for (const Coords& xy : swarms_[swarm_idx].xy) {
      if (xy.x < left || right < xy.x || xy.y < bottom || top < xy.y) {
        continue;
      }
      // X axe offset in units, left cell index and left contribution.
      const float unit_x = (xy.x - left) / x_cell_size;
      const int32_t cell_x = std::floor(unit_x);
      const float weight_x = unit_x - cell_x;
      // Same for Y axe.
      const float unit_y = (xy.y - bottom) / y_cell_size;
      const int32_t cell_y = std::floor(unit_y);
      const float weight_y = unit_y - cell_y;
      // Add to densities.
      // std:: cerr << std::format("XY({}, {}) -> cell({}, {}) {} {}", xy.x,
      // xy.y, cell_x, cell_y, weight_x, weight_y) << std::endl;
      densities(cell_x, cell_y)[swarm_idx] += (1.0f - weight_x) * (1.0f - weight_y);
      densities(cell_x + 1, cell_y)[swarm_idx] += weight_x * (1.0f - weight_y);
      densities(cell_x, cell_y + 1)[swarm_idx] += (1.0f - weight_x) * weight_y;
      densities(cell_x + 1, cell_y + 1)[swarm_idx] += weight_x * weight_y;
    }
  }
  // Compute colors from densities
  float largest_total_weights = 0.0f;
  for (uint32_t cell_x = 0; cell_x < width; cell_x++) {
    for (uint32_t cell_y = 0; cell_y < height; cell_y++) {
      float total_weights = 0.0;
      for (const float d : densities(2 + cell_x, 2 + cell_y)) {
        total_weights += d;
      }
      largest_total_weights = std::max(largest_total_weights, total_weights);
    }
  }
  Array2D<QColor> output(width, height);
  for (uint32_t cell_x = 0; cell_x < width; cell_x++) {
    for (uint32_t cell_y = 0; cell_y < height; cell_y++) {
      float total_weights = 0.0;
      for (const float d : densities(2 + cell_x, 2 + cell_y)) {
        total_weights += d;
      }
      float r = 0.0, g = 0.0, b = 0.0;
      for (uint32_t swarm_idx = 0; swarm_idx < swarms_.size(); swarm_idx++) {
        const float d = densities(2 + cell_x, 2 + cell_y)[swarm_idx] / total_weights;
        r += d * swarms_[swarm_idx].color.red();
        g += d * swarms_[swarm_idx].color.green();
        b += d * swarms_[swarm_idx].color.blue();
      }
      output(cell_x, cell_y) = QColor(r, g, b);
    }
  }
  return output;
}

void ObjectsRepository2D::addVector(Coords xy, QColor color) {
  vectors_.push_back({xy, color});
  emit updated();
}
