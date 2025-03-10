import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from dataclasses import dataclass


def convert_currency(value):
    if isinstance(value, str):
        value = value.replace("R$", "").replace(".", "").replace(",", ".").strip()
        return float(value) if value else 0.0
    return value


@dataclass
class SankeyDiagram:
    om_data: pd.DataFrame

    def show(self):
        df = self.prepare_df()

        (
            gasto_bancagem,
            gasto_comissao,
            gasto_custo_fixo,
            gasto_custo_op,
            gasto_folha_adm,
            gasto_imposto,
            gasto_rocam,
            total_gastos,
            total_receitas,
        ) = self.calc_totals(df)

        labels = self.define_nodes(
            gasto_bancagem,
            gasto_comissao,
            gasto_custo_fixo,
            gasto_custo_op,
            gasto_folha_adm,
            gasto_imposto,
            gasto_rocam,
            total_receitas,
        )

        source, target, values = self.define_links(
            gasto_bancagem,
            gasto_comissao,
            gasto_custo_fixo,
            gasto_custo_op,
            gasto_folha_adm,
            gasto_imposto,
            gasto_rocam,
            total_gastos,
            total_receitas,
        )

        fig = self.create_diagram(labels, source, target, values)

        st.plotly_chart(fig, use_container_width=True)

    def create_diagram(self, labels, source, target, values):
        fig = go.Figure(
            data=[
                go.Sankey(
                    node=dict(
                        pad=15,
                        thickness=20,
                        line=dict(color="black", width=0.5),
                        label=labels,
                        color="lightblue",
                    ),
                    link=dict(
                        source=source,
                        target=target,
                        value=values,
                        color="rgba(100,100,100,0.5)",
                    ),
                )
            ]
        )

        return fig

    def define_links(
        self,
        gasto_bancagem,
        gasto_comissao,
        gasto_custo_fixo,
        gasto_custo_op,
        gasto_folha_adm,
        gasto_imposto,
        gasto_rocam,
        total_gastos,
        total_receitas,
    ):
        expense_values = [
            gasto_rocam,
            gasto_custo_op,
            gasto_comissao,
            gasto_folha_adm,
            gasto_imposto,
            gasto_bancagem,
            gasto_custo_fixo,
        ]
        proportions = [val / total_gastos for val in expense_values]
        source = []
        target = []
        values = []
        for j, prop in enumerate(proportions):
            source.append(0)  # Apenas um nó de entrada: Receitas (índice 0)
            target.append(j + 1)  # Nó de despesa: índices 1 a 7
            values.append(total_receitas * prop)
        return source, target, values

    def define_nodes(
        self,
        gasto_bancagem,
        gasto_comissao,
        gasto_custo_fixo,
        gasto_custo_op,
        gasto_folha_adm,
        gasto_imposto,
        gasto_rocam,
        total_receitas,
    ):
        labels = [
            f"Receitas\n({total_receitas:,.2f})",
            f"Roçagem e Limpeza\n({gasto_rocam:,.2f})",
            f"Custo OP\n({gasto_custo_op:,.2f})",
            f"Comissão\n({gasto_comissao:,.2f})",
            f"Folha ADM\n({gasto_folha_adm:,.2f})",
            f"Imposto\n({gasto_imposto:,.2f})",
            f"Bancagem\n({gasto_bancagem:,.2f})",
            f"Custo Fixo\n({gasto_custo_fixo:,.2f})",
        ]
        return labels

    def calc_totals(self, df):
        total_receitas = df["Valor"].sum()
        gasto_rocam = df["Roçagem e Limpeza Mensal"].sum()
        gasto_custo_op = df["Custo OP"].sum()
        gasto_comissao = df["Comissão"].sum()
        gasto_folha_adm = df["Folha ADM"].sum()
        gasto_imposto = df["Imposto"].sum()
        gasto_bancagem = df["Bancagem"].sum()
        gasto_custo_fixo = df["Custo Fixo"].sum()
        total_gastos = (
            gasto_rocam
            + gasto_custo_op
            + gasto_comissao
            + gasto_folha_adm
            + gasto_imposto
            + gasto_bancagem
            + gasto_custo_fixo
        )
        return (
            gasto_bancagem,
            gasto_comissao,
            gasto_custo_fixo,
            gasto_custo_op,
            gasto_folha_adm,
            gasto_imposto,
            gasto_rocam,
            total_gastos,
            total_receitas,
        )

    def prepare_df(self):
        df = self.om_data.copy()
        df["Valor"] = df["Valor"].apply(convert_currency)
        return df
