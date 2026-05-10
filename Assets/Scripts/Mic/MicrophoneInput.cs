using UnityEngine;

[RequireComponent(typeof(AudioSource))]
public class MicrophoneInput : MonoBehaviour
{
    [Header("Microphone Settings")]
    public int microphoneIndex = 0;
    public int frequency = 44100;
    public bool startOnAwake = true;

    private AudioSource audioSource;
    private string microphoneName;

    void Awake()
    {
        audioSource = GetComponent<AudioSource>();
    }

    void Start()
    {
        if (Microphone.devices.Length == 0)
        {
            Debug.LogError("No microphone found!");
            return;
        }

        // Log all available microphones
        Debug.Log($"Found {Microphone.devices.Length} microphone(s):");
        for (int i = 0; i < Microphone.devices.Length; i++)
        {
            Debug.Log($"  [{i}] {Microphone.devices[i]}");
        }

        microphoneName = Microphone.devices[microphoneIndex];
        Debug.Log($"Using microphone: {microphoneName}");

        if (startOnAwake)
            StartMicrophone();
    }

    public void StartMicrophone()
    {
        if (Microphone.IsRecording(microphoneName))
        {
            Debug.LogWarning("Microphone already recording.");
            return;
        }

        audioSource.clip = Microphone.Start(microphoneName, true, 1, frequency);
        audioSource.loop = true;

        // Wait until microphone starts before playing
        while (!(Microphone.GetPosition(microphoneName) > 0)) { }

        audioSource.Play();
        Debug.Log("Microphone started successfully.");
    }

    public void StopMicrophone()
    {
        Microphone.End(microphoneName);
        audioSource.Stop();
        Debug.Log("Microphone stopped.");
    }

    void OnDestroy()
    {
        StopMicrophone();
    }
}