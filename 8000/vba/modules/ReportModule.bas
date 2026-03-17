Attribute VB_Name = "ReportModule"
Option Explicit

' ========================================
' Report Generation Module
' ========================================

' ========================================
' 1. Generate Complete Report
' ========================================
Sub GenerateReport()
    On Error GoTo ErrorHandler
    
    Dim ws As Worksheet
    Dim quantWs As Worksheet, accWs As Worksheet
    Dim row As Long
    Dim lastRow As Long
    
    ' Check data sheets
    On Error Resume Next
    Set quantWs = ThisWorkbook.Worksheets("Quantization Stats")
    Set accWs = ThisWorkbook.Worksheets("Accuracy Log")
    On Error GoTo ErrorHandler
    
    If quantWs Is Nothing Or accWs Is Nothing Then
        MsgBox "Please import quantization statistics and accuracy log data first!", vbExclamation, "No Data"
        Exit Sub
    End If
    
    ' Prepare report sheet
    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets("Report")
    If ws Is Nothing Then
        Set ws = ThisWorkbook.Worksheets.Add
        ws.Name = "Report"
    End If
    On Error GoTo ErrorHandler
    
    ' Clear existing content
    ws.Cells.Clear
    
    ' Title
    row = 1
    ws.Cells(row, 1).Value = "TinyStories-1M INT8 Quantization Analysis Report"
    ws.Cells(row, 1).Font.Size = 16
    ws.Cells(row, 1).Font.Bold = True
    ws.Cells(row, 1).Font.Color = RGB(68, 114, 196)
    row = row + 1
    
    ' Generation date
    ws.Cells(row, 1).Value = "Generated at: " & Format(Now, "yyyy-mm-dd hh:mm:ss")
    ws.Cells(row, 1).Font.Size = 10
    row = row + 2
    
    ' Part 1: Quantization Statistics
    ws.Cells(row, 1).Value = "1. Quantization Statistics"
    ws.Cells(row, 1).Font.Size = 12
    ws.Cells(row, 1).Font.Bold = True
    ws.Cells(row, 1).Interior.Color = RGB(217, 225, 242)
    row = row + 1
    
    ' Calculate scale factor statistics
    lastRow = quantWs.Cells(quantWs.Rows.Count, 1).End(xlUp).row
    If lastRow < 2 Then
        MsgBox "Quantization statistics are empty. Please import data first!", vbExclamation, "No Data"
        Exit Sub
    End If
    
    Dim scaleRange As Range
    Set scaleRange = quantWs.Range("B2:B" & lastRow)
    
    ' Avoid WorksheetFunction errors on empty/non-numeric ranges
    If Application.WorksheetFunction.Count(scaleRange) = 0 Then
        MsgBox "No numeric data found in quantization stats. Please check the imported file format.", vbExclamation, "No Numeric Data"
        Exit Sub
    End If
    
    Dim avgScale As Double, minScale As Double, maxScale As Double, stdScale As Double
    avgScale = Application.WorksheetFunction.Average(scaleRange)
    minScale = Application.WorksheetFunction.Min(scaleRange)
    maxScale = Application.WorksheetFunction.Max(scaleRange)
    stdScale = Application.WorksheetFunction.StDev(scaleRange)
    
    ws.Cells(row, 1).Value = "Number of Layers:"
    ws.Cells(row, 2).Value = lastRow - 1
    row = row + 1
    
    ws.Cells(row, 1).Value = "Average Scale Factor:"
    ws.Cells(row, 2).Value = Format(avgScale, "0.00000000")
    row = row + 1
    
    ws.Cells(row, 1).Value = "Minimum Scale Factor:"
    ws.Cells(row, 2).Value = Format(minScale, "0.00000000")
    row = row + 1
    
    ws.Cells(row, 1).Value = "Maximum Scale Factor:"
    ws.Cells(row, 2).Value = Format(maxScale, "0.00000000")
    row = row + 1
    
    ws.Cells(row, 1).Value = "Standard Deviation:"
    ws.Cells(row, 2).Value = Format(stdScale, "0.00000000")
    row = row + 2
    
    ' Part 2: Accuracy Analysis
    ws.Cells(row, 1).Value = "2. Accuracy Analysis"
    ws.Cells(row, 1).Font.Size = 12
    ws.Cells(row, 1).Font.Bold = True
    ws.Cells(row, 1).Interior.Color = RGB(217, 225, 242)
    row = row + 1
    
    ' Calculate accuracy metrics
    lastRow = accWs.Cells(accWs.Rows.Count, 1).End(xlUp).row
    Dim errorRange As Range
    Set errorRange = accWs.Range("D2:D" & lastRow)
    
    Dim mse As Double, mae As Double, maxError As Double
    Dim i As Long, sumSqError As Double, sumAbsError As Double
    
    sumSqError = 0
    sumAbsError = 0
    maxError = 0
    
    For i = 2 To lastRow
        Dim errVal As Double
        errVal = accWs.Cells(i, 4).Value
        sumSqError = sumSqError + errVal * errVal
        sumAbsError = sumAbsError + Abs(errVal)
        If Abs(errVal) > maxError Then maxError = Abs(errVal)
    Next i
    
    mse = sumSqError / (lastRow - 1)
    mae = sumAbsError / (lastRow - 1)
    
    ws.Cells(row, 1).Value = "Number of Samples:"
    ws.Cells(row, 2).Value = lastRow - 1
    row = row + 1
    
    ws.Cells(row, 1).Value = "MSE (Mean Squared Error):"
    ws.Cells(row, 2).Value = Format(mse, "0.00E+00")
    ws.Cells(row, 3).Value = IIf(mse < 0.0001, "Excellent", IIf(mse < 0.001, "Good", "Needs Improvement"))
    row = row + 1
    
    ws.Cells(row, 1).Value = "MAE (Mean Absolute Error):"
    ws.Cells(row, 2).Value = Format(mae, "0.000000")
    ws.Cells(row, 3).Value = IIf(mae < 0.001, "Excellent", IIf(mae < 0.01, "Good", "Needs Improvement"))
    row = row + 1
    
    ws.Cells(row, 1).Value = "Max Error:"
    ws.Cells(row, 2).Value = Format(maxError, "0.000000")
    ws.Cells(row, 3).Value = IIf(maxError < 0.01, "Excellent", IIf(maxError < 0.1, "Good", "Needs Improvement"))
    row = row + 2
    
    ' Part 3: Performance Metrics
    ws.Cells(row, 1).Value = "3. Performance Metrics"
    ws.Cells(row, 1).Font.Size = 12
    ws.Cells(row, 1).Font.Bold = True
    ws.Cells(row, 1).Interior.Color = RGB(217, 225, 242)
    row = row + 1
    
    ' Data from SUCCESS_REPORT
    ws.Cells(row, 1).Value = "FP32 Inference Time:"
    ws.Cells(row, 2).Value = "0.04 ms"
    row = row + 1
    
    ws.Cells(row, 1).Value = "INT8 Inference Time:"
    ws.Cells(row, 2).Value = "0.03 ms"
    row = row + 1
    
    ws.Cells(row, 1).Value = "Speedup:"
    ws.Cells(row, 2).Value = "1.45x"
    ws.Cells(row, 3).Value = "Improved"
    row = row + 1
    
    ws.Cells(row, 1).Value = "FP32 Model Size:"
    ws.Cells(row, 2).Value = "264 KB"
    row = row + 1
    
    ws.Cells(row, 1).Value = "INT8 Model Size:"
    ws.Cells(row, 2).Value = "68 KB"
    row = row + 1
    
    ws.Cells(row, 1).Value = "Compression Ratio:"
    ws.Cells(row, 2).Value = "3.88x"
    ws.Cells(row, 3).Value = "Near 4x"
    row = row + 2
    
    ' Format
    ws.Columns("A:C").AutoFit
    ws.Range("A1:C" & row).Font.Name = "Calibri"
    
    ' Generate charts
    Call GenerateScaleFactorChart
    Call GenerateErrorHistogram
    Call GeneratePerformanceChart
    
    ' Copy charts to report
    Call CopyChartsToReport
    
    ' Activate report sheet
    ws.Activate
    
    Exit Sub
    
ErrorHandler:
    MsgBox "Report generation failed: " & Err.Description, vbCritical, "Error"
End Sub

' ========================================
' 2. Copy charts to report
' ========================================
Sub CopyChartsToReport()
    On Error Resume Next
    
    Dim reportWs As Worksheet
    Dim quantWs As Worksheet
    Dim accWs As Worksheet
    Dim chartObj As ChartObject
    Dim topPos As Long
    
    Set reportWs = ThisWorkbook.Worksheets("Report")
    Set quantWs = ThisWorkbook.Worksheets("Quantization Stats")
    Set accWs = ThisWorkbook.Worksheets("Accuracy Log")
    
    If reportWs Is Nothing Then Exit Sub
    
    topPos = 350
    
    ' Copy scale factor chart
    If Not quantWs Is Nothing Then
        Set chartObj = quantWs.ChartObjects("ScaleFactorChart")
        If Not chartObj Is Nothing Then
            chartObj.Chart.ChartArea.Copy
            reportWs.Paste Destination:=reportWs.Range("E2")
        End If
    End If
    
    ' Copy error histogram
    If Not accWs Is Nothing Then
        Set chartObj = accWs.ChartObjects("ErrorHistogram")
        If Not chartObj Is Nothing Then
            chartObj.Chart.ChartArea.Copy
            reportWs.Paste Destination:=reportWs.Range("E20")
        End If
    End If
    
    Application.CutCopyMode = False
End Sub

' ========================================

