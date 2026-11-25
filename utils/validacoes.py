"""Funções de validação e utilidades gerais."""
import calendar
import re
from datetime import date


class ErroNegocio(Exception):
    """Erro de regra de negócio ou de validação de dados."""


def somente_digitos(texto: str) -> str:
    return re.sub(r"\D", "", texto or "")


def validar_nome(nome: str) -> str:
    nome = (nome or "").strip()
    if len(nome) < 3:
        raise ErroNegocio("O nome deve ter pelo menos 3 caracteres.")
    return nome


def validar_cpf(cpf: str) -> str:
    """Valida CPF (com dígitos verificadores) e devolve só os números."""
    cpf = somente_digitos(cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        raise ErroNegocio("CPF inválido.")
    for tamanho in (9, 10):
        soma = sum(int(cpf[i]) * (tamanho + 1 - i) for i in range(tamanho))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[tamanho]):
            raise ErroNegocio("CPF inválido.")
    return cpf


def validar_telefone(telefone: str) -> str:
    telefone = somente_digitos(telefone)
    if len(telefone) not in (10, 11):
        raise ErroNegocio("Telefone deve ter 10 ou 11 dígitos (com DDD).")
    return telefone


def validar_valor(valor) -> float:
    try:
        valor = float(str(valor).replace(",", "."))
    except ValueError:
        raise ErroNegocio("Valor inválido.")
    if valor <= 0:
        raise ErroNegocio("O valor deve ser maior que zero.")
    return round(valor, 2)


def validar_inteiro_positivo(valor, campo: str = "Valor") -> int:
    try:
        numero = int(valor)
    except (ValueError, TypeError):
        raise ErroNegocio(f"{campo} deve ser um número inteiro.")
    if numero <= 0:
        raise ErroNegocio(f"{campo} deve ser maior que zero.")
    return numero


def somar_meses(data: date, meses: int) -> date:
    """Soma meses a uma data, ajustando o dia quando necessário."""
    indice = data.month - 1 + meses
    ano = data.year + indice // 12
    mes = indice % 12 + 1
    dia = min(data.day, calendar.monthrange(ano, mes)[1])
    return date(ano, mes, dia)


def formatar_cpf(cpf: str) -> str:
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
