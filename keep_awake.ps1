$code = @'
using System;
using System.Runtime.InteropServices;

public class KeepAwake {
    [Flags]
    public enum EXECUTION_STATE : uint {
        ES_AWAYMODE_REQUIRED = 0x00000040,
        ES_CONTINUOUS = 0x80000000,
        ES_DISPLAY_REQUIRED = 0x00000002,
        ES_SYSTEM_REQUIRED = 0x00000001
    }

    [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    private static extern EXECUTION_STATE SetThreadExecutionState(EXECUTION_STATE esFlags);

    public static void PreventSleep() {
        // ES_CONTINUOUS | ES_SYSTEM_REQUIRED
        SetThreadExecutionState(EXECUTION_STATE.ES_CONTINUOUS | EXECUTION_STATE.ES_SYSTEM_REQUIRED);
    }
}
'@
Add-Type -TypeDefinition $code
[KeepAwake]::PreventSleep()
Write-Host "Da kich hoat che do chong ngu (System Required). Tien trinh cua anh se tiep tuc chay."
