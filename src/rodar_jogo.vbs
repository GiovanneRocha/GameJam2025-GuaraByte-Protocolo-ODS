Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")
batPath = objFSO.BuildPath(objFSO.GetParentFolderName(WScript.ScriptFullName), "rodar_jogo.bat")
If objFSO.FileExists(batPath) Then
    objShell.Run Chr(34) & batPath & Chr(34), 0, True
Else
    MsgBox "Arquivo rodar_jogo.bat não encontrado na mesma pasta.", 16, "Erro"
End If
