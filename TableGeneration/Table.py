import random
import numpy as np


def load_courp(p, join_c=''):
    courp = []
    with open(p, mode='r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip("\n").strip("\r\n")
            courp.append(line)
    courp = join_c.join(courp)
    return courp


class Table:
    def __init__(self,
                 ch_dict_path,
                 en_dict_path,
                 cell_box_type='cell',
                 no_of_rows=14,
                 no_of_cols=14,
                 min_txt_len=2,
                 max_txt_len=7,
                 max_span_row_count=3,
                 max_span_col_count=3,
                 max_span_value=20,
                 color_prob=0,
                 cell_max_width=0,
                 cell_max_height=0,
                 border_type=None
                 ):
        assert cell_box_type in [
            'cell', 'text'
        ], "cell_box_type must in ['cell', 'text'],cell: use cell location as cell box; text: use location of text in cell as cell box"
        self.cell_box_type = cell_box_type
        self.no_of_rows = no_of_rows
        self.no_of_cols = no_of_cols
        self.max_txt_len = max_txt_len
        self.min_txt_len = min_txt_len
        self.color_prob = color_prob
        self.cell_max_width = cell_max_width
        self.cell_max_height = cell_max_height
        self.max_span_row_count = max_span_row_count
        self.max_span_col_count = max_span_col_count
        self.max_span_value = max_span_value

        self.dict = ''
        self.ch = load_courp(ch_dict_path, '')
        self.en = load_courp(en_dict_path, '')  # "abcdefghijklmnopqrstuvwxyz"
        # 表格边框
        self.pre_boder_style = {
            1: {
                'name': 'border',
                'style': {
                    'table': 'border:1px solid black;',
                    'td': 'border:1px solid black;',
                    'th': 'border:1px solid black;'
                }
            },  # 绘制全部边框
            2: {
                'name': 'border_top',
                'style': {
                    'table': 'border-top:1px solid black;',
                    'td': 'border-top:1px solid black;',
                    'th': 'border-top:1px solid black;'
                }
            },  # 绘制上横线
            3: {
                'name': 'border_bottom',
                'style': {
                    'table': 'border-bottom:1px solid black;',
                    'td': 'border-bottom:1px solid black;',
                    'th': 'border-bottom:1px solid black;'
                }
            },  # 绘制下横线
            4: {
                'name': 'head_border_bottom',
                'style': {
                    'th': 'border-bottom: 1px solid black;'
                }
            },  # 绘制 head 下横线
            5: {
                'name': 'no_border',
                'style': ''
            },  # 无边框
            6: {
                'name': 'border_left',
                'style': {
                    'table': 'border-left:1px solid black;',
                    'td': 'border-left:1px solid black;',
                    'th': 'border-left:1px solid black;'
                }
            },  # 绘制左竖线
            7: {
                'name': 'border_right',
                'style': {
                    'table': 'border-right:1px solid black;',
                    'td': 'border-right:1px solid black;',
                    'th': 'border-right:1px solid black;'
                }
            }  # 绘制右竖线
        }

        # 随机选择一种,或者参数传入
        self.border_type = random.choice(list(self.pre_boder_style.keys())) if not border_type else border_type

        self.spanflag = False
        '''cell_types矩阵有两个可能的值：
            c: ch
            e: en
            n: number
            t: ''
            m: money

        '''
        self.cell_types = np.chararray(shape=(self.no_of_rows,
                                              self.no_of_cols))
        '''标头矩阵有两个可能的值：“s”和“h”，其中“h”表示标头，“s”表示简单文本'''
        self.headers = np.chararray(shape=(self.no_of_rows, self.no_of_cols))
        '''矩阵中某个位置的正值表示要跨越的列数，-1表示跳过该单元格作为跨越列的一部分'''
        self.col_spans_matrix = np.zeros(shape=(self.no_of_rows,
                                                self.no_of_cols))
        '''位置处的正值表示要跨越的行数，-1将显示跳过该单元格作为跨越行的一部分'''
        self.row_spans_matrix = np.zeros(shape=(self.no_of_rows,
                                                self.no_of_cols))
        '''missing_cells将包含一个（行、列）对列表，每对都将显示一个不应写入文本的单元格'''
        self.missing_cells = []

        '''header_count将跟踪被视为标题的顶部行数和左侧列数'''
        self.header_count = {'r': 2, 'c': 0}

    def get_log_value(self):
        '''

        @return: log base 2 (x)
        '''
        import math
        return int(math.log(self.no_of_rows * self.no_of_cols, 2))

    def define_col_types(self):
        '''
        我们定义每个列中的数据类型。我们将数据分为三种类型：
        1. 'n': 数字
        2. 'w': 单词
        3. 'r': 其他类型（包含特殊字符）
        @return:
        '''
        prob_words = 0.3
        prob_numbers = 0.5
        prob_ens = 0.1
        prob_money = 0.1
        for i, type in enumerate(
                random.choices(
                    ['n', 'm', 'c', 'e'],
                    weights=[prob_numbers, prob_money, prob_words, prob_ens],
                    k=self.no_of_cols)):
            self.cell_types[:, i] = type
        '''The headers should be of type word'''
        self.cell_types[0:2, :] = 'c'
        '''All cells should have simple text but the headers'''
        self.headers[:] = 's'
        self.headers[0:2, :] = 'h'

    def generate_random_text(self, type):
        '''
        cell_types矩阵有两个可能的值:
            c: ch
            e: en
            n: number
            t: ''
            m: money
        @param type:
        @return:
        '''
        if type in ['n', 'm']:
            max_num = random.choice([10, 100, 1000, 10000])
            if random.random() < 0.5:
                out = '{:.2f}'.format(random.random() * max_num)
            elif random.random() < 0.7:
                out = '{:.0f}'.format(random.random() * max_num)
            else:
                # 随机保留小数点后2位
                out = str(random.random() *
                          max_num)[:len(str(max_num)) + random.randint(0, 3)]
            if type == 'm':
                out = '$' + out
        elif (type == 'e'):
            txt_len = random.randint(self.min_txt_len, self.max_txt_len)
            out = self.generate_text(txt_len, self.en)
            # 50% 的概率第一个字母大写
            if random.random() < 0.5:
                out[0] = out[0].upper()
        elif type == 't':
            out = ''
        else:
            txt_len = random.randint(self.min_txt_len, self.max_txt_len)
            out = self.generate_text(txt_len, self.ch)
        return ''.join(out)

    def generate_text(self, txt_len, dict):
        random_star_idx = random.randint(0, len(dict) - txt_len)
        txt = dict[random_star_idx:random_star_idx + txt_len]
        return list(txt)

    def agnostic_span_indices(self, maxvalue, max_num=3):
        '''
        跨度索引。可用于行或列跨度
        跨度索引存储行或列跨度的起始索引，而Span_length将存储
        从起始索引开始的跨度长度（以单元格为单位）。
        @param maxvalue:
        @param max_num:
        @return:
        '''
        span_indices = []
        span_lengths = []
        # 随机选择范围计数
        span_count = random.randint(1, max_num)
        if (span_count >= maxvalue):
            return [], []

        indices = sorted(random.sample(list(range(0, maxvalue)), span_count))

        # 获取span开始idx和span值
        starting_index = 0
        for i, index in enumerate(indices):
            if (starting_index > index):
                continue

            max_lengths = maxvalue - index
            if (max_lengths < 2):
                break
            len_span = random.randint(1, min(max_lengths, self.max_span_value))

            if (len_span > 1):
                span_lengths.append(len_span)
                span_indices.append(index)
                starting_index = index + len_span

        return span_indices, span_lengths

    def make_first_row_spans(self):
        '''
        制作第一行spans
        @return:
        '''
        while (True):  # 迭代直到得到一些第一行跨度索引
            header_span_indices, header_span_lengths = self.agnostic_span_indices(
                self.no_of_cols, self.max_span_col_count)
            if (len(header_span_indices) != 0 and
                    len(header_span_lengths) != 0):
                break

        # 制作第一排跨度矩阵
        row_span_indices = []
        for index, length in zip(header_span_indices, header_span_lengths):
            self.spanflag = True
            self.col_spans_matrix[0, index] = length
            self.col_spans_matrix[0, index + 1:index + length] = -1
            row_span_indices += list(range(index, index + length))

        #对于非span列，将其设置为行span值2
        b = list(
            filter(lambda x: x not in row_span_indices,
                   list(range(self.no_of_cols))))
        self.row_spans_matrix[0, b] = 2
        self.row_spans_matrix[1, b] = -1

    def make_first_col_spans(self):
        '''
        在每行的第一列上创建一些随机行跨度
        @return:
        '''
        colnumber = 0
        # 跳过顶部2行标题
        span_indices, span_lengths = self.agnostic_span_indices(
            self.no_of_rows - 2, self.max_span_row_count)
        span_indices = [x + 2 for x in span_indices]

        for index, length in zip(span_indices, span_lengths):
            self.spanflag = True
            self.row_spans_matrix[index, colnumber] = length
            self.row_spans_matrix[index + 1:index + length, colnumber] = -1
        self.headers[:, colnumber] = 'h'
        self.header_count['c'] += 1

    def generate_missing_cells(self):
        '''
        这是随机选择一些单元格为空（不包含任何文本）
        @return:
        '''
        missing = np.random.random(size=(self.get_log_value(), 2))
        missing[:, 0] = (self.no_of_rows - 1 - self.header_count['r']
                         ) * missing[:, 0] + self.header_count['r']
        missing[:, 1] = (self.no_of_rows - 1 - self.header_count['c']
                         ) * missing[:, 1] + self.header_count['c']
        for arr in missing:
            self.missing_cells.append((int(arr[0]), int(arr[1])))

    def create_style(self):
        '''
        此函数将动态创建样式表。此样式表本质上创建了表格中的边框类型
        @return:
        '''
        boder_style = self.pre_boder_style[self.border_type]['style']
        style = '<head><meta charset="UTF-8"><style>'
        style += "html{background-color: white;}table{"

        # 表格中文本左右对齐方式
        style += "text-align:{};".format(
            random.choices(
                ['left', 'right', 'center'], weights=[0.25, 0.25, 0.5])[0])
        style += "border-collapse:collapse;"
        if 'table' in boder_style:
            style += boder_style['table']
        style += "}td{"

        # 文本上下居中
        if random.random() < 0.5:
            style += "align: center;valign: middle;"
        # 大单元格
        if self.cell_max_height != 0:
            style += "height: {}px;".format(
                random.randint(self.cell_max_height // 2,
                               self.cell_max_height))
        if self.cell_max_width != 0:
            style += "width: {}px;".format(
                random.randint(self.cell_max_width // 2, self.cell_max_width))
        # 文本换行
        style += "word-break:break-all;"
        if 'td' in boder_style:
            style += boder_style['td']

        style += "}th{padding:6px;padding-left: 15px;padding-right: 15px;"
        if 'th' in boder_style:
            style += boder_style['th']
        style += '}'

        style += "</style></head>"
        return style

    @property
    def create_html(self):
        '''
        制作表格 html
        取决于各种条件，常规或不规则的标题、
        表格类型和边框类型，此函数创建等效的html剧本
        @return:
        '''
        idcounter = 0
        structure = []
        temparr = ['td', 'th']
        html = """<html>"""
        html += self.create_style()
        html += '<body><table>'
        # html += '<table style="width: 100%; table-layout:fixed;">'
        for r in range(self.no_of_rows):
            html += '<tr>'
            structure.append('<tr>')
            for c in range(self.no_of_cols):
                text_type = self.cell_types[r, c].decode('utf-8')
                row_span_value = int(self.row_spans_matrix[r, c])
                col_span_value = int(self.col_spans_matrix[r, c])
                htmlcol = temparr[['s', 'h'].index(self.headers[r][c].decode('utf-8'))]

                if self.cell_box_type == 'cell':
                    htmlcol += ' id={}'.format(idcounter)

                htmlcol_style = htmlcol

                # 设置颜色
                if (col_span_value != 0) or (r, c) not in self.missing_cells:
                    if random.random() < self.color_prob:
                        color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
                        htmlcol_style += ' style="background-color: rgba({}, {}, {},1);"'.format(color[0], color[1], color[2])

                if (row_span_value == -1):
                    continue

                elif (row_span_value > 0):

                    html += '<' + htmlcol_style + ' rowspan=\"' + str(row_span_value) + '">'
                    if row_span_value > 1:
                        structure.append('<td')
                        structure.append(' rowspan=\"{}\"'.format(row_span_value))
                        structure.append('>')
                    else:
                        structure.append('<td>')
                else:
                    if (col_span_value == 0):
                        if (r, c) in self.missing_cells:
                            text_type = 't'

                    if (col_span_value == -1):
                        continue

                    html += '<' + htmlcol_style + ' colspan=\"' + str(col_span_value) + '">'
                    if col_span_value > 1:
                        structure.append('<td')
                        structure.append(' colspan=\"{}\"'.format(col_span_value))
                        structure.append('>')
                    else:
                        structure.append('<td>')
                if c == 0:
                    # 第一行设置为中英文
                    text_type = random.choice(['c', 'e'])

                txt = self.generate_random_text(text_type)
                if self.cell_box_type == 'text':
                    txt = '<span id=' + str(idcounter) + '>' + txt + ' </span>'


                idcounter += 1
                html += txt + '</' + htmlcol + '>'
                structure.append('</td>')

            html += '</tr>'
            structure.append('</tr>')
        html += "<table></body></html>"
        return html, structure, idcounter

    def create(self):
        '''
        这将创建完整的表
        border_type:表边框类型
        @return:
        '''
        self.define_col_types()  # 定义每列的数据类型
        self.generate_missing_cells()  # 生成丢失的单元格
        # 随机选择一种 表格边框样式
        if self.border_type < 60:  # 绘制横线的情况下进行随机span
            # 第一行跨度
            if self.max_span_col_count > 0:
                self.make_first_row_spans()
            # 第一列跨度
            if random.random() < 1 and self.max_span_row_count > 0:
                self.make_first_col_spans()

        html, structure, idcounter = self.create_html  # 创建相同的html

        return idcounter, html, structure, self.pre_boder_style[
            self.border_type]['name']
