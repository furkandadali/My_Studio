using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.XR.PXR;

public class MotionTrackerManager : MonoBehaviour
{
    [Header("Prefab")]
    [SerializeField] private MotionObjTracker trackerPrefab;

    [Header("Parent for instantiated trackers (optional)")]
    [SerializeField] private Transform trackerParent;

    private bool _trackingReady = false;
    private List<long> _connectedTrackerIds = new List<long>();
    private Dictionary<long, MotionObjTracker> _trackerObjects = new Dictionary<long, MotionObjTracker>();
    private Coroutine _pollingCoroutine;

    private void OnEnable()
    {
        PXR_MotionTracking.RequestMotionTrackerCompleteAction += OnMotionTrackerComplete;
        PXR_MotionTracking.MotionTrackerConnectionAction += OnTrackerConnectionChanged;
    }

    private void OnDisable()
    {
        PXR_MotionTracking.RequestMotionTrackerCompleteAction -= OnMotionTrackerComplete;
        PXR_MotionTracking.MotionTrackerConnectionAction -= OnTrackerConnectionChanged;
        if (_pollingCoroutine != null) StopCoroutine(_pollingCoroutine);
    }

    private void Start()
    {
        if (trackerPrefab == null)
            Debug.LogError("_245 trackerPrefab is not assigned in MotionTrackerManager!");
    }

    // Fires on every connect/disconnect with full updated tracker list
    private void OnMotionTrackerComplete(RequestMotionTrackerCompleteEventData eventData)
    {
        Debug.Log($"_245 RequestMotionTrackerCompleteAction — count:{eventData.trackerCount} result:{eventData.result}");

        if (eventData.trackerIds == null)
        {
            Debug.LogWarning("_245 No tracker IDs in event.");
            return;
        }

        // Build new ID set from event
        var newIds = new HashSet<long>(eventData.trackerIds);
        var currentIds = new HashSet<long>(_connectedTrackerIds);

        // Destroy prefabs for trackers that disconnected
        foreach (var id in currentIds)
        {
            if (!newIds.Contains(id))
            {
                Debug.Log($"_245 Tracker {id} removed — destroying prefab.");
                DestroyTrackerObject(id);
            }
        }

        // Instantiate prefabs for newly connected trackers
        foreach (var id in newIds)
        {
            if (!currentIds.Contains(id))
            {
                Debug.Log($"_245 Tracker {id} added — instantiating prefab.");
                SpawnTrackerObject(id);
            }
        }

        // Update connected list
        _connectedTrackerIds = new List<long>(newIds);
        _trackingReady = _connectedTrackerIds.Count > 0;

        Debug.Log($"_245 Active trackers: {_connectedTrackerIds.Count}");
    }

    private void SpawnTrackerObject(long trackerId)
    {
        if (trackerPrefab == null)
        {
            Debug.LogError("_245 Cannot spawn — trackerPrefab not assigned.");
            return;
        }

        if (_trackerObjects.ContainsKey(trackerId))
        {
            Debug.LogWarning($"_245 Tracker {trackerId} prefab already exists, skipping.");
            return;
        }

        var instance = Instantiate(
            trackerPrefab,
            Vector3.zero,
            Quaternion.identity,
            trackerParent
        );

        // Set the serial number on the MotionObjTracker component
        instance.serialNumber = trackerId.ToString();
        instance.trackerSN = new TrackerSN { value = trackerId.ToString() };
        instance.gameObject.name = $"MotionTracker_{trackerId}";

        _trackerObjects[trackerId] = instance;

        Debug.Log($"_245 Spawned prefab for tracker {trackerId}");
    }

    private void DestroyTrackerObject(long trackerId)
    {
        if (_trackerObjects.TryGetValue(trackerId, out var obj))
        {
            if (obj != null) Destroy(obj.gameObject);
            _trackerObjects.Remove(trackerId);
            Debug.Log($"_245 Destroyed prefab for tracker {trackerId}");
        }

        _connectedTrackerIds.Remove(trackerId);
    }

    // Just for logging — Complete handles all SN management
    private void OnTrackerConnectionChanged(long trackerID, int state)
    {
        Debug.Log($"_245 MotionTrackerConnectionAction — ID:{trackerID} State:{(state == 1 ? "connected" : "disconnected")}");
    }
}