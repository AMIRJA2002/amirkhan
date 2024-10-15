from .balebot import main
from threading import Thread


def pool_bale():
    Thread(target=main).start()


Thread(target=pool_bale).start()
