# MedDigtwin

## Healthcare Operational Digital Twin

**MedDigtwin by EmergentSoft** is an AWS-ready healthcare operational digital twin for observing, modeling and simulating hospital capacity, patient flow, workforce and operational constraints. The current environment uses synthetic data.

### Core capabilities

- Operational digital twin topology
- Synthetic healthcare baseline
- Patient-demand simulation
- Workforce / nursing availability modeling
- ICU and bed-capacity modeling
- Laboratory throughput modeling
- What-if scenarios
- Bottleneck analysis
- 24-hour operational horizon
- Presentation / demo mode
- NVIDIA + AWS reference architecture

## Security

Security is a first-class requirement for MedDigtwin.

### Repository security

- **Do not commit secrets, credentials, API keys, private certificates, tokens or production patient data.**
- Use environment variables or an approved secret-management service for credentials when backend services are introduced.
- Keep synthetic/demo data separate from any future production datasets.
- Review dependencies and third-party services before production deployment.
- Use least-privilege IAM/RBAC policies for AWS, application services and future integrations.
- Protect production branches with required reviews, status checks and controlled write access.
- Enable GitHub secret scanning, push protection and Dependabot/security alerts where available.
- Record security-relevant architectural and operational decisions in version control.
- Report suspected vulnerabilities privately rather than publishing exploit details in an issue.

### Healthcare data security

MedDigtwin currently uses **synthetic healthcare data**. Any future integration with real healthcare information must be subject to an appropriate privacy, security, compliance and data-governance review before use.

The project must not be treated as authorization to upload, process or expose patient-identifiable information. Future deployments should define applicable legal/regulatory requirements, data classification, retention, access controls, encryption, audit logging, incident response and vendor responsibilities.

### Security boundary

The current product is AWS-ready, but AWS-ready does not mean production healthcare compliance, clinical validation, regulatory certification or authorization to process regulated health information.

## Ownership & intellectual property

**MedDigtwin is a product/project of EmergentSoft Corporation.**

Copyright © 2026 EmergentSoft Corporation. All rights reserved, unless a specific file, dependency or third-party component states otherwise.

The **MedDigtwin** name, product concept, original source code, architecture, documentation, interface design and related original materials in this repository are proprietary to EmergentSoft Corporation unless explicitly identified as third-party material.

No license to copy, modify, distribute, sublicense, commercialize, resell or create derivative works from the proprietary project materials is granted by merely accessing this repository.

Third-party trademarks and technologies mentioned in this repository, including NVIDIA and AWS products, remain the property of their respective owners. Their mention does not imply ownership, partnership, sponsorship, certification or endorsement unless separately documented.

For commercial licensing, partnership or authorized use, contact **EmergentSoft Corporation** through the official company channels.

## Technology reference

The prototype maps relevant building blocks from:

**NVIDIA**
- CUDA
- TensorRT
- Triton Inference Server
- NVIDIA NIM
- NGC
- NVIDIA AI Enterprise
- Omniverse / OpenUSD
- Modulus
- RAPIDS / cuDF
- NeMo

**AWS**
- EC2 / GPU compute
- EKS / ECS
- Lambda
- S3
- Kinesis
- EventBridge
- IoT Core / IoT TwinMaker
- OpenSearch
- Bedrock
- SageMaker
- Step Functions
- CloudWatch
- IAM / KMS

These are architecture references. Their presence in the prototype does not by itself represent deployment, formal co-development, sponsorship, certification or endorsement.

## Safety boundary

MedDigtwin is an operational simulation prototype using synthetic data. It is **not a clinical decision-making system** and does not replace qualified clinical judgment.

## Run

Open `index.html` in a modern browser. No build step is required.

## Commercial readiness

MedDigtwin is the first EmergentSoft product formally presented as AWS-ready.

The repository includes AWS CDK infrastructure, ECS/Fargate deployment automation, Cognito identity, DynamoDB persistence, audit logging, WAF support and a commercial launch package.

Current commercial offer: enterprise pilot / custom quotation.

## Product roadmap

EmergentSoft can evolve MedDigtwin toward:

1. Verified production AWS deployment
2. Real hospital data connectors after separate governance review
3. Event-driven operational state synchronization
4. NVIDIA-accelerated simulation and inference
5. Digital-world visualization
6. Agentic operational analysis
7. Governance, auditability and human approval workflows

**EmergentSoft — Intelligent infrastructure · Digital workforce**
