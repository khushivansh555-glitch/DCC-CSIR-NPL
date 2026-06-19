from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    jsonify,
    send_file
)
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import xml.etree.ElementTree as ET
from datetime import datetime
import lxml.etree as etree
from io import BytesIO
from fpdf import FPDF

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
GENERATED_FOLDER = "generated"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)


def sign_data(data):
    with open("keys/private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

        try:
            signature = private_key.sign(
                data.encode(),
                padding.PKCS1v15(),
                hashes.SHA256()
            )

            return signature.hex()
        except Exception:
            # If private key is missing or invalid, return a placeholder signature
            return "UNSIGNED"


def generate_xml(results):
    root = ET.Element("CalibrationCertificate")

    info = ET.SubElement(root, "CertificateInfo")
    ET.SubElement(info, "Laboratory").text = "CSIR-National Physical Laboratory"
    ET.SubElement(info, "CertificateType").text = "Digital Calibration Certificate"
    ET.SubElement(info, "IssueDate").text = datetime.now().strftime("%Y-%m-%d")
    ET.SubElement(info, "ConfidenceLevel").text = str(results.get("confidence", ""))
    ET.SubElement(info, "CoverageFactor").text = str(results.get("coverage_factor", ""))
    ET.SubElement(info, "CertificateNumber").text = results.get("certificate_number", "")
    ET.SubElement(info, "CalibrationDate").text = results.get("calibration_date", "")

    customer = ET.SubElement(root, "Customer")
    ET.SubElement(customer, "CustomerName").text = results.get("customer_name", "")
    ET.SubElement(customer, "Organization").text = results.get("organization", "")

    instrument = ET.SubElement(root, "Instrument")
    ET.SubElement(instrument, "InstrumentName").text = results.get("instrument_name", "")
    ET.SubElement(instrument, "InstrumentID").text = results.get("instrument_id", "")
    ET.SubElement(instrument, "Manufacturer").text = results.get("manufacturer", "")
    ET.SubElement(instrument, "ModelNumber").text = results.get("model_number", "")
    ET.SubElement(instrument, "SerialNumber").text = results.get("serial_number", "")

    environment = ET.SubElement(root, "Environment")
    ET.SubElement(environment, "Temperature").text = str(results.get("ambient_temperature", ""))
    ET.SubElement(environment, "Humidity").text = str(results.get("humidity", ""))

    stats = ET.SubElement(root, "Statistics")
    ET.SubElement(stats, "Readings").text = str(results.get("n", ""))
    ET.SubElement(stats, "Mean").text = str(results.get("mean", ""))
    ET.SubElement(stats, "StdDeviation").text = str(results.get("std", ""))

    uncertainty = ET.SubElement(root, "Uncertainty")
    ET.SubElement(uncertainty, "MCMean").text = str(results.get("mc_mean", ""))
    ET.SubElement(uncertainty, "MCStd").text = str(results.get("mc_std", ""))
    ET.SubElement(uncertainty, "MCExpanded").text = str(results.get("mc_expanded", ""))
    ET.SubElement(uncertainty, "TypeA").text = str(results.get("type_a", ""))
    ET.SubElement(uncertainty, "ResolutionUnit").text = results.get("resolution_unit", "")
    ET.SubElement(uncertainty, "CalibrationUnit").text = results.get("calibration_unit", "")
    ET.SubElement(uncertainty, "DriftUnit").text = results.get("drift_unit", "")
    ET.SubElement(uncertainty, "TemperatureUnit").text = results.get("temperature_unit", "")
    ET.SubElement(uncertainty, "ResolutionContribution").text = str(results.get("u_res", ""))
    ET.SubElement(uncertainty, "CalibrationContribution").text = str(results.get("u_cal", ""))
    ET.SubElement(uncertainty, "DriftContribution").text = str(results.get("u_drift", ""))
    ET.SubElement(uncertainty, "TemperatureContribution").text = str(results.get("u_temp", ""))
    ET.SubElement(uncertainty, "TypeB").text = str(results.get("type_b", ""))
    ET.SubElement(uncertainty, "Combined").text = str(results.get("combined", ""))
    ET.SubElement(uncertainty, "Expanded").text = str(results.get("expanded", ""))

    comparison = ET.SubElement(root, "Comparison")
    ET.SubElement(comparison, "Difference").text = str(results.get("difference", ""))
    ET.SubElement(comparison, "PercentDifference").text = str(results.get("percent_difference", ""))

    bayesian = ET.SubElement(root, "Bayesian")
    ET.SubElement(bayesian, "PosteriorMean").text = str(results.get("posterior_mean", ""))
    ET.SubElement(bayesian, "PosteriorStd").text = str(results.get("posterior_std", ""))
    ET.SubElement(bayesian, "CredibleLower").text = str(results.get("credible_lower", ""))
    ET.SubElement(bayesian, "CredibleUpper").text = str(results.get("credible_upper", ""))

    remarks = ET.SubElement(root, "Remarks")
    remarks.text = results.get("remarks", "")

    dsi = ET.SubElement(root, "DSI")
    ET.SubElement(dsi, "Quantity").text = results.get("quantity", "")
    ET.SubElement(dsi, "MeasuredValue").text = str(results.get("mean", ""))
    ET.SubElement(dsi, "ExpandedUncertainty").text = str(results.get("expanded", ""))
    ET.SubElement(dsi, "CoverageFactor").text = str(results.get("coverage_factor", ""))
    ET.SubElement(dsi, "Unit").text = results.get("resolution_unit", "")
    ET.SubElement(dsi, "Symbol").text = results.get("resolution_unit", "")

    signature_section = ET.SubElement(root, "DigitalSignature")
    ET.SubElement(signature_section, "Algorithm").text = "RSA-SHA256"
    ET.SubElement(signature_section, "SignatureValue").text = "Pending"

    xml_content = ET.tostring(root, encoding="unicode")

    signature = sign_data(xml_content)
    signature_section.find("SignatureValue").text = signature[:32] + "..."

    xml_content = ET.tostring(root, encoding="unicode")

    xml_path = os.path.join(GENERATED_FOLDER, "certificate.xml")
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0"?>\n')
        f.write('<?xml-stylesheet type="text/xsl" href="certificate.xsl"?>\n')
        f.write(xml_content)

    return xml_path


def generate_xslt():
    xslt = """<?xml version="1.0"?>
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
"""

    with open(os.path.join(GENERATED_FOLDER, "certificate.xsl"), "w", encoding="utf-8") as f:
        f.write(xslt)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/excel_meta", methods=["POST"])
def excel_meta():
    file = request.files.get("excel")
    sheet_name = request.form.get("sheet_name")

    if file is None:
        return jsonify({"sheets": [], "columns": []})

    try:
        xls = pd.ExcelFile(file)
        sheets = xls.sheet_names
        columns = []

        if sheet_name in sheets:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            columns = [str(col) for col in df.columns]
        elif sheets:
            df = pd.read_excel(xls, sheet_name=sheets[0])
            columns = [str(col) for col in df.columns]

        return jsonify({"sheets": sheets, "columns": columns})
    except Exception:
        return jsonify({"sheets": [], "columns": []})


@app.route("/calculate", methods=["POST"])
def calculate():
    file = request.files["excel"]

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    sheet_name = request.form.get("sheet_name")
    column_name = request.form.get("column_name")

    if sheet_name:
        df = pd.read_excel(path, sheet_name=sheet_name)
    else:
        df = pd.read_excel(path)

    if column_name:
        readings = df[column_name].dropna().values
    else:
        readings = df.iloc[:, 0].dropna().values

    n = len(readings)
    mean = np.mean(readings)
    std = np.std(readings, ddof=1)
    type_a = std / np.sqrt(n)

    certificate_number = request.form["certificate_number"]
    customer_name = request.form["customer_name"]
    organization = request.form.get("organization", "")
    instrument_name = request.form["instrument_name"]
    instrument_id = request.form["instrument_id"]
    manufacturer = request.form.get("manufacturer", "")
    model_number = request.form.get("model_number", "")
    serial_number = request.form.get("serial_number", "")
    calibration_date = request.form.get("calibration_date", "")
    ambient_temperature = request.form.get("ambient_temperature", "")
    humidity = request.form.get("humidity", "")
    remarks = request.form.get("remarks", "")

    # Validate numeric inputs and provide a clear error if invalid
    def parse_float(field_name, default=0.0):
        val = request.form.get(field_name, "")
        try:
            return float(val)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid numeric value for '{field_name}': '{val}'")

    try:
        resolution = parse_float("resolution")
        calibration = parse_float("calibration")
        drift = parse_float("drift")
        temperature = parse_float("temperature")
    except ValueError as e:
        # Return a simple error page so user can correct the input
        return (f"<h3>Input error</h3><p>{str(e)}</p>"), 400

    resolution_unit = request.form.get("resolution_unit", "")
    calibration_unit = request.form.get("calibration_unit", "")
    drift_unit = request.form.get("drift_unit", "")
    temperature_unit = request.form.get("temperature_unit", "")

    quantity = request.form.get("quantity", "")
    confidence = int(request.form.get("confidence", 95))

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

    type_b = np.sqrt(u_res**2 + u_cal**2 + u_drift**2 + u_temp**2)
    combined = np.sqrt(type_a**2 + type_b**2)
    expanded = k * combined

    # Monte Carlo
    N = 100000
    res_samples = np.random.uniform(-resolution / 2, resolution / 2, N)
    cal_samples = np.random.normal(0, calibration / k, N)
    drift_samples = np.random.uniform(-drift, drift, N)
    temp_samples = np.random.uniform(-temperature, temperature, N)

    mc_results = mean + res_samples + cal_samples + drift_samples + temp_samples
    mc_mean = np.mean(mc_results)
    mc_std = np.std(mc_results)
    mc_expanded = k * mc_std

    # Bayesian
    prior_mean = mean
    prior_std = combined
    sample_mean = mean
    sample_std = std
    likelihood_var = (sample_std ** 2) / n
    prior_var = prior_std ** 2
    posterior_var = 1 / ((1 / prior_var) + (1 / likelihood_var))
    posterior_mean = posterior_var * ((prior_mean / prior_var) + (sample_mean / likelihood_var))
    posterior_std = np.sqrt(posterior_var)
    lower95 = posterior_mean - (1.96 * posterior_std)
    upper95 = posterior_mean + (1.96 * posterior_std)

    x = np.linspace(posterior_mean - 5 * posterior_std, posterior_mean + 5 * posterior_std, 1000)
    prior_pdf = norm.pdf(x, prior_mean, prior_std)
    likelihood_pdf = norm.pdf(x, sample_mean, np.sqrt(likelihood_var))
    posterior_pdf = norm.pdf(x, posterior_mean, posterior_std)

    plt.figure(figsize=(8, 5))
    plt.plot(x, prior_pdf, label="Prior")
    plt.plot(x, likelihood_pdf, label="Likelihood")
    plt.plot(x, posterior_pdf, label="Posterior")
    plt.xlabel("Measured Value")
    plt.ylabel("Probability Density")
    plt.title("Bayesian Inference")
    plt.legend()
    plt.grid(True)
    bayes_graph = os.path.join("static", "bayesian_graph.png")
    plt.savefig(bayes_graph, bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.hist(mc_results, bins=50, density=True, alpha=0.7, color="tab:blue", edgecolor="black", label="MC results")
    plt.axvline(mc_mean, color="red", linestyle="--", label="MC mean")
    plt.xlabel("Simulated Value")
    plt.ylabel("Density")
    plt.title("Monte Carlo Histogram")
    plt.legend()
    plt.grid(True)
    mc_hist_path = os.path.join("static", "mc_histogram.png")
    plt.savefig(mc_hist_path, bbox_inches="tight")
    plt.close()

    difference = abs(expanded - mc_expanded)
    percent_difference = (difference / expanded) * 100 if expanded != 0 else 0

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
        "bayesian_graph": "bayesian_graph.png",
        "difference": round(difference, 8),
        "percent_difference": round(percent_difference, 3),
    }

    generate_xml(results)
    generate_xslt()

    return render_template("result.html", results=results)


@app.route("/download/xml")
def download_xml():
    return send_from_directory(GENERATED_FOLDER, "certificate.xml", as_attachment=True)


@app.route("/download/xslt")
def download_xslt():
    return send_from_directory(GENERATED_FOLDER, "certificate.xsl", as_attachment=True)


@app.route("/view/certificate")
def view_certificate():
    xml_path = os.path.join(GENERATED_FOLDER, "certificate.xml")
    # Apply XSLT server-side and return HTML so browsers always show the certificate
    xml_path = os.path.join(GENERATED_FOLDER, "certificate.xml")
    xslt_path = os.path.join(GENERATED_FOLDER, "certificate.xsl")

    try:
        with open(xml_path, "rb") as xf, open(xslt_path, "rb") as sf:
            xml_doc = etree.parse(xf)
            xslt_doc = etree.parse(sf)
            transformer = etree.XSLT(xslt_doc)
            html_doc = transformer(xml_doc)
            html_string = etree.tostring(html_doc, encoding="unicode", method="html")

        return html_string, 200, {"Content-Type": "text/html; charset=utf-8"}
    except Exception:
        # Fallback to raw XML if transform fails
        try:
            with open(xml_path, "r", encoding="utf-8") as f:
                xml_content = f.read()
            return xml_content, 200, {"Content-Type": "application/xml; charset=utf-8"}
        except Exception as e:
            return (f"<h3>Error</h3><p>Unable to load certificate: {e}</p>"), 500


@app.route("/view/xslt")
def view_xslt():
    # Serve the XSLT with a stylesheet MIME type so browsers apply it
    xslt_path = os.path.join(GENERATED_FOLDER, "certificate.xsl")
    return send_file(xslt_path, mimetype="text/xsl")


@app.route("/download/pdf")
def download_pdf():
    xml_path = os.path.join(GENERATED_FOLDER, "certificate.xml")
    xslt_path = os.path.join(GENERATED_FOLDER, "certificate.xsl")

    with open(xml_path, "rb") as xml_file:
        xml_doc = etree.parse(xml_file)

    with open(xslt_path, "rb") as xslt_file:
        xslt_doc = etree.parse(xslt_file)

    xslt_transformer = etree.XSLT(xslt_doc)
    html_doc = xslt_transformer(xml_doc)
    html_string = etree.tostring(html_doc, encoding="unicode")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    from html.parser import HTMLParser

    class TextExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.text = []

        def handle_data(self, data):
            if data.strip():
                self.text.append(data.strip())

    extractor = TextExtractor()
    extractor.feed(html_string)

    for line in extractor.text[:100]:
        try:
            pdf.cell(0, 10, txt=line[:200], ln=True)
        except:
            pass

    pdf_buffer = BytesIO()
    pdf_bytes = pdf.output()
    pdf_buffer.write(pdf_bytes)
    pdf_buffer.seek(0)

    return send_file(pdf_buffer, mimetype="application/pdf", as_attachment=True, download_name="certificate.pdf")


if __name__ == "__main__":
    app.run(debug=True)
