#version 330 core

layout(location = 0) in vec3 in_normal;
layout(location = 1) in vec3 in_position;

out vec3 fragColor;
out vec3 normal;
out vec3 fragPos;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

void main(){
    fragColor = vec3(1.0);
    fragPos = vec3(model * vec4(in_position, 1.0));
    normal = mat3(transpose(inverse(model))) * in_normal;
    gl_Position = projection * view * model * vec4(in_position, 1.0);
}