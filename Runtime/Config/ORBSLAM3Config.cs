using OpenWiXR.Tracking;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using static OpenWiXR.Tracking.ORBSLAM3;

namespace OpenWiXR
{
    [CreateAssetMenu(fileName = "ORBSLAM3Config", menuName = "OpenWiXR/Create ORBSLAM3 Configuration", order = 1)]
    public class ORBSLAM3Config : ScriptableObject
    {
        public int FPS = 60;
        public TextAsset TimestampsFile, IMUFile;
        public string BaseImagePath;
        public string VocabularyPath, SettingsPath; // Relative to StreamingAssets path
        public Source_Type SourceType = Source_Type.Realtime;
        public Sensor_Type SensorType = Sensor_Type.IMU_MONOCULAR;
        public bool DisplayMapPoints = false;
    }
}