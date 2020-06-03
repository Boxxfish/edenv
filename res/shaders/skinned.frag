#version 330

in vec2 TexCoord;
in vec3 Normal;
in vec4 Color;

uniform struct {
  vec4 ambient;
  vec4 diffuse;
  vec4 emission;
  vec3 specular;
  float shininess;
  
  vec4 baseColor;
  float roughness;
  float metallic;
  float refractiveIndex;
} p3d_Material;

const int LIGHT_COUNT = 4;
uniform struct p3d_LightSourceParameters {
  vec4 color;
  vec4 position;
} p3d_LightSource[LIGHT_COUNT];

uniform sampler2D p3d_Texture0;

void main() {
	vec4 ambient = vec4(0, 0, 0, 0);
	vec4 diffuse = vec4(0, 0, 0, 0);
	vec4 specular = vec4(0, 0, 0, 0);
	
	// Iterate over lights
	for (int i = 0; i < LIGHT_COUNT; i++) {
		vec3 light_pos = p3d_LightSource[i].position.xyz;
		vec3 norm_light_pos = normalize(light_pos);
	
		// Diffuse
		diffuse += dot(norm_light_pos, Normal) * p3d_LightSource[i].color;
	}

	vec4 tex_color = texture(p3d_Texture0, TexCoord);
	gl_FragColor = (ambient + diffuse + specular) * Color * tex_color;
}