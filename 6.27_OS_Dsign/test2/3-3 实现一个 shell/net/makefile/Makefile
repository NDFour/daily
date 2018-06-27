maino=shell_main
evalo=shell_eval
parseo=shell_parseline 
buildino=shell_buildin_command 

myshell: $(maino).o $(evalo).o $(parseo).o $(buildino).o
	gcc $(maino).o $(evalo).o $(parseo).o shell_buildin_command.o -o myshell

$(maino).o: $(maino).c myshell.h
	gcc -c $(maino).c -o $(maino).o

$(evalo).o: $(evalo).c myshell.h
	gcc -c $(evalo).c -o $(evalo).o

shell_parseline.o: shell_parseline.c myshell.h
	gcc -c shell_parseline.c -o shell_parseline.o

shell_buildin_command.o: shell_buildin_command.c myshell.h
	gcc -c shell_buildin_command.c -o shell_buildin_command.o

clean:
	rm -f *.o myshell
