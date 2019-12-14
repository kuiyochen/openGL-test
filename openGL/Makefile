CC=g++
CCFLAGS=-Wall -g -std=c++11
PREFLAGS=-Wall -c -std=c++11
INCLUDE=-I ./include/
LIBS=-L ./lib/ -lglfw3 -lgdi32 -lopengl32
AUX=*.o
DEPS=main.cpp

main: $(AUX) $(DEPS)
	@echo "link $@"
	$(CC) $(INCLUDE) $(CCFLAGS) -o $@ $^ $(LIBS)

%.o: %.cpp *.h
	@echo "CC $@"
	$(CC) $(INCLUDE) $(PREFLAGS) -o $@ $<

# mingw32-make
# g++ -I include -L lib glad.o main.cpp -lglfw3 -lgdi32 -lopengl32 -o main.exe

$(V).SILENT: