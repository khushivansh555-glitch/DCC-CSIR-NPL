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
Certificate Information
</div>

<table>

<tr>
<td>Certificate Number</td>
<td>
<xsl:value-of
select="CalibrationCertificate/CertificateInfo/CertificateNumber"/>
</td>
</tr>

<tr>
<td>Calibration Date</td>
<td>
<xsl:value-of
select="CalibrationCertificate/CertificateInfo/CalibrationDate"/>
</td>
</tr>

<tr>
<td>Issue Date</td>
<td>
<xsl:value-of
select="CalibrationCertificate/CertificateInfo/IssueDate"/>
</td>
</tr>

</table>

<div class="section-title">
Customer Information
</div>

<table>

<tr>
<td>Customer Name</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Customer/CustomerName"/>
</td>
</tr>

<tr>
<td>Organization</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Customer/Organization"/>
</td>
</tr>

</table>

<div class="section-title">
Instrument Information
</div>

<table>

<tr>
<td>Instrument Name</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Instrument/InstrumentName"/>
</td>
</tr>

<tr>
<td>Instrument ID</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Instrument/InstrumentID"/>
</td>
</tr>

<tr>
<td>Manufacturer</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Instrument/Manufacturer"/>
</td>
</tr>

<tr>
<td>Model Number</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Instrument/ModelNumber"/>
</td>
</tr>

<tr>
<td>Serial Number</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Instrument/SerialNumber"/>
</td>
</tr>

</table>

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
<th>Unit</th>
</tr>

<tr>
<td>Resolution</td>

<td>
<xsl:value-of
select="CalibrationCertificate/Uncertainty/ResolutionContribution"/>
</td>

<td>
<xsl:value-of
select="CalibrationCertificate/Uncertainty/ResolutionUnit"/>
</td>

</tr>

<tr>
<td>Calibration</td>

<td>
<xsl:value-of
select="CalibrationCertificate/Uncertainty/CalibrationContribution"/>
</td>

<td>
<xsl:value-of
select="CalibrationCertificate/Uncertainty/CalibrationUnit"/>
</td>

</tr>

<tr>
<td>Drift</td>

<td>
<xsl:value-of
select="CalibrationCertificate/Uncertainty/DriftContribution"/>
</td>

<td>
<xsl:value-of
select="CalibrationCertificate/Uncertainty/DriftUnit"/>
</td>

</tr>

<tr>
<td>Temperature</td>

<td>
<xsl:value-of
select="CalibrationCertificate/Uncertainty/TemperatureContribution"/>
</td>

<td>
<xsl:value-of
select="CalibrationCertificate/Uncertainty/TemperatureUnit"/>
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

<div class="section-title">
Monte Carlo Results
</div>

<table>

<tr>
<th>Parameter</th>
<th>Value</th>
</tr>

<tr>
<td>Monte Carlo Mean</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Uncertainty/MCMean"/>
</td>
</tr>

<tr>
<td>Monte Carlo Std</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Uncertainty/MCStd"/>
</td>
</tr>

<tr>
<td>Monte Carlo Expanded</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Uncertainty/MCExpanded"/>
</td>
</tr>

</table>

<div class="section-title">
GUM vs Monte Carlo Comparison
</div>

<table>

<tr>
<th>Metric</th>
<th>Value</th>
</tr>

<tr>
<td>Absolute Difference</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Comparison/Difference"/>
</td>
</tr>

<tr>
<td>Percent Difference</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Comparison/PercentDifference"/>%
</td>
</tr>

</table>

<div class="section-title">
D-SI Metadata
</div>

<table>

<tr>
<th>Parameter</th>
<th>Value</th>
</tr>

<tr>
<td>Quantity</td>
<td>
<xsl:value-of
select="CalibrationCertificate/DSI/Quantity"/>
</td>
</tr>

<tr>
<td>Measured Value</td>
<td>
<xsl:value-of
select="CalibrationCertificate/DSI/MeasuredValue"/>
</td>
</tr>

<tr>
<td>Unit</td>
<td>
<xsl:value-of
select="CalibrationCertificate/DSI/Unit"/>
</td>
</tr>

<tr>
<td>Expanded Uncertainty</td>
<td>
<xsl:value-of
select="CalibrationCertificate/DSI/ExpandedUncertainty"/>
</td>
</tr>

<tr>
<td>Coverage Factor</td>
<td>
<xsl:value-of
select="CalibrationCertificate/DSI/CoverageFactor"/>
</td>
</tr>

</table>

<div class="section-title">
Bayesian Inference Results
</div>

<table>

<tr>
<th>Parameter</th>
<th>Value</th>
</tr>

<tr>
<td>Posterior Mean</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Bayesian/PosteriorMean"/>
</td>
</tr>

<tr>
<td>Posterior Std</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Bayesian/PosteriorStd"/>
</td>
</tr>

<tr>
<td>95% Credible Lower</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Bayesian/CredibleLower"/>
</td>
</tr>

<tr>
<td>95% Credible Upper</td>
<td>
<xsl:value-of
select="CalibrationCertificate/Bayesian/CredibleUpper"/>
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
