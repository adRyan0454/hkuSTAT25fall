Attribute VB_Name = "MainModule"
Option Explicit

' ============================================================================
' Global constants
' ============================================================================
Const OUTPUT_PATH As String = "vba\input\"
Const QUANT_STATS_FILE As String = "quant_stats_e2e.txt"
Const ACCURACY_LOG_FILE As String = "accuracy_log_e2e.txt"
Const CPP_EXE_PATH As String = "..\cplus\build\bin\Release\inference_engine.exe"

' ============================================================================
' Sub: ImportQuantStats
' Desc: Import quantization statistics file (quant_stats_e2e.txt)
' ============================================================================
Sub ImportQuantStats()
    On Error GoTo ErrorHandler
    
    Dim filePath As String
    Dim fileNum As Integer
    Dim lineText As String
    Dim dataArray() As String
    Dim ws As Worksheet
    Dim rowNum As Long
    
    ' Get or create worksheet
    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets("Quantization Stats")
    If ws Is Nothing Then
        Set ws = ThisWorkbook.Worksheets.Add
        ws.Name = "Quantization Stats"
    End If
    On Error GoTo ErrorHandler
    
    ' Clear existing data
    ws.Cells.Clear
    
    ' Header
    ws.Range("A1").Value = "Layer Name"
    ws.Range("B1").Value = "Scale Factor"
    ws.Range("A1:B1").Font.Bold = True
    ws.Range("A1:B1").Interior.Color = RGB(68, 114, 196)
    ws.Range("A1:B1").Font.Color = RGB(255, 255, 255)
    
    ' Build file path
    filePath = ThisWorkbook.Path & "\" & OUTPUT_PATH & QUANT_STATS_FILE
    
    ' Check file exists
    If Dir(filePath) = "" Then
        MsgBox "File not found: " & filePath, vbExclamation, "File Not Found"
        Exit Sub
    End If
    
    ' Open file
    fileNum = FreeFile
    Open filePath For Input As #fileNum
    
    ' Skip first two lines (header + separator)
    If Not EOF(fileNum) Then Line Input #fileNum, lineText
    If Not EOF(fileNum) Then Line Input #fileNum, lineText
    
    ' Read data
    rowNum = 2
    Do While Not EOF(fileNum)
        Line Input #fileNum, lineText
        lineText = Trim(lineText)
        
        ' Skip empty lines
        If Len(lineText) > 0 Then
            ' Tab separated
            dataArray = Split(lineText, vbTab)
            
            If UBound(dataArray) >= 1 Then
                ws.Cells(rowNum, 1).Value = Trim(dataArray(0))
                ws.Cells(rowNum, 2).Value = CDbl(Trim(dataArray(1)))
                rowNum = rowNum + 1
            End If
        End If
    Loop
    
    Close #fileNum
    
    ' Format data
    ws.Columns("A:B").AutoFit
    ws.Range("B2:B" & rowNum - 1).NumberFormat = "0.00000000"
    
    ' Add border
    With ws.Range("A1:B" & rowNum - 1)
        .Borders.LineStyle = xlContinuous
        .Borders.Weight = xlThin
    End With
    
    MsgBox "Successfully imported " & rowNum - 2 & " layers of quantization statistics.", vbInformation, "Import Complete"
    
    Exit Sub
    
ErrorHandler:
    If fileNum > 0 Then Close #fileNum
    MsgBox "Error while importing quantization statistics: " & Err.Description, vbCritical, "Error"
End Sub

' ============================================================================
' Sub: ImportAccuracyLog
' Desc: Import accuracy log file (accuracy_log_e2e.txt)
' ============================================================================
Sub ImportAccuracyLog()
    On Error GoTo ErrorHandler
    
    Dim filePath As String
    Dim fileNum As Integer
    Dim lineText As String
    Dim dataArray() As String
    Dim ws As Worksheet
    Dim rowNum As Long
    
    ' Get or create worksheet
    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets("Accuracy Log")
    If ws Is Nothing Then
        Set ws = ThisWorkbook.Worksheets.Add
        ws.Name = "Accuracy Log"
    End If
    On Error GoTo ErrorHandler
    
    ' Clear existing data
    ws.Cells.Clear
    
    ' Header
    ws.Range("A1").Value = "Sample Index"
    ws.Range("B1").Value = "FP32 Output"
    ws.Range("C1").Value = "INT8 Output"
    ws.Range("D1").Value = "Error"
    ws.Range("A1:D1").Font.Bold = True
    ws.Range("A1:D1").Interior.Color = RGB(68, 114, 196)
    ws.Range("A1:D1").Font.Color = RGB(255, 255, 255)
    
    ' Build file path
    filePath = ThisWorkbook.Path & "\" & OUTPUT_PATH & ACCURACY_LOG_FILE
    
    ' Check file exists
    If Dir(filePath) = "" Then
        MsgBox "File not found: " & filePath, vbExclamation, "File Not Found"
        Exit Sub
    End If
    
    ' Open file
    fileNum = FreeFile
    Open filePath For Input As #fileNum
    
    ' Skip first two lines (header + separator)
    If Not EOF(fileNum) Then Line Input #fileNum, lineText
    If Not EOF(fileNum) Then Line Input #fileNum, lineText
    
    ' Read data
    rowNum = 2
    Do While Not EOF(fileNum)
        Line Input #fileNum, lineText
        lineText = Trim(lineText)
        
        ' Skip empty lines
        If Len(lineText) > 0 Then
            ' Tab separated
            dataArray = Split(lineText, vbTab)
            
            If UBound(dataArray) >= 3 Then
                ws.Cells(rowNum, 1).Value = CLng(Trim(dataArray(0)))
                ws.Cells(rowNum, 2).Value = CDbl(Trim(dataArray(1)))
                ws.Cells(rowNum, 3).Value = CDbl(Trim(dataArray(2)))
                ws.Cells(rowNum, 4).Value = CDbl(Trim(dataArray(3)))
                rowNum = rowNum + 1
            End If
        End If
    Loop
    
    Close #fileNum
    
    ' Format data
    ws.Columns("A:D").AutoFit
    ws.Range("B2:D" & rowNum - 1).NumberFormat = "0.000000"
    
    ' Add border
    With ws.Range("A1:D" & rowNum - 1)
        .Borders.LineStyle = xlContinuous
        .Borders.Weight = xlThin
    End With
    
    MsgBox "Successfully imported " & rowNum - 2 & " accuracy samples.", vbInformation, "Import Complete"
    
    Exit Sub
    
ErrorHandler:
    If fileNum > 0 Then Close #fileNum
    MsgBox "Error while importing accuracy log: " & Err.Description, vbCritical, "Error"
End Sub

' ============================================================================
' Sub: RunCppInference
' Desc: Run C++ inference engine
' ============================================================================
Sub RunCppInference()
    On Error GoTo ErrorHandler
    
    Dim exePath As String
    Dim result As Long
    
    ' Build executable path
    exePath = ThisWorkbook.Path & "\" & CPP_EXE_PATH
    
    ' Check file exists
    If Dir(exePath) = "" Then
        MsgBox "C++ executable not found: " & exePath, vbExclamation, "File Not Found"
        Exit Sub
    End If
    
    ' Confirm with user
    If MsgBox("The C++ inference engine will be executed. This may take a few seconds." & vbCrLf & vbCrLf & _
              "Continue?", vbQuestion + vbYesNo, "Confirm Run") = vbNo Then
        Exit Sub
    End If
    
    ' Run process
    result = Shell(exePath, vbNormalFocus)
    
    ' Wait for user to confirm completion
    MsgBox "C++ program has been started." & vbCrLf & vbCrLf & _
           "Please wait for it to finish, then click OK to continue.", vbInformation, "Running"
    
    MsgBox "C++ inference engine execution finished." & vbCrLf & vbCrLf & _
           "You can now import the generated data files.", vbInformation, "Complete"
    
    Exit Sub
    
ErrorHandler:
    MsgBox "Error while running C++ program: " & Err.Description, vbCritical, "Error"
End Sub

' ============================================================================
' Sub: CompleteWorkflow
' Desc: One-click full workflow
' ============================================================================
Sub CompleteWorkflow()
    On Error GoTo ErrorHandler
    
    Dim startTime As Double
    startTime = Timer
    
    ' Confirm with user
    If MsgBox("The following steps will be executed:" & vbCrLf & vbCrLf & _
              "1. Import quantization statistics" & vbCrLf & _
              "2. Import accuracy log" & vbCrLf & _
              "3. Generate charts" & vbCrLf & _
              "4. Generate report" & vbCrLf & vbCrLf & _
              "Please make sure the required input files are in 'vba/input' directory." & vbCrLf & _
              "(quant_stats_e2e.txt and accuracy_log_e2e.txt)" & vbCrLf & vbCrLf & _
              "Continue?", vbQuestion + vbYesNo, "Confirm Workflow") = vbNo Then
        Exit Sub
    End If
    
    ' Step 1: Import quantization stats
    Application.StatusBar = "Step 1/4: Importing quantization stats..."
    ImportQuantStats
    
    ' Step 2: Import accuracy log
    Application.StatusBar = "Step 2/4: Importing accuracy log..."
    ImportAccuracyLog
    
    ' Step 3: Generate charts
    Application.StatusBar = "Step 3/4: Generating charts..."
    ChartModule.GenerateAllCharts
    
    ' Step 4: Generate report
    Application.StatusBar = "Step 4/4: Generating report..."
    ReportModule.GenerateReport
    
    ' Done
    Application.StatusBar = False
    
    Dim elapsedTime As Double
    elapsedTime = Timer - startTime
    
    MsgBox "Full workflow completed successfully." & vbCrLf & vbCrLf & _
           "Elapsed time: " & Format(elapsedTime, "0.0") & " seconds", vbInformation, "Complete"
    
    Exit Sub
    
ErrorHandler:
    Application.StatusBar = False
    MsgBox "Error while executing full workflow: " & Err.Description, vbCritical, "Error"
End Sub
