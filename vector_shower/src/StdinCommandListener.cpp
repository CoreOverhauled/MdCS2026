//
// Created by quazyrog on 10/05/26.
//
#include "StdinCommandListener.h"

#include <QJsonArray>
#include <QJsonObject>
#include <QJsonParseError>

#include "ObjectsRepository2D.h"

StdinCommandListener::StdinCommandListener(std::shared_ptr<ObjectsRepository2D> objects_repository)
    : QObject(nullptr),
      objects_repository_(std::move(objects_repository)),
      command_queue_(std::make_shared<CommandQueue>()) {
  auto reading_loop = [queue = command_queue_, this]() {
    std::string line;
    while (std::getline(std::cin, line)) {
      std::lock_guard lock(queue->mutex);
      if (!queue->stopped) {
        queue->commands.push_back(std::move(line));
        emit onNewCommand();
      } else {
        qDebug() << "StdinCommandListener: thread stopped, not emitting new command";
        return;
      }
    }
  };
  QObject::connect(this, &StdinCommandListener::onNewCommand, this,
                   &StdinCommandListener::handleNewCommand, Qt::QueuedConnection);
  std::thread t(reading_loop);
  t.detach();
}

StdinCommandListener::~StdinCommandListener() {
  std::lock_guard<std::mutex> lock(command_queue_->mutex);
  // Make sure the stray thread does not emit signals anymore
  command_queue_->stopped = true;
}

std::optional<QJsonDocument> StdinCommandListener::getCommand() {
  std::string line;
  {
    std::lock_guard lock(command_queue_->mutex);
    if (command_queue_->commands.empty()) {
      return std::nullopt;
    }
    line = std::move(command_queue_->commands.front());
    command_queue_->commands.pop_front();
  }
  QJsonParseError err;
  auto doc = QJsonDocument::fromJson(line.c_str(), &err);
  qDebug() << "StdinCommandListener: got command: " << doc.toJson();
  if (err.error != QJsonParseError::NoError || !doc.isObject() ||
      !doc.object().contains("__cmd__")) {
    return std::nullopt;
  }
  return doc;
}

void StdinCommandListener::handleNewCommand() {
  while (auto doc = getCommand()) {
    if (!doc) {
      return;
    }
    const auto& cmd = doc->object();
    if (cmd["__cmd__"].toString() == "add_vector") {
      const float x = cmd["x"].toDouble();
      const float y = cmd["y"].toDouble();
      const auto color = QColor(cmd["color"].toVariant().toString());
      objects_repository_->addVector({x, y}, color);
    } else if (cmd["__cmd__"].toString() == "add_vector_swarm") {
      const auto raw_xs = cmd["xs"].toArray();
      const auto raw_ys = cmd["ys"].toArray();
      const size_t size = std::min(raw_xs.size(), raw_ys.size());
      std::vector<ObjectsRepository2D::Coords> vs;
      vs.reserve(size);
      for (int i = 0; i < size; i++) {
        vs.emplace_back(raw_xs[i].toDouble(), raw_ys[i].toDouble());
      }
      const auto color = QColor(cmd["color"].toVariant().toString());
      objects_repository_->addVectorSwarm(color, std::move(vs));
    }
  }
}
