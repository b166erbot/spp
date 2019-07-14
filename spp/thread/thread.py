from threading import Thread


class MultiThread:
    """ Classe gerenciadora de Threads. """

    def __init__(self, funcoes: list, queues: list, main):
        self.queues = queues
        zipped = zip(funcoes, queues)
        self.threads = [Thread(target=main, daemon=True)]
        self.threads += [Thread(target=rodar, args=(funcao, queue), daemon=True)
                         for funcao, queue in zipped]

    def rodar(self):
        for thread in self.threads:
            thread.start()
        self.threads[0].join()


def rodar(tarefa, queue):
    while True:
        # é obrigatório armazenar em uma variável ou condicionar com if a queue
        temp = queue.get()
        tarefa(*temp) if temp else tarefa()
        queue.task_done()
