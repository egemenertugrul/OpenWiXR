using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using OpenWiXR.Communications;
using static OpenWiXR.Communications.WebSocketsClient;
using Newtonsoft.Json.Linq;

namespace OpenWiXR.Tracking
{
    public sealed class SLAMPoseDriver : PoseDriver
    {
        private ORBSLAM3 SLAM;
        private void Start()
        {
            SLAM = GetComponent<ORBSLAM3>();
            if (!SLAM)
            {
                throw new NullReferenceException("SLAM is required for the SLAMPoseDriver.");
            }

            SLAM.OnPoseUpdated.AddListener(SLAMPoseHandler);
        }

        private void SLAMPoseHandler(Vector3 translation, Quaternion rotation)
        {
            UpdatePositionAndRotation(translation, rotation);
        }
    }
}