import streamlit as st
import pandas as pd

# ===================== CONFIGURAÇÕES DA PÁGINA =====================
st.set_page_config(
    page_title="Orçamento de Móveis Planejados",
    page_icon="🪑",
    layout="centered"
)

# ===================== TABELAS DE PREÇOS =====================
precos = {"Branco": 1050, "Amadeirado": 1150, "Laca": 1250}

precos_painel = {
    "Branco": {"Comum": 500, "Ripado": 560},
    "Laca": {"Comum": 640, "Ripado": 710},
    "Amadeirado": {"Comum": 560, "Ripado": 660}
}

tipos_moveis = ["Painel", "Guarda-Roupa", "Armário de Cozinha"]

# ===================== CABEÇALHO =====================
st.image("static/logo.png", width=160)
st.title("🪑 Orçamento de Móveis Planejados")
st.markdown(
    "Calcule facilmente o valor estimado de **painéis**, **armários** e **móveis planejados**."
)

st.divider()

# ===================== FORMULÁRIO =====================
with st.form("orcamento_form"):
    tipo_movel = st.selectbox("Tipo de Móvel:", [""] + tipos_moveis)

    # Tipo de painel só aparece se for painel
    tipo_painel = "Comum"
    if tipo_movel == "Painel":
        tipo_painel = st.selectbox("Tipo de Painel:", ["Comum", "Ripado"])

    # Campos lado a lado
    col1, col2 = st.columns(2)
    with col1:
        altura = st.number_input("Altura (m):", min_value=0.5, max_value=5.0, step=0.01)
    with col2:
        largura = st.number_input("Largura (m):", min_value=0.5, max_value=10.0, step=0.01)

    material = st.selectbox("Material:", ["", "Branco", "Laca", "Amadeirado"])
    aplicar_desconto = st.checkbox("Aplicar desconto de 5%")

    calcular = st.form_submit_button("💰 Calcular Orçamento")

# ===================== CÁLCULO DO ORÇAMENTO =====================
if calcular:
    if not tipo_movel or not material:
        st.warning("⚠️ Por favor, selecione o tipo de móvel e o material.")
    else:
        try:
            altura_calculada = max(altura, 1.0)

            # Seleciona o preço correto
            if tipo_movel == "Painel":
                if material in precos_painel:
                    preco_m2 = precos_painel[material][tipo_painel]
                else:
                    st.warning("⚠️ Painel só disponível em Branco, Laca ou Amadeirado.")
                    st.stop()
            else:
                preco_m2 = precos[material]

            # Cálculos
            area = altura_calculada * largura
            custo_original = area * preco_m2

            if aplicar_desconto:
                custo_final = custo_original * 0.95
                desconto_texto = "Desconto aplicado de 5%"
            else:
                custo_final = custo_original
                desconto_texto = "Sem desconto"

            # ===================== EXIBIÇÃO DO RESULTADO =====================
            st.success("✅ Orçamento calculado com sucesso!")

            with st.container():
                st.markdown("---")
                st.subheader("📋 Detalhes do Orçamento")
                st.markdown(f"""
                **Tipo de Móvel:** {tipo_movel}  
                **Tipo de Painel:** {tipo_painel if tipo_movel == "Painel" else "—"}  
                **Material:** {material}  
                **Altura:** {altura_calculada:.2f} m  
                **Largura:** {largura:.2f} m  
                **Área Total:** {area:.2f} m²  
                **Valor por m²:** R$ {preco_m2:,.2f}  
                **{desconto_texto}**  
                ### 💰 Valor Final: R$ {custo_final:,.2f}
                """)

            # ===================== EXPORTAÇÃO =====================
            dados = {
                "Tipo de Móvel": [tipo_movel],
                "Material": [material],
                "Altura (m)": [altura_calculada],
                "Largura (m)": [largura],
                "Área (m²)": [area],
                "Valor por m² (R$)": [preco_m2],
                "Desconto": [desconto_texto],
                "Valor Final (R$)": [custo_final]
            }

            df = pd.DataFrame(dados)
            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "⬇️ Baixar Orçamento (CSV)",
                csv,
                "orcamento_versatto.csv",
                "text/csv",
                help="Baixe uma cópia do orçamento em formato CSV."
            )

        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")

# ===================== RODAPÉ =====================
st.divider()
st.caption("© 2025 Versatto Móveis Planejados — Calculadora de Orçamentos")
