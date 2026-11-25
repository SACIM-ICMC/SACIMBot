from dataclasses import dataclass, field

from bot.entidades.callback import CallbackData as CD


@dataclass
class Menu:
    tipo_menu: CD.TipoMenu
    lista_menus: tuple[CD.ItemMenu]  # Lista de botões do menu
    menu_atual: CD.ItemMenu = field(init=False)

    def __post_init__(self) -> None:
        # Garante as condições
        if not self.lista_menus:
            raise ValueError("A lista não pode ser vazia!")
        self.menu_atual = self.lista_menus[0]

    # Mudar de menu
    def mudar_menu(self, menu: CD.ItemMenu) -> bool:
        # Verifica a viabilidade de mudar
        if self.menu_atual == menu or menu not in self.lista_menus:
            return False
        self.menu_atual = menu
        return True
