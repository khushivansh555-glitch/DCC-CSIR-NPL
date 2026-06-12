<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">

<html>

<head>

<title>Digital Calibration Certificate</title>

<style><![CDATA[

body{
font-family:Arial, sans-serif;
margin:40px;
background:#ffffff;
color:#000000;
}

.header{
display:flex;
align-items:center;
border-bottom:3px solid #003366;
padding-bottom:15px;
margin-bottom:25px;
}

.logo{
width:120px;
height:auto;
margin-right:20px;
}

.title-section{
flex:1;
}

.main-title{
font-size:28px;
font-weight:bold;
color:#003366;
margin:0;
}

.sub-title{
font-size:16px;
margin-top:5px;
}

.section-title{
background:#003366;
color:white;
padding:8px;
margin-top:20px;
margin-bottom:10px;
font-weight:bold;
}

table{
border-collapse:collapse;
width:100%;
margin-bottom:20px;
}

th{
background:#e8eef7;
}

th,td{
border:1px solid #444;
padding:8px;
text-align:left;
}

.footer{
margin-top:40px;
border-top:2px solid #003366;
padding-top:15px;
}

.signature{
margin-top:50px;
}

]]></style>

</head>

<body>

<div class="header">

<img
class="logo"
src="../static/images/logo.png"/>

<div class="title-section">

<p class="main-title">
DIGITAL CALIBRATION CERTIFICATE
</p>

<p class="sub-title">
CSIR-National Physical Laboratory
</p>

<p class="sub-title">
Machine Readable Digital Calibration Certificate
</p>

</div>

</div>

<div class="section-title">
Statistical Analysis
</div>

<table>

<tr>
<th>Parameter</th>
<th>Value</th>
</tr>

<tr>
<td>Number of Readings</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Statistics/Readings"/>
</td>
</tr>

<tr>
<td>Mean</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Statistics/Mean"/>
</td>
</tr>

<tr>
<td>Standard Deviation</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Statistics/StdDeviation"/>
</td>
</tr>

</table>

<div class="section-title">
Type B Contributions
</div>

<table>

<tr>
<th>Component</th>
<th>Contribution</th>
</tr>

<tr>
<td>Resolution</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Uncertainty/ResolutionContribution"/>
</td>
</tr>

<tr>
<td>Calibration</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Uncertainty/CalibrationContribution"/>
</td>
</tr>

<tr>
<td>Drift</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Uncertainty/DriftContribution"/>
</td>
</tr>

<tr>
<td>Temperature</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Uncertainty/TemperatureContribution"/>
</td>
</tr>

</table>

<div class="section-title">
Final Uncertainty Results
</div>

<table>

<tr>
<th>Parameter</th>
<th>Value</th>
</tr>

<tr>
<td>Type A Uncertainty</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Uncertainty/TypeA"/>
</td>
</tr>

<tr>
<td>Type B Uncertainty</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Uncertainty/TypeB"/>
</td>
</tr>

<tr>
<td>Combined Uncertainty</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Uncertainty/Combined"/>
</td>
</tr>

<tr>
<td>Expanded Uncertainty (k=2)</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Uncertainty/Expanded"/>
</td>
</tr>

</table>

<div class="footer">

<p>
Certificate generated automatically using Digital Calibration Certificate workflow.
</p>

<div class="signature">

<p>
_____________________________
</p>

<p>
Authorized Signatory
</p>

</div>

</div>

</body>

</html>

</xsl:template>

</xsl:stylesheet>
