"""Persistência em arquivos JSON."""
import json
import os


class RepositorioJSON:
    def __init__(self, caminho: str):
        self.caminho = caminho
        pasta = os.path.dirname(caminho)
        if pasta:
            os.makedirs(pasta, exist_ok=True)

    def carregar(self) -> list:
        if not os.path.exists(self.caminho):
            return []
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except (json.JSONDecodeError, OSError):
            # Arquivo corrompido ou ilegível: começa vazio em vez de quebrar.
            return []

    def salvar(self, registros: list) -> None:
        with open(self.caminho, "w", encoding="utf-8") as arquivo:
            json.dump(registros, arquivo, ensure_ascii=False, indent=2)
