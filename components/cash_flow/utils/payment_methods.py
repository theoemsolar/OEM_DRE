from enum import Enum


class PaymentMethods(Enum):
    BUSINESS_DAY = 1
    FIX_DATE = 2
    AFTER_NF = 3
    CONTRACT = 4


PAYMENT_METHODS = {
    "data da Roçagem e Limpeza Mensal": PaymentMethods.CONTRACT,
    "data da Custo OP": PaymentMethods.BUSINESS_DAY,
    "data da Comissão": PaymentMethods.BUSINESS_DAY,
    "data da Folha ADM": PaymentMethods.BUSINESS_DAY,
    "data da Imposto": PaymentMethods.AFTER_NF,
    "data da Bancagem": PaymentMethods.FIX_DATE,
    "data da Custo Fixo": PaymentMethods.FIX_DATE,
}
