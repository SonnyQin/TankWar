// Request GLSL 3.3
#version 330

// Create a struct for directional light
struct DirectionalLight
{
    vec3 mPosition;
	// Direction of light
	vec3 mDirection;
	// Diffuse color
	vec3 mDiffuseColor;
	// Specular color
	vec3 mSpecColor;
};

struct SpotLight
{
    vec3 mPosition;
	// Direction of light
	vec3 mDirection;

    // Diffuse color
	vec3 mDiffuseColor;
	// Specular color
	vec3 mSpecColor;

    float mInnerCutOff;

    float mOuterCutOff;
};

// Inputs from vertex shader
// Tex coord
in vec2 fragTexCoord;
// Normal (in world space)
in vec3 fragNormal;
// Position (in world space)
in vec3 fragWorldPos;

// This corresponds to the output color to the color buffer
out vec4 outColor;

// This is used for the texture sampling
uniform sampler2D uTexture;

// Uniforms for lighting
// Camera position (in world space)
uniform vec3 uCameraPos;
// Specular power for this surface
uniform float uSpecPower;
// Ambient light level
uniform vec3 uAmbientLight;

//Metalic [0, 1]
uniform float uMetallic;


// Directional Light
uniform DirectionalLight uDirLight;

vec3 CalculateDirectionalLight(vec3 N, vec3 L, vec3 V, vec3 H, DirectionalLight dirLight)
{
	vec3 Phong = vec3(0.0,0.0,0.0);
	float NdotL = dot(N, L);
    if(NdotL<0)
    {
        NdotL=-NdotL;
    }
	if (NdotL > 0)
	{
		vec3 Diffuse = (1.0-uMetallic)*dirLight.mDiffuseColor * NdotL;
		vec3 Specular = uMetallic*dirLight.mSpecColor * pow(max(0.0, dot(H, N)), uSpecPower);
		Phong += Diffuse + Specular;
	}
    return Phong;
}

void main()
{
	// Surface normal
	vec3 N = normalize(fragNormal);
	// Vector from surface to light
	vec3 L = normalize(-uDirLight.mDirection);
	// Vector from surface to camera
	vec3 V = normalize(uCameraPos - fragWorldPos);

    vec3 H=normalize(L+V);

    vec3 Phong=uAmbientLight;

    Phong+=CalculateDirectionalLight(N, L, V, H, uDirLight);

	// Final color is texture color times phong light (alpha = 1)
    outColor = texture(uTexture, fragTexCoord) * vec4(Phong, 1.0f);
}