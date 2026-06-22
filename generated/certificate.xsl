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
.header{display:flex;align-items:flex-start;justify-content:flex-start;border-bottom:2px solid #999;padding-bottom:8px;margin-bottom:14px;position:relative}
.hdr-left{flex:0 0 100px}
.hdr-left img{width:100px}
    .hdr-center{flex:1 1 auto;text-align:left;padding-left:10px;min-width:0}
    .org-hi{color:#c0392b;font-weight:700;font-size:18px;margin:0}
.org-en{color:#2c3e50;font-weight:700;font-size:16px;margin:2px 0}
.header-subtext p{margin:2px 0;font-size:12px;line-height:1.3}
    .hdr-right{flex:0 0 140px;border-left:3px solid #ddd;padding-left:12px}
.cert-box{border:1px solid #333;padding:8px}
.cert-title{font-weight:700;font-size:14px;margin:0 0 6px 0}
.section-title{background:#003366;color:#fff;padding:8px;margin-top:18px;margin-bottom:10px;font-weight:bold}
table{border-collapse:collapse;width:100%;margin-bottom:12px}
th,td{border:1px solid #444;padding:6px;text-align:left}
th{background:#f1f7fb}
.footer-signatures{display:flex;flex-wrap:wrap;gap:12px;margin-top:20px}
.footer-column{flex:1 1 220px;min-width:200px;border:1px solid #444;padding:10px;text-align:left}
.footer-label{display:flex;justify-content:space-between;gap:12px;font-weight:700;margin-bottom:8px}
.footer-label span{display:inline-block}
.footer-en{text-align:left;flex:1}
.footer-hi{text-align:right;flex:1}
.footer-placeholder{margin-top:10px;font-size:14px}
]]></style>
</head>
<body>

<div class="header">
  <div class="hdr-left"><img src="../static/images/logo.png" alt="logo"/></div>
  <div class="hdr-center">
    <p class="org-hi">सी एस आई आर - राष्ट्रीय भौतिक प्रयोगशाला</p>
    <p class="org-en">CSIR - NATIONAL PHYSICAL LABORATORY</p>
    <div class="header-subtext">
      <p>(Council of Scientific and Industrial Research)</p>
      <p>(National Metrology Institute (NMI), Member BIPM and Signatory CIPM-MRA)</p>
      <p>Dr. K. S. Krishnan Marg, New Delhi – 110012, INDIA</p>
      <p>Phone: +91-11-4560 8441, 8610, 9447</p>
      <p>Fax: +91-11-4560 8448</p>
      <p>E-mail: [cttc@nplindia.org]</p>
      <p>Website: [www.nplindia.org]</p>
    </div>
  </div>
  <div class="hdr-right"><div class="cert-box"><p class="cert-title">CALIBRATION CERTIFICATE</p><p>Certificate No.: <strong><xsl:value-of select="CalibrationCertificate/CertificateInfo/CertificateNumber"/></strong></p><p>Date: <xsl:value-of select="CalibrationCertificate/CertificateInfo/IssueDate"/></p></div></div>
</div>

<div class="section-title">Certificate Information</div>
<table>
  <tr><td>Certificate Number</td><td><xsl:value-of select="CalibrationCertificate/CertificateInfo/CertificateNumber"/></td></tr>
  <tr><td>Calibration Date</td><td><xsl:value-of select="CalibrationCertificate/CertificateInfo/CalibrationDate"/></td></tr>
  <tr><td>Issue Date</td><td><xsl:value-of select="CalibrationCertificate/CertificateInfo/IssueDate"/></td></tr>
  <tr><td>Uploaded Data File</td><td><a>
        <xsl:attribute name="href"><xsl:text>/uploads/</xsl:text><xsl:value-of select="CalibrationCertificate/CertificateInfo/UploadedDataFile"/></xsl:attribute>
        <xsl:value-of select="CalibrationCertificate/CertificateInfo/UploadedDataFile"/>
      </a></td></tr>
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

<div class="footer-signatures">
  <div class="footer-column">
    <p class="footer-label">
      <span class="footer-en">Calibrated by:</span>
      <span class="footer-hi">कैलिब्रेटेड बाय:</span>
    </p>
    <p>________________________</p>
    <p>(Name) / (नाम)</p>
  </div>
  <div class="footer-column">
    <p class="footer-label">
      <span class="footer-en">Checked by:</span>
      <span class="footer-hi">चेक्ड बाय:</span>
    </p>
    <p>________________________</p>
    <p>(Name) / (नाम)</p>
  </div>
  <div class="footer-column">
    <p class="footer-label">
      <span class="footer-en">Scientist-in-charge:</span>
      <span class="footer-hi">वैज्ञानिक प्रभारी:</span>
    </p>
    <p>________________________</p>
    <p>(Name) / (नाम)</p>
  </div>
  <div class="footer-column">
    <p class="footer-label">
      <span class="footer-en">Issued by:</span>
      <span class="footer-hi">जारीकर्ता:</span>
    </p>
    <p>________________________</p>
    <p>(Director's Nominee) / (निदेशक का नामित)</p>
  </div>
</div>

<div style="margin-top:20px;font-size:12px">Certificate generated automatically.</div>

</body>
</html>

</xsl:template>
</xsl:stylesheet>
