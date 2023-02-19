import argparse
import sys
from TableGeneration.GenerateTable import GenerateTable


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num', type=int, default=1, help='生成表的数量')
    # output path
    parser.add_argument('--output', type=str, default='output/simple_table')  # 数据保存路径
    # courp path
    parser.add_argument('--ch_dict_path', type=str, default='dict/ch_news.txt')
    parser.add_argument('--en_dict_path', type=str, default='dict/en_corpus.txt')

    # table settings

    # 单元格box 类型
    parser.add_argument('--cell_box_type', type=str, default='cell',
                        help='单元格：使用单元格位置作为单元格框；文本：将单元格中文本的位置用作单元格框')
    # 行和列
    parser.add_argument('--min_row', type=int, default=3, help='表中的最小行数')
    parser.add_argument('--max_row', type=int, default=15, help='表中的最大行数')
    parser.add_argument('--min_col', type=int, default=3, help='表中的最小列')
    parser.add_argument('--max_col', type=int, default=10, help='表中的最大列数')
    # 单元格行和列的跨度
    parser.add_argument('--max_span_row_count', type=int, default=3, help='最大跨度行')
    parser.add_argument('--max_span_col_count', type=int, default=3, help='最大跨度列')
    parser.add_argument('--max_span_value', type=int, default=10, help='行跨度和列跨度中的最大值')
    # 单元格长度
    parser.add_argument('--min_txt_len', type=int, default=2, help='单元格中的最小字符数')
    parser.add_argument('--max_txt_len', type=int, default=10, help='单元格中的最大字符数')
    # color
    # 彩色单元格表格
    # python3 generate_data.py --output output/color_simple_table --num=1 --color_prob=0.3
    parser.add_argument('--color_prob', type=float, default=0, help='彩色单元格概率 --color_prob=0.3')
    # 单元格尺寸
    parser.add_argument('--cell_max_width', type=int, default=0, help='最大宽度cell ')
    parser.add_argument('--cell_max_height', type=int, default=0, help='最大高度 cell')
    # 浏览器窗口尺寸
    parser.add_argument('--brower_width', type=int, default=1920, help='浏览器宽度 ')
    parser.add_argument('--brower_height', type=int, default=2440, help='浏览器高度')
    parser.add_argument('--brower', type=str, default='chrome', help='chrome or firefox')

    args = parser.parse_args()
    if args.brower == 'chrome' and sys.platform == 'darwin':
        print('火狐推荐用于Mac OS，错误是您选择的是Chrome')
        sys.exit(0)
    # for keys, value in parser.parse_args()._get_kwargs():
    #     print('{}="{}"'.format(keys, value))
    return args


if __name__ == '__main__':
    args = parse_args()
    t = GenerateTable(output=args.output,
                      ch_dict_path=args.ch_dict_path,
                      en_dict_path=args.en_dict_path,
                      cell_box_type=args.cell_box_type,
                      min_row=args.min_row,
                      max_row=args.max_row,
                      min_col=args.min_col,
                      max_col=args.max_col,
                      min_txt_len=args.min_txt_len,
                      max_txt_len=args.max_txt_len,
                      max_span_row_count=args.max_span_row_count,
                      max_span_col_count=args.max_span_col_count,
                      max_span_value=args.max_span_value,
                      color_prob=args.color_prob,
                      cell_max_width=args.cell_max_width,
                      cell_max_height=args.cell_max_height,
                      brower=args.brower,
                      brower_width=args.brower_width,
                      brower_height=args.brower_height)

    t.gen_table_img(args.num)
    t.close()
