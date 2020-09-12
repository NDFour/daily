import xlwt


class Write_2_Excel(object):

	file_name = ''
	words_list = []

	def __init__(self, file_name, words_list):
		self.file_name = file_name
		self.words_list = words_list

	#设置表格样式
	def set_style(self, name, height, bold = False, italic = False):
		style = xlwt.XFStyle()
		font = xlwt.Font()
		font.name = name
		font.bold = bold
		font.italic = italic
		font.color_index = 4
		font.height = height

		style.font = font

		return style


	# 设置表格 背景色
	def set_table_bg( self, style, color ):
		# Create the Pattern
		pattern = xlwt.Pattern() 
		# May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
		pattern.pattern = xlwt.Pattern.SOLID_PATTERN 
		# May be: 8 through 63. 0 = Black, 1 = White, 2 = Red,
		# 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 
		# 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow ,
		# almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 
		# 23 = Dark Gray, the list goes on...
		pattern.pattern_fore_colour = color

		# style = xlwt.XFStyle() # Create the Pattern
		style.pattern = pattern # Add Pattern to Style


	# 设置单元格内容对齐方式
	'''
	def set_table_alignment( style ):
		alignment = xlwt.Alignment() # Create Alignment
		# May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, 
		# HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
		alignment.horz = xlwt.Alignment.HORZ_CENTER 
		# May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
		alignment.vert = xlwt.Alignment.VERT_CENTER 

		style.alignment = alignment # Add Alignment to Style
	'''


	#写Excel
	def write_excel( self ):
		f = xlwt.Workbook(encoding = 'utf-8')
		sheet1 = f.add_sheet('词汇表',cell_overwrite_ok=True)

		row0 = ['单词', '音标', 'collins 排名', 'oxford 3000 核心词汇',
				'Bnc 排名', 'Frq 排名', '中文释义', '英文释义', '变形', '标签']

		# colum0 = ["张三","李四","恋习Python","小明","小红","无名"]

		style_for_wechat = self.set_style('Times New Roman',220, True, False)
		self.set_table_bg(style_for_wechat, 3) # 绿色背景

		#写第 0 行 —— 公众号推广
		wechat_ad = ['公', '众', '号' ,'：', '撞', '弯', '了', '腰', '（ 微信号：', 'free_to_read ）']
		for i in range(0, len(wechat_ad)):
			sheet1.write(0, i, wechat_ad[i], style_for_wechat)

		style_for_title = self.set_style('Times New Roman',220, True, False)
		self.set_table_bg(style_for_title, 5) # 黄色背景

		#写第 1 行 —— 标题
		for i in range(0,len(row0)):
			# 参数对应 行, 列, 值
			sheet1.write(2, i, row0[i], style_for_title)

		# 设置单元格样式
		# style = set_style('Times New Roman',220, True, False)
		style_bold = self.set_style('Times New Roman',220, True, False)
		style_italic = self.set_style('Times New Roman',220, False, True)
		style_normal = self.set_style('Times New Roman',220, False, False)

		j_cnt = 2
		for word in self.words_list:
			# 从第 2 行 开始写
			# 0: 公众号 推广信息
			# 1: 空行
			# 2: 表格 标题
			j_cnt += 1
			# 粗体
			sheet1.write(j_cnt, 0, word['word'], style_bold )
			# 斜体
			sheet1.write(j_cnt, 1, word['phonetic'], style_italic )
			sheet1.write(j_cnt, 2, word['collins'], style_normal )
			sheet1.write(j_cnt, 3, word['oxford'], style_normal )
			sheet1.write(j_cnt, 4, word['bnc'], style_normal )
			sheet1.write(j_cnt, 5, word['frq'], style_normal )
			sheet1.write(j_cnt, 6, word['translation'], style_normal )
			sheet1.write(j_cnt, 7, word['definition'], style_normal )
			sheet1.write(j_cnt, 8, word['exchange'], style_normal )
			sheet1.write(j_cnt, 9, word['tag'], style_normal )

		'''
		#写第一列
		for i in range(0,len(colum0)):
			sheet1.write(i+1,0,colum0[i],set_style('Times New Roman',220,True))

		sheet1.write(1,3,'2006/12/12')
		sheet1.write_merge(6,6,1,3,'未知')#合并行单元格
		sheet1.write_merge(1,2,3,3,'打游戏')#合并列单元格
		sheet1.write_merge(4,5,3,3,'打篮球')
		'''

		f.save( self.file_name )

if __name__ == '__main__':
	# write_excel()
	w_2_excel = Write_2_Excel('output/test_excel_name.xls', [])
	w_2_excel.write_excel()

