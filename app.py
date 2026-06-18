from flask import (
    Flask,
    render_template,
    request,
    send_from_directory
)
from scipy.stats import norm
import matplotlib.pyplot as plt
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
    ET.SubElement(info, "Laboratory").text = "CSIR-National Physical Laboratory"
    ET.SubElement(info, "CertificateType").text = "Digital Calibration Certificate"
    ET.SubElement(info, "IssueDate").text = datetime.now().strftime("%Y-%m-%d")
    ET.SubElement(info, "ConfidenceLevel").text = str(results["confidence"])
    ET.SubElement(info, "CoverageFactor").text = str(results["coverage_factor"])
    ET.SubElement(
        info,
        "CertificateNumber"
    ).text = results["certificate_number"]

    ET.SubElement(
        info,
        "CalibrationDate"
    ).text = results["calibration_date"]

    customer = ET.SubElement(
        root,
        "Customer"
    )

    ET.SubElement(
        customer,
        "CustomerName"
    ).text = results["customer_name"]

    ET.SubElement(
        customer,
        "Organization"
    ).text = results["organization"]

    instrument = ET.SubElement(
        root,
        "Instrument"
    )

    ET.SubElement(
        instrument,
        "InstrumentName"
    ).text = results["instrument_name"]

    ET.SubElement(
        instrument,
        "InstrumentID"
    ).text = results["instrument_id"]

    ET.SubElement(
        instrument,
        "Manufacturer"
    ).text = results["manufacturer"]

    ET.SubElement(
        instrument,
        "ModelNumber"
    ).text = results["model_number"]

    ET.SubElement(
        instrument,
        "SerialNumber"
    ).text = results["serial_number"]

    environment = ET.SubElement(
        root,
        "Environment"
    )

    ET.SubElement(
        environment,
        "Temperature"
    ).text = results["ambient_temperature"]

    ET.SubElement(
        environment,
        "Humidity"
    ).text = results["humidity"]

    stats = ET.SubElement(root, "Statistics")

    ET.SubElement(stats, "Readings").text = str(results["n"])
    ET.SubElement(stats, "Mean").text = str(results["mean"])
    ET.SubElement(stats, "StdDeviation").text = str(results["std"])

    uncertainty = ET.SubElement(root, "Uncertainty")

    ET.SubElement(
    uncertainty,
    "MCMean"
    ).text = str(results["mc_mean"])

    ET.SubElement(
    uncertainty,
    "MCStd"
    ).text = str(results["mc_std"])

    ET.SubElement(
    uncertainty,
    "MCExpanded"
    ).text = str(results["mc_expanded"])  

    ET.SubElement(
        uncertainty,
        "TypeA"
    ).text = str(results["type_a"])

    ET.SubElement(
        uncertainty,
        "ResolutionUnit"
    ).text = results["resolution_unit"]

    ET.SubElement(
        uncertainty,
        "CalibrationUnit"
    ).text = results["calibration_unit"]

    ET.SubElement(
        uncertainty,
        "DriftUnit"
    ).text = results["drift_unit"]

    ET.SubElement(
        uncertainty,
        "TemperatureUnit"
    ).text = results["temperature_unit"]

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

# Comparison Section

    comparison = ET.SubElement(
        root,
        "Comparison"
    )

    ET.SubElement(
        comparison,
        "Difference"
    ).text = str(results["difference"])

    ET.SubElement(
        comparison,
        "PercentDifference"
    ).text = str(results["percent_difference"])

    bayesian = ET.SubElement(
        root,
        "Bayesian"
    )

    ET.SubElement(
        bayesian,
        "PosteriorMean"
    ).text = str(results["posterior_mean"])

    ET.SubElement(
        bayesian,
        "PosteriorStd"
    ).text = str(results["posterior_std"])

    ET.SubElement(
        bayesian,
        "CredibleLower"
    ).text = str(results["credible_lower"])

    ET.SubElement(
        bayesian,
        "CredibleUpper"
    ).text = str(results["credible_upper"])

    remarks = ET.SubElement(
        root,
        "Remarks"
    )

    remarks.text = results["remarks"]

    # D-SI Section

    dsi = ET.SubElement(
        root,
        "DSI"
    )

    ET.SubElement(
        dsi,
        "Quantity"
    ).text = results["quantity"]

    ET.SubElement(
        dsi,
        "MeasuredValue"
    ).text = str(results["mean"])

    ET.SubElement(
        dsi,
        "ExpandedUncertainty"
    ).text = str(results["expanded"])

    ET.SubElement(
        dsi,
        "CoverageFactor"
    ).text = str(results["coverage_factor"])

    ET.SubElement(
    dsi,
    "Unit"
    ).text = results["resolution_unit"]

    ET.SubElement(
    dsi,
    "Symbol"
    ).text = results["resolution_unit"]

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
    # Certificate Information

    certificate_number = request.form["certificate_number"]

    customer_name = request.form["customer_name"]

    organization = request.form["organization"]

    instrument_name = request.form["instrument_name"]

    instrument_id = request.form["instrument_id"]

    manufacturer = request.form["manufacturer"]

    model_number = request.form["model_number"]

    serial_number = request.form["serial_number"]

    calibration_date = request.form["calibration_date"]

    ambient_temperature = request.form["ambient_temperature"]

    humidity = request.form["humidity"]

    remarks = request.form["remarks"]

    resolution = float(request.form["resolution"])

    calibration = float(request.form["calibration"])

    drift = float(request.form["drift"])

    temperature = float(request.form["temperature"])

    resolution_unit = request.form["resolution_unit"]

    calibration_unit = request.form["calibration_unit"]

    drift_unit = request.form["drift_unit"]

    temperature_unit = request.form["temperature_unit"]

    quantity = request.form["quantity"]

    confidence = int(request.form["confidence"])

    if confidence == 90:
        k = 1.645
    elif confidence == 95:
        k = 2.0
    elif confidence == 99:
        k = 2.58
    else:
        k = 2.0

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

    expanded = k * combined

    # Monte Carlo Simulation

    N = 100000

    res_samples = np.random.uniform(
        -resolution / 2,
        resolution / 2,
        N
    )

    cal_samples = np.random.normal(
        0,
        calibration / k,
        N
    )

    drift_samples = np.random.uniform(
        -drift,
        drift,
        N
    )

    temp_samples = np.random.uniform(
        -temperature,
        temperature,
        N
    )

    mc_results = (
        mean
        + res_samples
        + cal_samples
        + drift_samples
        + temp_samples
    )

    mc_mean = np.mean(mc_results)

    mc_std = np.std(mc_results)

    mc_expanded = k * mc_std

    # Bayesian Inference

    prior_mean = mean

    prior_std = combined

    sample_mean = mean

    sample_std = std

    likelihood_var = (sample_std ** 2) / n

    prior_var = prior_std ** 2

    posterior_var = 1 / (
        (1 / prior_var)
        +
        (1 / likelihood_var)
    )

    posterior_mean = posterior_var * (
        (prior_mean / prior_var)
        +
        (sample_mean / likelihood_var)
    )

    posterior_std = np.sqrt(
        posterior_var
    )

    lower95 = posterior_mean - (
        1.96 * posterior_std
    )

    upper95 = posterior_mean + (
        1.96 * posterior_std
    )

    x = np.linspace(
        posterior_mean - 5 * posterior_std,
        posterior_mean + 5 * posterior_std,
        1000
    )

    prior_pdf = norm.pdf(
        x,
        prior_mean,
        prior_std
    )

    likelihood_pdf = norm.pdf(
        x,
        sample_mean,
        np.sqrt(likelihood_var)
    )

    posterior_pdf = norm.pdf(
        x,
        posterior_mean,
        posterior_std
    )
    plt.figure(figsize=(8,5))

    plt.plot(
        x,
        prior_pdf,
        label="Prior"
    )

    plt.plot(
        x,
        likelihood_pdf,
        label="Likelihood"
    )

    plt.plot(
        x,
        posterior_pdf,
        label="Posterior"
    )

    plt.xlabel("Measured Value")

    plt.ylabel("Probability Density")

    plt.title(
        "Bayesian Inference"
    )

    plt.legend()

    plt.grid(True)

    bayes_graph = os.path.join(
        "static",
        "bayesian_graph.png"
    )

    plt.savefig(
        bayes_graph,
        bbox_inches="tight"
    )

    plt.close()

    difference = abs(
        expanded -
        mc_expanded
    )

    percent_difference = (
        difference / expanded
    ) * 100

    results = {
        "quantity": quantity,

        "certificate_number": certificate_number,

"customer_name": customer_name,

"organization": organization,

"instrument_name": instrument_name,

"instrument_id": instrument_id,

"manufacturer": manufacturer,

"model_number": model_number,

"serial_number": serial_number,

"calibration_date": calibration_date,

"ambient_temperature": ambient_temperature,

"humidity": humidity,

    "remarks": remarks,
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
            "expanded": round(expanded, 8),
            "confidence": confidence,
            "coverage_factor": round(k, 3),
            "resolution_unit": resolution_unit,
            "calibration_unit": calibration_unit,
            "drift_unit": drift_unit,
            "temperature_unit": temperature_unit,
            "mc_mean": round(mc_mean, 8),
            "mc_std": round(mc_std, 8),
            "mc_expanded": round(mc_expanded, 8),
            "posterior_mean": round(float(posterior_mean), 8),
            "posterior_std": round(float(posterior_std), 8),
            "credible_lower": round(float(lower95), 8),
            "credible_upper": round(float(upper95), 8),
            "bayesian_graph":
            "bayesian_graph.png",
            "difference": round(difference, 8),
            "percent_difference": round(percent_difference, 3),
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