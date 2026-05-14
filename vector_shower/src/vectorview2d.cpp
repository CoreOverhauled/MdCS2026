#include "vectorview2d.h"

#include <QKeyEvent>
#include <QPainter>

namespace {
double GridUnitFromAxeLength(const int32_t axe_length_px, double axe_len_world) {
  const double MAX_GRID_SPACING_PX = 200.0;
  std::array<double, 3> STEP_SEQUENCE{2.0, 2.5, 2.0};
  const double unit_exp = std::floor(std::log10(axe_len_world));
  double unit = std::pow(10.0, unit_exp), prev_unit;
  uint32_t i = 0;
  double ticks_distance;
  do {
    double num_ticks = axe_len_world / unit;
    ticks_distance = axe_length_px / num_ticks;
    prev_unit = unit;
    unit /= STEP_SEQUENCE[i % STEP_SEQUENCE.size()];
    ++i;
  } while (ticks_distance > MAX_GRID_SPACING_PX);
  return prev_unit;
}

std::vector<double> ComputeGridTicks(const double unit, const double v0, const double v1) {
  std::vector<double> ticks;
  for (double i = std::floor(v0 / unit) - 1.0; i * unit < v1; i += 1.0) {
    if (i * unit > v0) {
      ticks.push_back(i * unit);
    }
  }
  return ticks;
}

class CoordinateConverter {
 public:
  explicit CoordinateConverter(const QRectF& viewport_location, float screen_width,
                               float screen_height)
      : x0_(viewport_location.left()),
        y0_(viewport_location.top()),  // Qt's inverted coords affect top/bottom
        height_(screen_height),
        xScale_(screen_width / viewport_location.width()),
        yScale_(screen_height / viewport_location.height()) {}
  QPointF operator()(const QPointF& world) const {
    auto result = QPointF((world.x() - x0_) * xScale_, height_ - (world.y() - y0_) * yScale_);
    return result;
  }

 private:
  float x0_, y0_;
  float height_;
  float xScale_, yScale_;
};
}  // namespace

VectorView2D::VectorView2D(std::shared_ptr<ObjectsRepository2D> objects, QWidget* parent)
    : drawing_data_(std::move(objects)), QWidget(parent) {
  double cx = viewport_location_.x() + viewport_location_.width() / 2.0;
  double cy = viewport_location_.y() + viewport_location_.height() / 2.0;
  double pixel_scale = width() / viewport_location_.width();
  double top_y = cy + pixel_scale * height() / 2.0;
  double left_x = cx - pixel_scale * width() / 2.0;
  viewport_location_ = QRectF(left_x, top_y, width(), top_y);
  setFocusPolicy(Qt::StrongFocus);
  setFocus();
}

void VectorView2D::paintEvent(QPaintEvent* event) {
  update_pending_ = false;
  QPainter painter(this);
  const int32_t width = this->width();
  const int32_t height = this->height();
  painter.setPen(QPen(QColor("white"), 1));

  // Draw swarms
  float swarm_pixel_ratio = 2.5;
  int32_t swarm_width = width / swarm_pixel_ratio;
  int32_t swarm_height = height / swarm_pixel_ratio;
  QImage swarm_image(swarm_width, swarm_height, QImage::Format_RGB32);
  Array2D<QColor> swarmColoring =
      drawing_data_->computeSwarnColorGrid(viewport_location_, swarm_width, swarm_height);
  for (int32_t x = 0; x < swarm_width; x++) {
    for (int32_t y = 0; y < swarm_height; y++) {
      swarm_image.setPixel(x, y, swarmColoring(x, swarm_height - 1 - y).rgb());
    }
  }
  painter.drawImage(rect(), swarm_image);

  // Draw vectors
  CoordinateConverter worldToViewport(viewport_location_, width, height);
  painter.save();
  painter.setPen(QPen(painter.pen().color(), 1));
  for (const auto& [pos, color] : drawing_data_->getVectors()) {
    auto center = QPointF(pos.x, pos.y);
    if (viewport_location_.contains(center)) {
      painter.setBrush(QBrush(color));
      auto p = worldToViewport(center);
      painter.drawEllipse(worldToViewport(center), 5, 5);
    }
  }
  painter.restore();

  // Compute grid scale.
  const double unit = std::min(GridUnitFromAxeLength(width, viewport_location_.width()),
                               GridUnitFromAxeLength(height, viewport_location_.height()));
  const int32_t dec_places = std::max(-std::ceil(std::log10(unit)), 0.0);
  auto make_label = [dec_places](double val) {
    std::stringstream ss;
    ss << std::fixed << std::setprecision(dec_places) << val;
    return QString::fromStdString(ss.str());
  };

  // X: Draw vertical lines.
  const double x0 = viewport_location_.x();
  const double w = viewport_location_.width();
  const int32_t x_text_pos = height - 6;
  for (double tick : ComputeGridTicks(unit, x0, x0 + w)) {
    const int32_t screen_x = (tick - x0) / w * width;
    painter.drawLine(screen_x, 0, screen_x, height);
    painter.drawText(screen_x + 3, x_text_pos, make_label(tick));
  }

  // Draw horizontal lines.
  const double y0 = viewport_location_.y();
  const double h = viewport_location_.height();
  // TODO: measure height to adjust.
  const int32_t y_text_pos = 3;
  for (double tick : ComputeGridTicks(unit, y0, y0 + h)) {
    const double screen_y = (1.0 - (tick - y0) / h) * height;
    painter.drawLine(0, screen_y, width, screen_y);
    painter.drawText(y_text_pos, screen_y + -10, make_label(tick));
  }
}

void VectorView2D::resizeEvent(QResizeEvent* event) {
  // TODO: this resets scale and position, it shouldn't!
  viewport_location_ = QRectF(0, 0, 10, (10.0 * height()) / width());
}

void VectorView2D::keyPressEvent(QKeyEvent* event) {
  // qDebug() << "Keyboard event: " << event->text() << event->key();
  switch (event->key()) {
    case Qt::Key_Left:
      shiftViewport(10, LEFT);
      break;
    case Qt::Key_Right:
      shiftViewport(10, RIGHT);
      break;
    case Qt::Key_Up:
      shiftViewport(10, UP);
      break;
    case Qt::Key_Down:
      shiftViewport(10, DOWN);
      break;
    case Qt::Key_Plus:
      scaleViewport(1.0 / 1.1);
      break;
    case Qt::Key_Minus:
      scaleViewport(1.1);
      break;
    default:
      QWidget::keyPressEvent(event);
  }
}

void VectorView2D::scaleViewport(double scale) {
  const double w = viewport_location_.width() * scale;
  const double h = viewport_location_.height() * scale;
  viewport_location_ =
      QRectF(viewport_location_.x() + (viewport_location_.width() - w) / 2.0,
             viewport_location_.y() + (viewport_location_.height() - h) / 2.0, w, h);
  updateView();
}

void VectorView2D::shiftViewport(double shift, Direction direction) {
  const double pixel_scale = viewport_location_.width() / width();
  shift = shift * pixel_scale;
  ;
  if (direction == UP || direction == DOWN) {
    if (direction == DOWN) {
      shift = -shift;
    }
    viewport_location_.translate(0, shift);
  } else {
    if (direction == LEFT) {
      shift = -shift;
    }
    viewport_location_.translate(shift, 0);
  }
  updateView();
}

void VectorView2D::updateView() {
  if (!update_pending_) {
    update_pending_ = true;
    update();
  }
}
