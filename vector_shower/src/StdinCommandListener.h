//
// Created by quazyrog on 10/05/26.
//

#ifndef COMMANDLISTENER_H
#define COMMANDLISTENER_H
#include <QJsonDocument>
#include <condition_variable>
#include <deque>
#include <iostream>

#include "ObjectsRepository2D.h"

class StdinCommandListener : public QObject {
  Q_OBJECT
 public:
  explicit StdinCommandListener(std::shared_ptr<ObjectsRepository2D> objects_repository);
  StdinCommandListener(const StdinCommandListener&) = delete;
  StdinCommandListener& operator=(const StdinCommandListener&) = delete;
  ~StdinCommandListener() override;

 signals:
  void onNewCommand();
 private slots:
  void handleNewCommand();

 private:
  struct CommandQueue {
    std::mutex mutex;
    bool stopped = false;
    std::deque<std::string> commands;
  };

  std::optional<QJsonDocument> getCommand();

  const std::shared_ptr<ObjectsRepository2D> objects_repository_;
  std::shared_ptr<CommandQueue> command_queue_;
};

#endif  // COMMANDLISTENER_H
