# Digital Calibration Certificate (DCC) Software

## Overview

This project is a web-based Digital Calibration Certificate (DCC) generation and uncertainty analysis software developed using Python and Flask. The application enables users to upload measurement data from Excel files, perform uncertainty evaluation, generate machine-readable calibration certificates in XML format, and visualize statistical analysis results.

The software has been developed as part of a project at the Impedance Laboratory, CSIR-National Physical Laboratory (NPL), New Delhi.

---

## Features

### Data Import

* Upload measurement data from Excel files (.xlsx)
* Sheet selection from multi-sheet Excel workbooks
* Column selection for measurement data extraction

### Uncertainty Analysis

* Type A uncertainty evaluation
* Type B uncertainty evaluation
* Combined standard uncertainty calculation
* Expanded uncertainty calculation
* User-selectable confidence levels (90%, 95%, 99%)

### Monte Carlo Simulation

* Monte Carlo uncertainty propagation
* Monte Carlo expanded uncertainty estimation
* Comparison between GUM and Monte Carlo results
* Monte Carlo histogram visualization

### Bayesian Inference

* Posterior mean estimation
* Posterior standard deviation estimation
* Credible interval calculation
* Bayesian probability distribution graph generation

### Digital Calibration Certificate

* XML-based machine-readable certificate generation
* XSLT-based human-readable certificate rendering
* Certificate metadata management
* Customer and instrument information storage

### D-SI Metadata Support

* Measurement quantity information
* Measurement value and unit metadata
* Expanded uncertainty metadata
* Coverage factor metadata

### Digital Signature

* RSA-SHA256 based digital signature generation
* Certificate integrity verification support
* Public and private key infrastructure using PEM files

---

## Technologies Used

* Python
* Flask
* Pandas
* NumPy
* SciPy
* Matplotlib
* XML / XSLT
* Cryptography Library (RSA Digital Signatures)

---

## Project Structure

```text
uncertainty_dcc_app/

├── app.py
├── generate_keys.py
├── private_key.pem
├── public_key.pem

├── uploads/
├── generated/

├── templates/
│   ├── index.html
│   └── result.html

├── static/
│   ├── style.css
│   ├── bayesian_graph.png
│   └── monte_carlo_histogram.png

├── requirements.txt
└── README.md
```

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd uncertainty_dcc_app
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Generate RSA Keys

```bash
python generate_keys.py
```

### Run Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

in your web browser.

---

## Workflow

1. Upload Excel measurement data.
2. Select worksheet and measurement column.
3. Enter Type B uncertainty parameters.
4. Select confidence level.
5. Perform uncertainty analysis.
6. Generate Monte Carlo simulation results.
7. Generate Bayesian inference results.
8. Generate Digital Calibration Certificate.
9. Download XML and XSLT certificate files.

---

## Generated Outputs

The software generates:

* Statistical Analysis Results
* Type A and Type B Uncertainty
* Combined and Expanded Uncertainty
* Monte Carlo Analysis Results
* Bayesian Analysis Results
* Digital Calibration Certificate (XML)
* Human Readable Certificate (XSLT)
* Digital Signature Information

---

## Future Scope

* PDF certificate generation
* Digital signature verification module
* Database integration
* Laboratory Information Management System (LIMS) integration
* Environmental sensor integration
* Advanced D-SI metadata implementation
* Multi-user authentication and access control

---

## Author

Khushi

Intern, Impedance Laboratory

CSIR – National Physical Laboratory (NPL), New Delhi

---

## Disclaimer

This software is intended for research, educational, and laboratory workflow automation purposes. Users should validate all measurement results and uncertainty calculations before using them in official calibration reports.
