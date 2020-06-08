#version 330

in vec4 p3d_Vertex;
in vec3 p3d_Normal;
in vec2 p3d_MultiTexCoord0;
in ivec4 joint;
in vec4 weight;
in vec4 p3d_Color;

uniform mat4 p3d_ViewProjectionMatrix;
uniform mat3 p3d_NormalMatrix;
uniform mat4 p3d_ModelMatrix;
uniform mat4 p3d_ViewMatrix;

const int BONE_COUNT = 100;
uniform mat4 boneMats[BONE_COUNT];

out vec2 TexCoord;
out vec3 Normal;
out vec4 Color;

void main() {
	Color = p3d_Color;
	TexCoord = p3d_MultiTexCoord0;
	mat4 transformMat = boneMats[joint.x] * weight.x + boneMats[joint.y] * weight.y + boneMats[joint.z] * weight.z + boneMats[joint.w] * weight.w;
	mat4 NormalMatrix = transpose(inverse(p3d_ViewMatrix * transformMat * p3d_ModelMatrix));
	Normal = normalize((NormalMatrix * vec4(p3d_Normal, 0)).xyz);
	gl_Position = p3d_ViewProjectionMatrix * transformMat * p3d_ModelMatrix * p3d_Vertex;
}