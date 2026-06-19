<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" indent="yes"/>
<xsl:template match="/">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<title>Calibration Certificate</title>
<style><![CDATA[
body{font-family:Arial, sans-serif;margin:30px;color:#000}
.header{display:flex;align-items:flex-start;justify-content:space-between;border-bottom:2px solid #999;padding-bottom:8px;margin-bottom:14px}
.hdr-left{flex:0 0 120px}
.hdr-left img{width:120px}
.hdr-center{flex:1;text-align:left;padding-left:10px}
.org-hi{color:#c0392b;font-weight:700;font-size:18px;margin:0}
.org-en{color:#2c3e50;font-weight:700;font-size:16px;margin:2px 0}
.hdr-right{flex:0 0 260px;border-left:3px solid #ddd;padding-left:12px}
.cert-box{border:1px solid #333;padding:8px}
.cert-title{font-weight:700;font-size:14px;margin:0 0 6px 0}
.section-title{background:#003366;color:#fff;padding:8px;margin-top:18px;margin-bottom:10px;font-weight:bold}
table{border-collapse:collapse;width:100%;margin-bottom:12px}
th,td{border:1px solid #444;padding:6px;text-align:left}
th{background:#f1f7fb}
]]></style>
</head>
<body>

<div class="header">
  <div class="hdr-left"><img src="../static/images/logo.png" alt="logo"/></div>
  <div class="hdr-center">
    <p class="org-hi">सी एस आई आर - राष्ट्रीय भौतिक प्रयोगशाला</p>
    <p class="org-en">CSIR - NATIONAL PHYSICAL LABORATORY</p>
  </div>
  <div class="hdr-right"><div class="cert-box"><p class="cert-title">CALIBRATION CERTIFICATE</p><p>Certificate No.: <strong><xsl:value-of select="CalibrationCertificate/CertificateInfo/CertificateNumber"/></strong></p><p>Date: <xsl:value-of select="CalibrationCertificate/CertificateInfo/IssueDate"/></p></div></div>
</div>

<div class="section-title">Certificate Information</div>
<table>
  <tr><td>Certificate Number</td><td><xsl:value-of select="CalibrationCertificate/CertificateInfo/CertificateNumber"/></td></tr>
  <tr><td>Calibration Date</td><td><xsl:value-of select="CalibrationCertificate/CertificateInfo/CalibrationDate"/></td></tr>
  <tr><td>Issue Date</td><td><xsl:value-of select="CalibrationCertificate/CertificateInfo/IssueDate"/></td></tr>
</table>

<div class="section-title">Customer Information</div>
<table>
  <tr><td>Customer Name</td><td><xsl:value-of select="CalibrationCertificate/Customer/CustomerName"/></td></tr>
  <tr><td>Organization</td><td><xsl:value-of select="CalibrationCertificate/Customer/Organization"/></td></tr>
</table>

<div class="section-title">Instrument Information</div>
<table>
  <tr><td>Instrument Name</td><td><xsl:value-of select="CalibrationCertificate/Instrument/InstrumentName"/></td></tr>
  <tr><td>Instrument ID</td><td><xsl:value-of select="CalibrationCertificate/Instrument/InstrumentID"/></td></tr>
  <tr><td>Manufacturer</td><td><xsl:value-of select="CalibrationCertificate/Instrument/Manufacturer"/></td></tr>
  <tr><td>Model Number</td><td><xsl:value-of select="CalibrationCertificate/Instrument/ModelNumber"/></td></tr>
  <tr><td>Serial Number</td><td><xsl:value-of select="CalibrationCertificate/Instrument/SerialNumber"/></td></tr>
</table>

<div class="section-title">Statistical Analysis</div>
<table>
  <tr><th>Parameter</th><th>Value</th></tr>
  <tr><td>Number of Readings</td><td><xsl:value-of select="CalibrationCertificate/Statistics/Readings"/></td></tr>
  <tr><td>Mean</td><td><xsl:value-of select="CalibrationCertificate/Statistics/Mean"/></td></tr>
  <tr><td>Standard Deviation</td><td><xsl:value-of select="CalibrationCertificate/Statistics/StdDeviation"/></td></tr>
</table>

<div class="section-title">Uncertainty &amp; Monte Carlo</div>
<table>
  <tr><td>Type A</td><td><xsl:value-of select="CalibrationCertificate/Uncertainty/TypeA"/></td></tr>
  <tr><td>Type B</td><td><xsl:value-of select="CalibrationCertificate/Uncertainty/TypeB"/></td></tr>
  <tr><td>Combined</td><td><xsl:value-of select="CalibrationCertificate/Uncertainty/Combined"/></td></tr>
  <tr><td>Expanded (k)</td><td><xsl:value-of select="CalibrationCertificate/Uncertainty/Expanded"/></td></tr>
  <tr><td>MC Mean</td><td><xsl:value-of select="CalibrationCertificate/Uncertainty/MCMean"/></td></tr>
  <tr><td>MC Std</td><td><xsl:value-of select="CalibrationCertificate/Uncertainty/MCStd"/></td></tr>
  <tr><td>MC Expanded</td><td><xsl:value-of select="CalibrationCertificate/Uncertainty/MCExpanded"/></td></tr>
</table>

<div class="section-title">Comparison</div>
<table>
  <tr><td>Absolute Difference</td><td><xsl:value-of select="CalibrationCertificate/Comparison/Difference"/></td></tr>
  <tr><td>Percent Difference</td><td><xsl:value-of select="CalibrationCertificate/Comparison/PercentDifference"/>%</td></tr>
</table>

<div class="section-title">Bayesian Inference</div>
<table>
  <tr><td>Posterior Mean</td><td><xsl:value-of select="CalibrationCertificate/Bayesian/PosteriorMean"/></td></tr>
  <tr><td>Posterior Std</td><td><xsl:value-of select="CalibrationCertificate/Bayesian/PosteriorStd"/></td></tr>
  <tr><td>95% Credible Lower</td><td><xsl:value-of select="CalibrationCertificate/Bayesian/CredibleLower"/></td></tr>
  <tr><td>95% Credible Upper</td><td><xsl:value-of select="CalibrationCertificate/Bayesian/CredibleUpper"/></td></tr>
</table>

<div class="section-title">Digital Signature</div>
<table>
  <tr><td>Algorithm</td><td><xsl:value-of select="CalibrationCertificate/DigitalSignature/Algorithm"/></td></tr>
  <tr><td>Signature</td><td><xsl:value-of select="CalibrationCertificate/DigitalSignature/SignatureValue"/></td></tr>
</table>

<div style="margin-top:20px;font-size:12px">Certificate generated automatically.</div>

</body>
</html>

</xsl:template>
</xsl:stylesheet>
