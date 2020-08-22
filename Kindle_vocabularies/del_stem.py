

def del_stem():
	old_file_name = 'final_1500_end.txt'
	new_file_name = 'NEW_' + old_file_name

	with open(old_file_name, 'r') as f:
		last_line = ''
		for line in f.readlines():
			# print(line)
			# print('@@@@@@@@@')

			with open(new_file_name, 'a') as f_new:
				# f_new.write(line)
				if line[6:].strip() != last_line[6:].strip():
					# print(line)
					f_new.write(line)
				else:
					print(line)

			last_line = line

if __name__ == '__main__':
	del_stem()

