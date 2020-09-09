#导入词云的包
from wordcloud import WordCloud
#导入matplotlib作图的包
import matplotlib.pyplot as plt


class Gen_Word_Cloud(object):
	src_name = 'sources/'
	dst_name = ''

	def __init__(self, src_name):
		self.src_name += src_name
		self.dst_name = src_name


	def gen_pic(self):
		with open(self.src_name, 'r', encoding = 'utf-8') as f:
			text = f.read()

			#生成一个词云对象
			wordcloud = WordCloud(
			        background_color="white", #设置背景为白色，默认为黑色
			        width=1500,              #设置图片的宽度
			        height=960,              #设置图片的高度
			        margin=10               #设置图片的边缘
			        ).generate(text)
			# 绘制图片
			plt.imshow(wordcloud)
			# 消除坐标轴
			plt.axis("off")
			# 展示图片
			plt.show()
			# 保存图片
			wordcloud.to_file( 'output/' + self.dst_name + '.png')


if __name__ == '__main__':
	gen_word_cloud = Gen_Word_Cloud('animal_farm.txt')
	gen_word_cloud.gen_pic()

