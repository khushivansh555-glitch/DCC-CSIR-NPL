from flask import (
    Flask,
    render_template,
    request,
    send_from_directory
)
import pandas as pd
import numpy as np
import os
import xml.etree.ElementTree as ET
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
GENERATED_FOLDER = "generated"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)


def generate_xml(results):

    root = ET.Element("CalibrationCertificate")

    info = ET.SubElement(root, "CertificateInfo")

    ET.SubElement(
    info,
    "Laboratory"
    ).text = "CSIR-National Physical Laboratory"

    ET.SubElement(
    info,
    "CertificateType"
).text = "Digital Calibration Certificate"

    ET.SubElement(
    info,
    "IssueDate"
    ).text = datetime.now().strftime("%Y-%m-%d")
    

    stats = ET.SubElement(root, "Statistics")

    ET.SubElement(stats, "Readings").text = str(results["n"])
    ET.SubElement(stats, "Mean").text = str(results["mean"])
    ET.SubElement(stats, "StdDeviation").text = str(results["std"])

    uncertainty = ET.SubElement(root, "Uncertainty")

    ET.SubElement(
        uncertainty,
        "TypeA"
    ).text = str(results["type_a"])

    ET.SubElement(
        uncertainty,
        "ResolutionContribution"
    ).text = str(results["u_res"])

    ET.SubElement(
        uncertainty,
        "CalibrationContribution"
    ).text = str(results["u_cal"])

    ET.SubElement(
        uncertainty,
        "DriftContribution"
    ).text = str(results["u_drift"])

    ET.SubElement(
        uncertainty,
        "TemperatureContribution"
    ).text = str(results["u_temp"])

    ET.SubElement(
        uncertainty,
        "TypeB"
    ).text = str(results["type_b"])

    ET.SubElement(
        uncertainty,
        "Combined"
    ).text = str(results["combined"])

    ET.SubElement(
        uncertainty,
        "Expanded"
    ).text = str(results["expanded"])

    xml_path = os.path.join(
        GENERATED_FOLDER,
        "certificate.xml"
    )

    xml_content = ET.tostring(
        root,
        encoding="unicode"
    )

    with open(
        xml_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write('<?xml version="1.0"?>\n')

        f.write(
            '<?xml-stylesheet type="text/xsl" href="certificate.xsl"?>\n'
        )

        f.write(xml_content)

    return xml_path


def generate_xslt():

    xslt = """<?xml version="1.0"?>

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
"""

    with open(
        os.path.join(
            GENERATED_FOLDER,
            "certificate.xsl"
        ),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(xslt)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():

    file = request.files["excel"]

    path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(path)

    df = pd.read_excel(path)

    readings = df.iloc[:, 0].dropna().values

    n = len(readings)

    mean = np.mean(readings)

    std = np.std(readings, ddof=1)

    type_a = std / np.sqrt(n)

    resolution = float(request.form["resolution"])

    calibration = float(request.form["calibration"])

    drift = float(request.form["drift"])

    temperature = float(request.form["temperature"])

    k = float(request.form["k"])

    u_res = resolution / np.sqrt(12)

    u_cal = calibration / k

    u_drift = drift / np.sqrt(3)

    u_temp = temperature / np.sqrt(3)

    type_b = np.sqrt(
        u_res**2 +
        u_cal**2 +
        u_drift**2 +
        u_temp**2
    )

    combined = np.sqrt(
        type_a**2 +
        type_b**2
    )

    expanded = 2 * combined

    results = {
        "n": n,
        "mean": round(mean, 8),
        "std": round(std, 8),
        "type_a": round(type_a, 8),
        "u_res": round(u_res, 8),
        "u_cal": round(u_cal, 8),
        "u_drift": round(u_drift, 8),
        "u_temp": round(u_temp, 8),
        "type_b": round(type_b, 8),
        "combined": round(combined, 8),
        "expanded": round(expanded, 8)
    }

    generate_xml(results)

    generate_xslt()

    return render_template(
        "result.html",
        results=results
    )


@app.route("/download/xml")
def download_xml():

    return send_from_directory(
        GENERATED_FOLDER,
        "certificate.xml",
        as_attachment=True
    )


@app.route("/download/xslt")
def download_xslt():

    return send_from_directory(
        GENERATED_FOLDER,
        "certificate.xsl",
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)