#define GL_SILENCE_DEPRECATION

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <math.h>

#include <wchar.h>

#ifdef _WIN32
	#include <Windows.h>
#endif

#include <glad/glad.h>
#include <GLFW/glfw3.h>

const int WINDOW_WIDTH = 1024;
const int WINDOW_HEIGHT = 768;

const char *vertexShaderSource = "#version 330 core\n"
	"layout (location = 0) in vec3 aPos;\n"
	"void main()\n"
	"{\n"
	"   gl_Position = vec4(aPos, 1.0);\n"
	"}\0";
const char *fragmentShaderSource = "#version 330 core\n"
	"out vec4 FragColor;\n"
	"void main()\n"
	"{\n"
	"   FragColor = vec4(0.0f, 0.0f, 0.0f, 1.0f);\n"
	"}\n\0";

void key_callbak (GLFWwindow *window, int key, int scancode, int action, int mode);
void frame_buffer_size_callbak (GLFWwindow* window, int width, int height);

int main(int argc, char const *argv[])
{

	#ifdef _WIN32
		//http://m.blog.csdn.net/article/details?id=52789570
		//控制檯顯示亂碼糾正
		system("chcp 65001"); //設定字符集（使用SetConsoleCP(65001)設定無效，原因未知）
		// SetConsoleOutputCP (65001);
		CONSOLE_FONT_INFOEX info = {0}; // 以下設定字型來支援中文顯示。
		info.cbSize = sizeof(info);
		info.dwFontSize.Y = 16; // leave X as zero
		info.FontWeight = FW_NORMAL;
		wcscpy(info.FaceName, L"Consolas");
		SetCurrentConsoleFontEx(GetStdHandle(STD_OUTPUT_HANDLE), 0, &info);
	#endif

	// glfwInit();
	if(!glfwInit()) {
		std::cout << "glfwInit fail!" << std::endl;
		glfwTerminate();
		return -1;
	}
	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3); // version a.b ---> a=MAJOR=3
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3); // version a.b ---> b=MINOR=3
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
	glfwWindowHint(GLFW_RESIZABLE, GL_TRUE); // printf("Set COMPAT hint.\n");
	glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
	GLFWwindow *window = glfwCreateWindow(WINDOW_WIDTH, WINDOW_HEIGHT, "奎佑征服宇宙", NULL, NULL);
	if (window == NULL) {
		std::cout << "window is not created!" << std::endl;
		glfwTerminate();
		return -1;
	}
	glfwMakeContextCurrent(window);
	if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
		std::cout << "Cannot load GLAD!" << std::endl;
		glfwTerminate();
		return -1;
	}
	glfwSetKeyCallback(window, key_callbak);
	glfwSetFramebufferSizeCallback(window, frame_buffer_size_callbak);
	// glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT);
	// std::cout << "hhahahaha" << std::endl;

	int vertexShader = glCreateShader(GL_VERTEX_SHADER);
	glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
	glCompileShader(vertexShader);
	// check for shader compile errors
	int success;
	char infoLog[512];
	glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);
	if (!success)
	{
		glGetShaderInfoLog(vertexShader, 512, NULL, infoLog);
		std::cout << "ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" << infoLog << std::endl;
	}
	// fragment shader
	int fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
	glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
	glCompileShader(fragmentShader);
	// check for shader compile errors
	glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &success);
	if (!success)
	{
		glGetShaderInfoLog(fragmentShader, 512, NULL, infoLog);
		std::cout << "ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n" << infoLog << std::endl;
	}
	// link shaders
	int shaderProgram = glCreateProgram();
	glAttachShader(shaderProgram, vertexShader);
	glAttachShader(shaderProgram, fragmentShader);
	glLinkProgram(shaderProgram);
	// check for linking errors
	glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
	if (!success) {
		glGetProgramInfoLog(shaderProgram, 512, NULL, infoLog);
		std::cout << "ERROR::SHADER::PROGRAM::LINKING_FAILED\n" << infoLog << std::endl;
	}
	glDeleteShader(vertexShader);
	glDeleteShader(fragmentShader);


	float vertices[] = {
		-0.5f, -0.5f, 0.0f,
		 0.5f, -0.5f, 0.0f,
		 0.0f,  0.5f, 0.0f
	};

	unsigned int VAO;
	glGenVertexArrays(1, &VAO);
	glBindVertexArray(VAO);
	unsigned int VBO;
	glGenBuffers(1, &VBO);
	glBindBuffer(GL_ARRAY_BUFFER, VBO);
	glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
	glEnableVertexAttribArray(0);

	// uncomment this call to draw in wireframe polygons.
	// glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);

	while (!glfwWindowShouldClose(window)) {
		glfwPollEvents();
		glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		glUseProgram(shaderProgram);
		glBindVertexArray(VAO);
		glDrawArrays(GL_TRIANGLES, 0, 3);
		glfwSwapBuffers(window);
	}
	glfwTerminate();
	return 0;
}

void key_callbak (GLFWwindow *window, int key, int scancode, int action, int mode) {
	if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS) {
		glfwSetWindowShouldClose(window, GL_TRUE);
		std::cout << " 感謝您征服宇宙 " << std::endl;
	}
}

void frame_buffer_size_callbak (GLFWwindow* window, int width, int height) {
	glViewport(0, 0, width, height);
}