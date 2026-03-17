Attribute VB_Name = "ChartModule"
Option Explicit

' ========================================
' Chart Generation Module
' ========================================

' ========================================
' 1. Generate scale factor bar chart
' ========================================
Sub GenerateScaleFactorChart()
    On Error GoTo ErrorHandler
    
    Dim ws As Worksheet
    Dim chartObj As ChartObject
    Dim lastRow As Long
    Dim dataRange As Range
    
    ' Check data sheet
    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets("Quantization Stats")
    On Error GoTo ErrorHandler
    
    If ws Is Nothing Then
        MsgBox "Please import quantization statistics first!", vbExclamation, "No Data"
        Exit Sub
    End If
    
    ' Get data range
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).row
    If lastRow < 2 Then
        MsgBox "No data available!", vbExclamation, "No Data"
        Exit Sub
    End If
    
    ' Delete old chart
    On Error Resume Next
    ws.ChartObjects("ScaleFactorChart").Delete
    On Error GoTo ErrorHandler
    
    ' Create chart
    Set chartObj = ws.ChartObjects.Add(Left:=300, Top:=10, Width:=500, Height:=300)
    chartObj.Name = "ScaleFactorChart"
    
    With chartObj.Chart
        .ChartType = xlColumnClustered
        
        ' Set data source
        .SetSourceData Source:=ws.Range("A1:B" & lastRow)
        
        ' Use a cleaner built-in style (if available)
        On Error Resume Next
        .ChartStyle = 201
        On Error GoTo ErrorHandler
        
        ' Set title
        .HasTitle = True
        .ChartTitle.Text = "Scale Factor Distribution"
        .ChartTitle.Font.Size = 14
        .ChartTitle.Font.Bold = True
        
        ' Set axes
        .Axes(xlCategory).HasTitle = True
        .Axes(xlCategory).AxisTitle.Text = "Layer Name"
        .Axes(xlCategory).TickLabels.Orientation = 45
        .Axes(xlValue).HasTitle = True
        .Axes(xlValue).AxisTitle.Text = "Scale Factor"
        
        ' Reduce clutter: no per-bar labels
        .SeriesCollection(1).HasDataLabels = False
        
        ' Set colors
        .SeriesCollection(1).Format.Fill.ForeColor.RGB = RGB(68, 114, 196)
        
        ' Set legend
        .HasLegend = False
    End With
    
    MsgBox "Scale factor chart generated.", vbInformation, "Chart Generated"
    
    Exit Sub
    
ErrorHandler:
    MsgBox "Chart generation failed: " & Err.Description, vbCritical, "Error"
End Sub

' ========================================
' 2. Generate error histogram
' ========================================
Sub GenerateErrorHistogram()
    On Error GoTo ErrorHandler
    
    Dim ws As Worksheet
    Dim chartObj As ChartObject
    Dim lastRow As Long
    Dim errorRange As Range
    Dim histWs As Worksheet
    Dim bins() As Double
    Dim freq() As Long
    Dim i As Long, j As Long
    Dim numBins As Integer
    
    ' Check data sheet
    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets("Accuracy Log")
    On Error GoTo ErrorHandler
    
    If ws Is Nothing Then
        MsgBox "Please import accuracy log first!", vbExclamation, "No Data"
        Exit Sub
    End If
    
    ' Get error data
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).row
    If lastRow < 2 Then
        MsgBox "No data available!", vbExclamation, "No Data"
        Exit Sub
    End If
    
    Set errorRange = ws.Range("D2:D" & lastRow)
    
    ' Create temporary sheet for histogram data
    On Error Resume Next
    Set histWs = ThisWorkbook.Worksheets("_HistTemp")
    If histWs Is Nothing Then
        Set histWs = ThisWorkbook.Worksheets.Add
        histWs.Name = "_HistTemp"
    End If
    histWs.Visible = xlSheetVeryHidden
    On Error GoTo ErrorHandler
    
    histWs.Cells.Clear
    
    ' Set bins (10 bins)
    numBins = 10
    ReDim bins(0 To numBins)
    ReDim freq(0 To numBins - 1)
    
    Dim minError As Double, maxError As Double
    minError = Application.WorksheetFunction.Min(errorRange)
    maxError = Application.WorksheetFunction.Max(errorRange)
    
    Dim binWidth As Double
    binWidth = (maxError - minError) / numBins
    
    ' Create bin boundaries
    For i = 0 To numBins
        bins(i) = minError + i * binWidth
        histWs.Cells(i + 2, 1).Value = bins(i)
    Next i
    
    ' Calculate frequency
    Dim errorVal As Double
    For i = 2 To lastRow
        errorVal = ws.Cells(i, 4).Value
        For j = 0 To numBins - 1
            If errorVal >= bins(j) And errorVal < bins(j + 1) Then
                freq(j) = freq(j) + 1
                Exit For
            ElseIf j = numBins - 1 And errorVal = bins(numBins) Then
                freq(j) = freq(j) + 1
            End If
        Next j
    Next i
    
    ' Write frequency data
    histWs.Cells(1, 1).Value = "Error Range"
    histWs.Cells(1, 2).Value = "Frequency"
    histWs.Cells(1, 1).Value = "Error Range"
    histWs.Cells(1, 2).Value = "Frequency"
    For i = 0 To numBins - 1
        histWs.Cells(i + 2, 1).Value = Format(bins(i), "0.000000") & " - " & Format(bins(i + 1), "0.000000")
        histWs.Cells(i + 2, 2).Value = freq(i)
    Next i
    
    ' Delete old chart
    On Error Resume Next
    ws.ChartObjects("ErrorHistogram").Delete
    On Error GoTo ErrorHandler
    
    ' Create chart
    Set chartObj = ws.ChartObjects.Add(Left:=350, Top:=10, Width:=500, Height:=300)
    chartObj.Name = "ErrorHistogram"
    
    With chartObj.Chart
        .ChartType = xlColumnClustered
        
        ' Set data source
        .SetSourceData Source:=histWs.Range("A1:B" & numBins + 1)
        
        ' Use a cleaner built-in style (if available)
        On Error Resume Next
        .ChartStyle = 204
        On Error GoTo ErrorHandler
        
        ' Set title
        .HasTitle = True
        .ChartTitle.Text = "Error Distribution Histogram"
        .ChartTitle.Font.Size = 14
        .ChartTitle.Font.Bold = True
        
        ' Set axes
        .Axes(xlCategory).HasTitle = True
        .Axes(xlCategory).AxisTitle.Text = "Error Range"
        .Axes(xlValue).HasTitle = True
        .Axes(xlValue).AxisTitle.Text = "Frequency"
        
        ' Set colors
        .SeriesCollection(1).Format.Fill.ForeColor.RGB = RGB(237, 125, 49)
        
        ' Set legend
        .HasLegend = False
        
        ' Adjust gap / outline
        .SeriesCollection(1).Format.Line.Visible = msoTrue
        .SeriesCollection(1).Format.Line.ForeColor.RGB = RGB(255, 255, 255)
    End With
    
    MsgBox "Error histogram generated.", vbInformation, "Chart Generated"
    
    Exit Sub
    
ErrorHandler:
    MsgBox "Chart generation failed: " & Err.Description, vbCritical, "Error"
End Sub

' ========================================
' 3. Generate performance comparison chart
' ========================================
Sub GeneratePerformanceChart()
    On Error GoTo ErrorHandler
    
    Dim ws As Worksheet
    Dim chartObj As ChartObject
    Dim perfWs As Worksheet
    
    ' Create temporary sheet for performance data
    On Error Resume Next
    Set perfWs = ThisWorkbook.Worksheets("_PerfTemp")
    If perfWs Is Nothing Then
        Set perfWs = ThisWorkbook.Worksheets.Add
        perfWs.Name = "_PerfTemp"
    End If
    perfWs.Visible = xlSheetVeryHidden
    On Error GoTo ErrorHandler
    
    perfWs.Cells.Clear
    
    ' Set performance data (from SUCCESS_REPORT)
    perfWs.Cells(1, 1).Value = "Metric"
    perfWs.Cells(1, 2).Value = "FP32"
    perfWs.Cells(1, 3).Value = "INT8"
    
    perfWs.Cells(2, 1).Value = "Inference Time (ms)"
    perfWs.Cells(2, 2).Value = 0.04  ' FP32 time
    perfWs.Cells(2, 3).Value = 0.03  ' INT8 time
    
    perfWs.Cells(3, 1).Value = "Model Size (KB)"
    perfWs.Cells(3, 2).Value = 264  ' FP32 size
    perfWs.Cells(3, 3).Value = 68   ' INT8 size
    
    ' Get report sheet
    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets("Report")
    If ws Is Nothing Then
        Set ws = ThisWorkbook.Worksheets.Add
        ws.Name = "Report"
    End If
    On Error GoTo ErrorHandler
    
    ' Delete old chart
    On Error Resume Next
    ws.ChartObjects("PerformanceChart").Delete
    On Error GoTo ErrorHandler
    
    ' Create chart
    Set chartObj = ws.ChartObjects.Add(Left:=50, Top:=350, Width:=600, Height:=300)
    chartObj.Name = "PerformanceChart"
    
    With chartObj.Chart
        .ChartType = xlBarClustered
        
        ' Set data source
        .SetSourceData Source:=perfWs.Range("A1:C3")
        
        ' Use a cleaner built-in style (if available)
        On Error Resume Next
        .ChartStyle = 206
        On Error GoTo ErrorHandler
        
        ' Set title
        .HasTitle = True
        .ChartTitle.Text = "Performance Comparison (FP32 vs INT8)"
        .ChartTitle.Font.Size = 14
        .ChartTitle.Font.Bold = True
        
        ' Set axes
        .Axes(xlCategory).HasTitle = False
        .Axes(xlValue).HasTitle = True
        .Axes(xlValue).AxisTitle.Text = "Value"
        
        ' Set data labels
        .SeriesCollection(1).HasDataLabels = True
        .SeriesCollection(2).HasDataLabels = True
        
        ' Set colors
        .SeriesCollection(1).Format.Fill.ForeColor.RGB = RGB(68, 114, 196)  ' FP32 - Blue
        .SeriesCollection(2).Format.Fill.ForeColor.RGB = RGB(112, 173, 71)  ' INT8 - Green
        
        ' Set legend
        .HasLegend = True
        .Legend.Position = xlLegendPositionBottom
    End With
    
    MsgBox "Performance comparison chart generated.", vbInformation, "Chart Generated"
    
    Exit Sub
    
ErrorHandler:
    MsgBox "Chart generation failed: " & Err.Description, vbCritical, "Error"
End Sub
