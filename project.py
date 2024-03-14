import sys

sys.path.append("MVP")

from MVP.model import Model
from MVP.view import Cripto50
from MVP.presenter import Presenter


def main():
    model = Model()
    view = Cripto50()
    presenter = Presenter(model, view)
    presenter.loadGUI()


if __name__ == "__main__":
    main()
