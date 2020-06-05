#version 130

in vec4 p3d_Vertex;
in vec4 p3d_Color;

uniform mat4 p3d_ModelMatrix;
uniform mat4 p3d_ViewMatrix;
uniform mat4 p3d_ProjectionMatrix;
uniform vec3 cam_pos;
uniform vec3 gizmo_pos;

out vec4 Color;

void main() {
	Color = p3d_Color;
	float distance = length(cam_pos - gizmo_pos);
	float scaleFactor = distance / 20;
	mat4 scaleMat = mat4(scaleFactor, 0, 0, 0,
						 0, scaleFactor, 0, 0,
						 0, 0, scaleFactor, 0,
						 0, 0, 0, 1);
	gl_Position = p3d_ProjectionMatrix * p3d_ViewMatrix * p3d_ModelMatrix * scaleMat * p3d_Vertex;
}