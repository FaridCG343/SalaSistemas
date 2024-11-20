#version 330 core

in vec4 fragColor;
in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform sampler2D u_texture;
uniform Light light;
uniform vec3 camPos;

out vec4 FragColor;

vec3 getLight(vec3 color){
    vec3 Normal = normalize(normal);
    // Ambient
    vec3 ambient = light.Ia;

    // Diffuse
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    vec3 diffuse = light.Id * diff;

    // Specular
    vec3 viewDir = normalize(camPos -fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = light.Is * spec;
    return color * (ambient + diffuse + specular);
}

void main() {
    float gamma = 2.2;
    vec3 color = texture(u_texture, uv_0).rgb;
    color = pow(color, vec3(gamma));

    color = getLight(color);

    // gamma correction
    color = pow(color, vec3(1.0/gamma));

    FragColor = vec4(color, 1.0);
}