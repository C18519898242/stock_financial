import json

import commons
import guosen
import pandas as pd


def __save_overview_data():
    f_logger = commons.get_logger()
    f_logger.info("正在更新公司基本 ...")

    # 获取 stock info
    config = commons.Config()
    stock_info_file_data_path = config.get_file_path(r"data/stock_info.csv")

    # 创建自定义数据类型映射字典
    d_type_mapping = {'tickerSymbol': str, 'stockName': str}
    stock_df = pd.read_csv(stock_info_file_data_path, dtype=d_type_mapping)

    stock_df["pb"] = ""
    stock_df["pe"] = ""
    stock_df["industry1"] = ""
    stock_df["industry2"] = ""

    for index, row in stock_df.iterrows():
        symbol = row.tickerSymbol
        f_logger.info("正在下载 股票 {symbol} 信息, index is {index}".format(symbol=symbol, index=index))
        overview = guosen.get_overview_data(symbol)

        if overview is not None:
            stock_df.loc[index, "pb"] = overview["pb"]
            stock_df.loc[index, "pe"] = overview["pe"]
            stock_df.loc[index, "industry1"] = overview["industry1"]
            stock_df.loc[index, "industry2"] = overview["industry2"]

    financial_base_path = config.get_file_path(r"data\financial_base.csv")
    stock_df.to_csv(financial_base_path, encoding="utf-8-sig", index=False)


if __name__ == "__main__":
    __save_overview_data()
