using UnityEngine;

[RequireComponent(typeof(AudioSource))]
public class CustomLipSync : MonoBehaviour
{
    [Header("Skinned Mesh Renderer")]
    public SkinnedMeshRenderer headMesh;

    [Header("Blendshape Indices")]
    public int jawOpenIndex = 49;
    public int mouthFunnelIndex = 26;
    public int mouthOpenIndex = 0;
    public int mouthCloseIndex = 23;

    [Header("Sensitivity")]
    [Range(0.001f, 0.1f)]
    public float sensitivity = 0.02f;

    [Header("Smoothing")]
    [Range(0.01f, 1f)]
    public float smoothSpeed = 0.1f;

    [Header("Blendshape Multiplier")]
    [Range(1f, 200f)]
    public float multiplier = 150f;

    [Header("Threshold")]
    [Range(0f, 0.1f)]
    public float silenceThreshold = 0.005f;

    // Private
    private AudioSource audioSource;
    private float[] samples = new float[1024];
    private float currentAmplitude = 0f;
    private float smoothAmplitude = 0f;
    private float previousAmplitude = 0f;

    void Awake()
    {
        audioSource = GetComponent<AudioSource>();
    }

    void Start()
    {
        if (headMesh == null)
        {
            Debug.LogError("CustomLipSync: Head mesh not assigned!");
            return;
        }

        Debug.Log("CustomLipSync initialized successfully.");
    }

    void Update()
    {
        if (audioSource == null || headMesh == null) return;

        AnalyzeAudio();
        ApplyToBlendshapes();
    }

    void AnalyzeAudio()
    {
        // Get raw audio samples from AudioSource
        audioSource.GetOutputData(samples, 0);

        // Calculate RMS (Root Mean Square) amplitude
        float sum = 0f;
        for (int i = 0; i < samples.Length; i++)
        {
            sum += samples[i] * samples[i];
        }

        currentAmplitude = Mathf.Sqrt(sum / samples.Length);

        // Apply silence threshold
        if (currentAmplitude < silenceThreshold)
            currentAmplitude = 0f;

        // Smooth the amplitude to avoid jittery movement
        smoothAmplitude = Mathf.Lerp(smoothAmplitude, currentAmplitude, smoothSpeed);

        previousAmplitude = smoothAmplitude;
    }

    void ApplyToBlendshapes()
    {
        // Convert amplitude to blendshape weight (0-100)
        float weight = Mathf.Clamp(smoothAmplitude * multiplier, 0f, 100f);

        // Apply jaw open — primary mouth movement
        headMesh.SetBlendShapeWeight(jawOpenIndex, weight);

        // Apply mouth open — secondary
        headMesh.SetBlendShapeWeight(mouthOpenIndex, weight * 0.6f);

        // Apply mouth funnel at mid range volumes (like O sound)
        float funnelWeight = Mathf.Clamp((weight - 20f) * 0.5f, 0f, 60f);
        headMesh.SetBlendShapeWeight(mouthFunnelIndex, funnelWeight);

        // Close mouth when silent
        float closeWeight = Mathf.Clamp(100f - (weight * 2f), 0f, 100f);
        headMesh.SetBlendShapeWeight(mouthCloseIndex, closeWeight * 0.3f);
    }

    // Public method to get current amplitude (useful for networking later)
    public float GetCurrentAmplitude()
    {
        return smoothAmplitude;
    }

    // Public method to manually feed amplitude (useful for remote players)
    public void SetAmplitude(float amplitude)
    {
        smoothAmplitude = amplitude;
        ApplyToBlendshapes();
    }

    void OnDestroy()
    {
        // Reset all blendshapes on destroy
        if (headMesh != null)
        {
            headMesh.SetBlendShapeWeight(jawOpenIndex, 0f);
            headMesh.SetBlendShapeWeight(mouthOpenIndex, 0f);
            headMesh.SetBlendShapeWeight(mouthFunnelIndex, 0f);
            headMesh.SetBlendShapeWeight(mouthCloseIndex, 0f);
        }
    }
}