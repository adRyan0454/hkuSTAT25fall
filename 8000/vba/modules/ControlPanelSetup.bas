Attribute VB_Name = "ControlPanelSetup"
Option Explicit

' ========================================
' Control Panel Setup Module
' ========================================

' ========================================
' Initialize Control Panel
' ========================================
Sub InitializeControlPanel()
    On Error GoTo ErrorHandler
    
    Dim ws As Worksheet
    Dim btn As Button
    Dim row As Long
    
    ' Create or get control panel sheet
    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets("Control Panel")
    If ws Is Nothing Then
        Set ws = ThisWorkbook.Worksheets.Add(Before:=ThisWorkbook.Worksheets(1))
        ws.Name = "Control Panel"
    End If
    On Error GoTo ErrorHandler
    
    ' Clear existing content
    ws.Cells.Clear
    ws.Buttons.Delete
    
    ' Title
    row = 3
    ws.Cells(row, 2).Value = "INT8 Quantization Visualization & Analysis Tool"
    ws.Cells(row, 2).Font.Size = 18
    ws.Cells(row, 2).Font.Bold = True
    ws.Cells(row, 2).Font.Color = RGB(68, 114, 196)
    row = row + 4
    
    ' Single main button
    Set btn = ws.Buttons.Add(ws.Cells(row, 2).Left, ws.Cells(row, 2).Top, 300, 50)
    btn.OnAction = "GenerateVisualizationReport"
    btn.Text = "Generate Visualization Report"
    btn.Font.Size = 14
    btn.Font.Bold = True
    btn.Characters.Font.Color = RGB(255, 255, 255)
    btn.ShapeRange.Fill.ForeColor.RGB = RGB(68, 114, 196)
    row = row + 6
    
    ' Input path info
    ws.Cells(row, 2).Value = "Data Path:"
    ws.Cells(row, 2).Font.Size = 10
    ws.Cells(row, 3).Value = "vba\input\"
    ws.Cells(row, 3).Font.Size = 10
    ws.Cells(row, 3).Interior.Color = RGB(255, 255, 200)
    row = row + 2
    
    ' Simple instruction
    ws.Cells(row, 2).Value = "Please ensure the following files exist in vba\input\ directory:"
    ws.Cells(row, 2).Font.Size = 9
    ws.Cells(row, 2).Font.Italic = True
    row = row + 1
    ws.Cells(row, 2).Value = "- quant_stats_e2e.txt"
    ws.Cells(row, 2).Font.Size = 9
    row = row + 1
    ws.Cells(row, 2).Value = "- accuracy_log_e2e.txt"
    ws.Cells(row, 2).Font.Size = 9
    
    ' Format
    ws.Columns("A:E").AutoFit
    ws.Columns("B").ColumnWidth = 35
    ws.Columns("C").ColumnWidth = 40
    
    ' Activate control panel
    ws.Activate
    ws.Range("B3").Select
    
    Exit Sub
    
ErrorHandler:
    MsgBox "Initialization failed: " & Err.Description, vbCritical, "Error"
End Sub
