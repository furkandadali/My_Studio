using UnityEditor;

[ InitializeOnLoad ] public class Signer {

  static Signer () {
    PlayerSettings.Android.keystorePass = "VRDev2026";
    PlayerSettings.Android.keyaliasName = "dev";
    PlayerSettings.Android.keyaliasPass = "VRDev2026";
  }

}