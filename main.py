import datetime
import plotly.express as px
import pandas as pd
import streamlit as st
fund_col_dict = {'natl_bk': '大型商业银行/政策性银行',
                 'jnt_bk': '股份制商业银行',
                 'city_bk': '城市商业银行',
                 'fn_bk': '外资银行',
                 'rural_inst': '农村金融机构',
                 'sec': '证券公司',
                 'ins': '保险公司',
                 'fund': '基金公司及产品',
                 'wm': '理财子公司理财类产品',
                 'mny_mkt_fund': '货币市场基金',
                 'fn_inst': '境外机构',
                 'oth_prdct': '其他产品类',
                 'oth': '其他',
}
fund_col = list(fund_col_dict.values())


@st.experimental_memo(max_entries=2)
def get_data()->pd.DataFrame:
    # 读取数据
    df = pd.read_excel("cfets_bond_trade_activity-sample.xlsx")
    df.rename(columns=fund_col_dict, inplace=True)
    return df


@st.experimental_memo(max_entries=2)
def get_bond_name():
    df = get_data()
    return list(set(df['sym']))


def main():
    df = get_data()
    bond_name = get_bond_name()
    date_start = st.date_input(label="开始日期", value=df['actual_date'].iloc[0])
    date_end = st.date_input(label="结束日期", value=df['actual_date'].iloc[-1])
    date_start = datetime.datetime.combine(date_start, datetime.datetime.min.time())
    date_end = datetime.datetime.combine(date_end, datetime.datetime.min.time())
    use_text = st.checkbox(label="开启文本输入选择", value=False)
    l, r = st.columns(2)
    with l:
        if not use_text:
            select_bond = st.selectbox(label='输入债券名', options=bond_name)
        else:
            st.empty()
    with r:
        if use_text:
            select_bond = st.text_input(label="输入债券名")
        else:
            st.empty()
    if use_text:
        if select_bond not in bond_name:
            st.warning("输入的债券名不合法，请检查输入")
            return
    # 重新选取数据
    select_df = df[df['sym'] == select_bond]
    select_df = select_df[select_df['actual_date'] >= date_start]
    select_df = select_df[select_df['actual_date'] <= date_end]
    # 统计数据
    stas_result = select_df.groupby("actual_date")[fund_col].sum().sum()
    stas_result = pd.DataFrame(stas_result, columns={"机构交易情况（亿元）"})
    st.table(stas_result)
    fig = px.bar(stas_result, y='机构交易情况（亿元）',
                 hover_data=['机构交易情况（亿元）'], color='机构交易情况（亿元）',
                 height=400)
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()