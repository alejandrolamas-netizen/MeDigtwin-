# MedDigtwin — AWS-ready product announcement

## First AWS-ready product officially presented by EmergentSoft

**MedDigtwin** is the first EmergentSoft product to be formally presented as an **AWS-ready healthcare operational digital twin**.

**Product:** MedDigtwin  
**Company:** EmergentSoft Corporation  
**Category:** Healthcare Operational Digital Twin  
**Data posture:** Synthetic healthcare operations data  
**Deployment target:** AWS  
**Product status:** AWS-ready architecture and deployment automation prepared; production deployment status must be verified independently before claiming live availability.

### What AWS-ready means

MedDigtwin has been engineered around an AWS deployment path that includes:

- AWS CDK / CloudFormation
- Amazon ECR for container images
- Amazon ECS with AWS Fargate
- Application Load Balancer
- Amazon Cognito for application identity
- Amazon DynamoDB for simulation and audit persistence
- Amazon CloudWatch for observability
- IAM least-privilege roles
- AWS KMS-compatible encryption architecture
- GitHub Actions with AWS OIDC for CI/CD
- Optional ACM HTTPS and AWS WAF hardening

### Product proposition

MedDigtwin enables healthcare organizations to **observe, model, simulate and anticipate operational conditions** before implementing operational changes.

The initial synthetic environment models emergency demand, patient flow, inpatient beds, ICU capacity, nursing availability, operating rooms, laboratory throughput, operational bottlenecks and what-if scenarios.

### Operational workflow

**Observe → Model → Simulate → Anticipate → Decide**

MedDigtwin is focused on operational simulation and decision support. It does not provide diagnosis or treatment recommendations and is not a clinical decision-making system.

### AWS and NVIDIA positioning

AWS provides the cloud infrastructure path for the product. NVIDIA technologies are referenced as an acceleration path for future simulation, inference and digital-world capabilities.

References to AWS, NVIDIA or other third-party technologies do not imply sponsorship, certification, endorsement or formal co-development unless separately documented.

### Healthcare data boundary

The current product uses synthetic data.

Real healthcare information, including patient-identifiable or regulated health information, must not be introduced into the current prototype without a separate privacy, security, compliance, data-governance and deployment assessment.

## Official statement

> **MedDigtwin is the first EmergentSoft product formally presented as AWS-ready, establishing the company's initial cloud deployment reference architecture for operational digital twins in healthcare.**

This statement describes the product's engineering and presentation status. It does not claim AWS endorsement, certification, Marketplace publication or production deployment unless those milestones are separately verified.

---

**EmergentSoft Corporation**  
*Intelligent infrastructure · Digital workforce*  
*Make the enterprise operable by AI.*
