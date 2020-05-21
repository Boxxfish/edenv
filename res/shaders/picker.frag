#version 130

uniform int object_id;

void main() {
	vec4 color;
	color.x = (object_id) / 255.0;
	color.y = (object_id) / 255.0;
	color.z = (object_id) / 255.0;
	color.w = 1;
	gl_FragColor = color;
}