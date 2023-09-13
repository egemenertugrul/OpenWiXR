﻿namespace OpenWiXR
{
    using UnityEditor;
    using UnityEngine;

    public static class EditorUtilities
    {
        public static void HideField(SerializedObject serializedObject, string fieldName)
        {
            SerializedProperty prop = serializedObject.FindProperty(fieldName);
            if (prop != null)
            {
                EditorGUI.BeginChangeCheck();
                EditorGUILayout.PropertyField(prop, true);
                if (EditorGUI.EndChangeCheck())
                {
                    serializedObject.ApplyModifiedProperties();
                }
            }
        }
        
        public static void DisableField(SerializedObject serializedObject, string fieldName)
        {
            SerializedProperty prop = serializedObject.FindProperty(fieldName);
            if (prop != null)
            {
                EditorGUI.BeginChangeCheck();
                EditorGUI.BeginDisabledGroup(true); // Start disabling the field
                EditorGUILayout.PropertyField(prop, true);
                EditorGUI.EndDisabledGroup(); // End disabling the field
                if (EditorGUI.EndChangeCheck())
                {
                    serializedObject.ApplyModifiedProperties();
                }
            }
        }
        public static void PropertyField(SerializedObject serializedObject, string fieldName)
        {
            SerializedProperty prop = serializedObject.FindProperty(fieldName);
            EditorGUILayout.PropertyField(prop, true);
        }

        public static void DrawUILine(Color color, int thickness = 2, int padding = 10)
        {
            Rect r = EditorGUILayout.GetControlRect(GUILayout.Height(padding + thickness));
            r.height = thickness;
            r.y += padding / 2;
            r.x -= 2;
            r.width += 6;
            EditorGUI.DrawRect(r, color);
        }

    }

}