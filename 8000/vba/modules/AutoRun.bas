Attribute VB_Name = "AutoRun"
Option Explicit

' ========================================
' Auto Run Module - Main Entry Point
' ========================================
' This module contains the main entry point for generating visualization reports
' and the silent import functions used by the main workflow.
' ========================================

' ========================================
' Generate Visualization Report
' Main entry point - Called by Control Panel button
' ========================================
Sub GenerateVisualizationReport()
    On Error GoTo ErrorHandler
    
    Dim quantStatsPath As String
    Dim accuracyLogPath As String
    Dim missingFiles As String
    Dim response As VbMsgBoxResult
    Dim quantWs As Worksheet, accWs As Worksheet
    Dim quantLastRow As Long, accLastRow As Long
    
    ' Build file paths
    quantStatsPath = ThisWorkbook.Path & "\input\quant_stats_e2e.txt"
    accuracyLogPath = ThisWorkbook.Path & "\input\accuracy_log_e2e.txt"
    
    ' Step 1: Check data files exist
    missingFiles = ""
    If Dir(quantStatsPath) = "" Then
        missingFiles = missingFiles & "- quant_stats_e2e.txt" & vbCrLf
    End If
    If Dir(accuracyLogPath) = "" Then
        missingFiles = missingFiles & "- accuracy_log_e2e.txt" & vbCrLf
    End If
    
    ' If files missing, show error and exit
    If missingFiles <> "" Then
        MsgBox "Data files not found!" & vbCrLf & vbCrLf & _
               "Missing files:" & vbCrLf & _
               missingFiles & vbCrLf & _
               "Please ensure files exist in vba\input\ directory", _
               vbExclamation, "Data Files Missing"
        Exit Sub
    End If
    
    ' Step 2: Import data first (with error checking)
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    
    ' Import quantization stats
    On Error Resume Next
    Call AutoImportQuantStatsSilent
    If Err.Number <> 0 Then
        Application.ScreenUpdating = True
        Application.DisplayAlerts = True
        MsgBox "Failed to import quantization statistics: " & Err.Description, vbExclamation, "Import Error"
        Exit Sub
    End If
    Err.Clear
    
    ' Import accuracy log
    On Error Resume Next
    Call AutoImportAccuracyLogSilent
    If Err.Number <> 0 Then
        Application.ScreenUpdating = True
        Application.DisplayAlerts = True
        MsgBox "Failed to import accuracy log: " & Err.Description, vbExclamation, "Import Error"
        Exit Sub
    End If
    Err.Clear
    On Error GoTo ErrorHandler
    
    ' Step 3: Verify data was imported successfully
    On Error Resume Next
    Set quantWs = ThisWorkbook.Worksheets("Quantization Stats")
    Set accWs = ThisWorkbook.Worksheets("Accuracy Log")
    On Error GoTo ErrorHandler
    
    If quantWs Is Nothing Or accWs Is Nothing Then
        Application.ScreenUpdating = True
        Application.DisplayAlerts = True
        MsgBox "Failed to create data worksheets. Please check the file formats.", vbExclamation, "Import Failed"
        Exit Sub
    End If
    
    quantLastRow = quantWs.Cells(quantWs.Rows.Count, 1).End(xlUp).row
    accLastRow = accWs.Cells(accWs.Rows.Count, 1).End(xlUp).row
    
    ' Check if data was actually imported (row 1 is header, so need at least row 2)
    If quantLastRow < 2 Then
        Application.ScreenUpdating = True
        Application.DisplayAlerts = True
        MsgBox "Quantization statistics imported but appears to be empty." & vbCrLf & _
               "Please check the file format of quant_stats_e2e.txt", vbExclamation, "Empty Data"
        Exit Sub
    End If
    
    If accLastRow < 2 Then
        Application.ScreenUpdating = True
        Application.DisplayAlerts = True
        MsgBox "Accuracy log imported but appears to be empty." & vbCrLf & _
               "Please check the file format of accuracy_log_e2e.txt", vbExclamation, "Empty Data"
        Exit Sub
    End If
    
    ' Step 4: Data connected successfully - show welcome message
    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    
    response = MsgBox("Welcome to the INT8 Quantization Analysis Tool!" & vbCrLf & vbCrLf & _
                      "Data connected successfully!" & vbCrLf & vbCrLf & _
                      "This tool will now:" & vbCrLf & _
                      "1. Generate visualization charts" & vbCrLf & _
                      "2. Create a comprehensive analysis report" & vbCrLf & vbCrLf & _
                      "Continue?", _
                      vbYesNo + vbQuestion, "INT8 Quantization Analysis")
    
    If response = vbNo Then
        Exit Sub
    End If
    
    ' Step 5: Generate report (charts are generated inside GenerateReport)
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    
    Call ReportModule.GenerateReport
    
    ' Restore settings
    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    
    ' Activate report sheet
    On Error Resume Next
    ThisWorkbook.Worksheets("Report").Activate
    On Error GoTo 0
    
    Exit Sub
    
ErrorHandler:
    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    MsgBox "Report Generation Failed: " & vbCrLf & Err.Description, vbCritical, "Error"
End Sub

' ========================================
' Silent Import Functions (No Message Boxes)
' ========================================
Sub AutoImportQuantStatsSilent()
    On Error GoTo ErrorHandler
    
    Dim filePath As String
    Dim fileNum As Integer
    Dim lineText As String
    Dim dataArray() As String
    Dim ws As Worksheet
    Dim row As Long
    
    filePath = ThisWorkbook.Path & "\input\quant_stats_e2e.txt"
    
    If Dir(filePath) = "" Then
        Err.Raise vbObjectError + 1, "AutoImportQuantStatsSilent", "File not found: " & filePath
        Exit Sub
    End If
    
    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets("Quantization Stats")
    If ws Is Nothing Then
        Set ws = ThisWorkbook.Worksheets.Add
        ws.Name = "Quantization Stats"
    End If
    If Err.Number <> 0 Then
        Err.Raise vbObjectError + 2, "AutoImportQuantStatsSilent", "Failed to create worksheet: " & Err.Description
    End If
    On Error GoTo ErrorHandler
    
    ws.Cells.Clear
    ws.Cells(1, 1).Value = "Layer Name"
    ws.Cells(1, 2).Value = "Scale Factor"
    ws.Range("A1:B1").Font.Bold = True
    ws.Range("A1:B1").Interior.Color = RGB(68, 114, 196)
    ws.Range("A1:B1").Font.Color = RGB(255, 255, 255)
    
    fileNum = FreeFile
    Open filePath For Input As #fileNum
    
    ' Skip first two lines (header + separator)
    If Not EOF(fileNum) Then Line Input #fileNum, lineText
    If Not EOF(fileNum) Then Line Input #fileNum, lineText
    
    ' Read data
    row = 2
    Do While Not EOF(fileNum)
        Line Input #fileNum, lineText
        lineText = Trim(lineText)
        
        ' Skip empty lines
        If Len(lineText) > 0 Then
            ' Tab separated
            dataArray = Split(lineText, vbTab)
            
            If UBound(dataArray) >= 1 Then
                ws.Cells(row, 1).Value = Trim(dataArray(0))
                ws.Cells(row, 2).Value = CDbl(Trim(dataArray(1)))
                row = row + 1
            End If
        End If
    Loop
    
    Close #fileNum
    
    ws.Columns("A:B").AutoFit
    ws.Range("B2:B" & row - 1).NumberFormat = "0.00000000"
    
    ' Verify data was imported
    If row < 3 Then
        Err.Raise vbObjectError + 3, "AutoImportQuantStatsSilent", "No data rows imported"
    End If
    
    Exit Sub
    
ErrorHandler:
    If fileNum > 0 Then Close #fileNum
    ' Re-raise error so caller can handle it
    If Err.Number <> 0 Then
        Err.Raise Err.Number, Err.Source, Err.Description
    End If
End Sub

Sub AutoImportAccuracyLogSilent()
    On Error GoTo ErrorHandler
    
    Dim filePath As String
    Dim fileNum As Integer
    Dim lineText As String
    Dim dataArray() As String
    Dim ws As Worksheet
    Dim row As Long
    
    filePath = ThisWorkbook.Path & "\input\accuracy_log_e2e.txt"
    
    If Dir(filePath) = "" Then
        Err.Raise vbObjectError + 1, "AutoImportAccuracyLogSilent", "File not found: " & filePath
        Exit Sub
    End If
    
    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets("Accuracy Log")
    If ws Is Nothing Then
        Set ws = ThisWorkbook.Worksheets.Add
        ws.Name = "Accuracy Log"
    End If
    If Err.Number <> 0 Then
        Err.Raise vbObjectError + 2, "AutoImportAccuracyLogSilent", "Failed to create worksheet: " & Err.Description
    End If
    On Error GoTo ErrorHandler
    
    ws.Cells.Clear
    ws.Cells(1, 1).Value = "Sample Index"
    ws.Cells(1, 2).Value = "FP32 Output"
    ws.Cells(1, 3).Value = "INT8 Output"
    ws.Cells(1, 4).Value = "Error"
    ws.Range("A1:D1").Font.Bold = True
    ws.Range("A1:D1").Interior.Color = RGB(68, 114, 196)
    ws.Range("A1:D1").Font.Color = RGB(255, 255, 255)
    
    fileNum = FreeFile
    Open filePath For Input As #fileNum
    
    ' Skip first two lines (header + separator)
    If Not EOF(fileNum) Then Line Input #fileNum, lineText
    If Not EOF(fileNum) Then Line Input #fileNum, lineText
    
    ' Read data
    row = 2
    Do While Not EOF(fileNum)
        Line Input #fileNum, lineText
        lineText = Trim(lineText)
        
        ' Skip empty lines
        If Len(lineText) > 0 Then
            ' Tab separated
            dataArray = Split(lineText, vbTab)
            
            If UBound(dataArray) >= 3 Then
                ws.Cells(row, 1).Value = CLng(Trim(dataArray(0)))
                ws.Cells(row, 2).Value = CDbl(Trim(dataArray(1)))
                ws.Cells(row, 3).Value = CDbl(Trim(dataArray(2)))
                ws.Cells(row, 4).Value = CDbl(Trim(dataArray(3)))
                row = row + 1
            End If
        End If
    Loop
    
    Close #fileNum
    
    ws.Columns("A:D").AutoFit
    ws.Range("B2:D" & row - 1).NumberFormat = "0.000000"
    
    ' Verify data was imported
    If row < 3 Then
        Err.Raise vbObjectError + 3, "AutoImportAccuracyLogSilent", "No data rows imported"
    End If
    
    Exit Sub
    
ErrorHandler:
    If fileNum > 0 Then Close #fileNum
    ' Re-raise error so caller can handle it
    If Err.Number <> 0 Then
        Err.Raise Err.Number, Err.Source, Err.Description
    End If
End Sub

