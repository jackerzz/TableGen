from TableGeneration.GenerateTable import GenerateTable
class TableConfig:
    def __init__(self):
        # 浏览器设置
        self.brower:str = "chrome"
        self.brower_height:int = 1338
        self.brower_width:int = 947

        # 单元格box 类型
        self.cell_box_type: str = "text"
        # self.cell_box_type: str = "cell"

        # 单元格尺寸
        self.cell_max_height:int =0
        self.cell_max_width:int = 0

        # 彩色单元格表格
        self.color_prob: float = 0         # python3 generate_data.py --output output/color_simple_table --num=1 --color_prob=0.3

        # 行和列
        self.max_col:int = 8
        self.min_col:int = 3
        self.max_row: int = 8
        self.min_row:int = 5

        # 单元格行和列的跨度
        self.max_span_col_count:int = 3
        self.max_span_row_count:int = 3
        self.max_span_value:int = 5

        # 单元格长度
        self.max_txt_len: int = 5
        self.min_txt_len:int = 2

        # 生成表的数量
        self.num:int =1

        # courp path
        self.ch_dict_path: str = "dict/ch_news.txt"
        self.en_dict_path: str = "dict/en_corpus.txt"

        # output path
        self.output: str = "output/simple_table"

        # 特殊参数
        self.border_type = 5 # 无边框


class Table(TableConfig):
    def __init__(self):
        super().__init__()
        self.t=GenerateTable(
            output=self.output,
            ch_dict_path=self.ch_dict_path,
            en_dict_path=self.en_dict_path,
            cell_box_type=self.cell_box_type,
            min_row=self.min_row,
            max_row=self.max_row,
            min_col=self.min_col,
            max_col=self.max_col,
            min_txt_len=self.min_txt_len,
            max_txt_len=self.max_txt_len,
            max_span_row_count=self.max_span_row_count,
            max_span_col_count=self.max_span_col_count,
            max_span_value=self.max_span_value,
            color_prob=self.color_prob,
            cell_max_width=self.cell_max_width,
            cell_max_height=self.cell_max_height,
            brower=self.brower,
            brower_width=self.brower_width,
            brower_height=self.brower_height,
            border_type=self.border_type
        )

    def run(self):
        self.t.gen_table_img(self.num)

    def close(self):
        self.t.close()


if __name__ == '__main__':
    table = Table()
    table.run()