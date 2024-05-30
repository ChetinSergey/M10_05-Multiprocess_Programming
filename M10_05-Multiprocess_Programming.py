import multiprocessing


class WarehouseManager:
    def __init__(self):
        self.data = multiprocessing.Manager().dict()

    def process_request(self, request):
        product, action, total = request
        if product in self.data:
            if action == "receipt":
                self.data[product] += total
            elif action == "shipment":
                if total < self.data[product]:
                    self.data[product] -= total
        else:
            self.data[product] = total

    def run(self, requests):
        parallel_process = []
        for request in requests:
            parallel_process.append(multiprocessing.Process(target=self.process_request, args=(request,)))
        for i in parallel_process:
            i.start()
        for i in parallel_process:
            i.join()


if __name__ == '__main__':
    # Создаем менеджера склада
    manager = WarehouseManager()

    # Множество запросов на изменение данных о складских запасах
    requests = [
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50)
    ]

    # Запускаем обработку запросов
    manager.run(requests)

    # Выводим обновленные данные о складских запасах
    print(manager.data)
