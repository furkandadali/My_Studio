using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.XR.PXR;

public class MotionObjTracker : MonoBehaviour
{
    public TrackerSN trackerSN { get; set; }
    public string serialNumber { get; set; }

    [SerializeField] private Renderer trackerRenderer;

    private long _trackerId;
    private MotionTrackerLocation _location;
    private bool _confidence;

    private void Awake()
    {
        if (!trackerRenderer)
            trackerRenderer = GetComponentInChildren<Renderer>();
    }

    // Called by MotionTrackerManager after instantiation
    public void Initialize(long trackerId)
    {
        _trackerId = trackerId;
        serialNumber = trackerId.ToString();
        trackerSN = new TrackerSN { value = serialNumber };
        gameObject.name = $"MotionTracker_{trackerId}";
        Debug.Log($"_245 MotionObjTracker initialized — ID: {_trackerId}");
    }

    private void FixedUpdate()
    {
        if (_trackerId == 0) return;
        UpdateTrackingData();
    }

    private void UpdateTrackingData()
    {
        var result = PXR_MotionTracking.GetMotionTrackerLocation(_trackerId, ref _location, ref _confidence);

        if (result != 0 || !_confidence) return;

        transform.localPosition = _location.pose.Position.ToVector3();
        transform.localRotation = _location.pose.Orientation.ToQuat();
    }
}