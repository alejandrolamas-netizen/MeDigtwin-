import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as elbv2 from 'aws-cdk-lib/aws-elasticloadbalancingv2';
import * as acm from 'aws-cdk-lib/aws-certificatemanager';
import * as wafv2 from 'aws-cdk-lib/aws-wafv2';
import * as cognito from 'aws-cdk-lib/aws-cognito';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

export class MedDigtwinStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, 'MedDigtwinVpc', {
      maxAzs: 2,
      natGateways: 1,
      ipAddresses: ec2.IpAddresses.cidr('10.40.0.0/16'),
    });

    const repository = new ecr.Repository(this, 'MedDigtwinApiRepository', {
      repositoryName: 'meddigtwin-api',
      imageScanOnPush: true,
      encryption: ecr.RepositoryEncryption.AES_256,
      lifecycleRules: [{ maxImageCount: 10 }],
      removalPolicy: cdk.RemovalPolicy.RETAIN,
    });

    const userPool = new cognito.UserPool(this, 'MedDigtwinUserPool', {
      userPoolName: 'meddigtwin-users',
      selfSignUpEnabled: false,
      signInAliases: { email: true },
      standardAttributes: { email: { required: true, mutable: false } },
      customAttributes: {
        tenant_id: new cognito.StringAttribute({ mutable: false }),
        role: new cognito.StringAttribute({ mutable: true }),
      },
      passwordPolicy: {
        minLength: 12,
        requireLowercase: true,
        requireUppercase: true,
        requireDigits: true,
        requireSymbols: true,
      },
      removalPolicy: cdk.RemovalPolicy.RETAIN,
    });

    const userPoolClient = userPool.addClient('MedDigtwinWebClient', {
      generateSecret: false,
      authFlows: { userPassword: true, userSrp: true },
    });

    const simulationsTable = new dynamodb.Table(this, 'MedDigtwinSimulationsTable', {
      tableName: 'meddigtwin-simulations',
      partitionKey: { name: 'tenant_id', type: dynamodb.AttributeType.STRING },
      sortKey: { name: 'simulation_key', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      encryption: dynamodb.TableEncryption.AWS_MANAGED,
      pointInTimeRecovery: true,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
    });

    const auditTable = new dynamodb.Table(this, 'MedDigtwinAuditTable', {
      tableName: 'meddigtwin-audit',
      partitionKey: { name: 'tenant_id', type: dynamodb.AttributeType.STRING },
      sortKey: { name: 'event_key', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      encryption: dynamodb.TableEncryption.AWS_MANAGED,
      pointInTimeRecovery: true,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
    });

    const environment = (this.node.tryGetContext('environment') as string) || 'demo';

    const cluster = new ecs.Cluster(this, 'MedDigtwinCluster', {
      vpc,
      containerInsights: true,
    });

    const logGroup = new logs.LogGroup(this, 'MedDigtwinApiLogs', {
      retention: logs.RetentionDays.ONE_MONTH,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
    });

    const taskRole = new iam.Role(this, 'MedDigtwinTaskRole', {
      assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
    });

    const executionRole = new iam.Role(this, 'MedDigtwinExecutionRole', {
      assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonECSTaskExecutionRolePolicy'),
      ],
    });

    const taskDefinition = new ecs.FargateTaskDefinition(this, 'MedDigtwinTaskDefinition', {
      family: 'meddigtwin-api',
      cpu: 512,
      memoryLimitMiB: 1024,
      executionRole,
      taskRole,
    });

    taskDefinition.addContainer('Api', {
      image: ecs.ContainerImage.fromEcrRepository(repository, 'latest'),
      logging: ecs.LogDrivers.awsLogs({ streamPrefix: 'meddigtwin-api', logGroup }),
      environment: {
        ENVIRONMENT: environment,
        SYNTHETIC_DATA_ONLY: 'true',
        OIDC_ISSUER: cdk.Fn.sub('https://cognito-idp.${AWS::Region}.amazonaws.com/${UserPoolId}'),
        OIDC_AUDIENCE: userPoolClient.userPoolClientId,
        OIDC_JWKS_URL: cdk.Fn.sub('https://cognito-idp.${AWS::Region}.amazonaws.com/${UserPoolId}/.well-known/jwks.json'),
        DDB_SIMULATIONS_TABLE: simulationsTable.tableName,
        DDB_AUDIT_TABLE: auditTable.tableName,
        AWS_REGION: cdk.Aws.REGION,
        AWS_DEFAULT_REGION: cdk.Aws.REGION,
      },
      portMappings: [{ containerPort: 8000 }],
      healthCheck: {
        command: ['CMD-SHELL', "python -c \"import urllib.request; urllib.request.urlopen('http://localhost:8000/health')\""],
        interval: cdk.Duration.seconds(30),
        timeout: cdk.Duration.seconds(5),
        retries: 3,
        startPeriod: cdk.Duration.seconds(20),
      },
    });

    simulationsTable.grantReadWriteData(taskRole);
    auditTable.grantReadWriteData(taskRole);

    const service = new ecs.FargateService(this, 'MedDigtwinApiService', {
      cluster,
      taskDefinition,
      desiredCount: 0,
      assignPublicIp: false,
      minHealthyPercent: 100,
      maxHealthyPercent: 200,
      circuitBreaker: { rollback: true },
    });

    const alb = new elbv2.ApplicationLoadBalancer(this, 'MedDigtwinAlb', {
      vpc,
      internetFacing: true,
    });

    const certificateArn = this.node.tryGetContext('certificateArn') as string | undefined;
    const domainName = this.node.tryGetContext('domainName') as string | undefined;

    const httpListener = alb.addListener('HttpListener', {
      port: 80,
      open: true,
    });

    if (certificateArn) {
      const certificate = acm.Certificate.fromCertificateArn(this, 'MedDigtwinCertificate', certificateArn);
      const httpsListener = alb.addListener('HttpsListener', {
        port: 443,
        certificates: [certificate],
        open: true,
      });
      httpsListener.addTargets('ApiTargetHttps', {
        port: 8000,
        targets: [service],
        healthCheck: { path: '/health', healthyHttpCodes: '200' },
      });
      httpListener.addAction('RedirectToHttps', {
        action: elbv2.ListenerAction.redirect({
          protocol: 'HTTPS',
          port: '443',
          permanent: true,
        }),
      });
    } else {
      httpListener.addTargets('ApiTarget', {
        port: 8000,
        targets: [service],
        healthCheck: { path: '/health', healthyHttpCodes: '200' },
      });
    }

    const webAcl = new wafv2.CfnWebACL(this, 'MedDigtwinWebAcl', {
      name: 'meddigtwin-web-acl',
      scope: 'REGIONAL',
      defaultAction: { allow: {} },
      visibilityConfig: {
        cloudWatchMetricsEnabled: true,
        metricName: 'meddigtwin-web-acl',
        sampledRequestsEnabled: true,
      },
      rules: [{
        name: 'AWSManagedCommonRules',
        priority: 0,
        overrideAction: { none: {} },
        statement: {
          managedRuleGroupStatement: {
            vendorName: 'AWS',
            name: 'AWSManagedRulesCommonRuleSet',
          },
        },
        visibilityConfig: {
          cloudWatchMetricsEnabled: true,
          metricName: 'meddigtwin-common-rules',
          sampledRequestsEnabled: true,
        },
      }],
    });

    new wafv2.CfnWebACLAssociation(this, 'MedDigtwinWebAclAssociation', {
      resourceArn: alb.loadBalancerArn,
      webAclArn: webAcl.attrArn,
    });

    if (domainName) {
      new cdk.CfnOutput(this, 'ConfiguredDomain', { value: domainName });
    }

    new cdk.CfnOutput(this, 'UserPoolId', { value: userPool.userPoolId });
    new cdk.CfnOutput(this, 'UserPoolClientId', { value: userPoolClient.userPoolClientId });

    new cdk.CfnOutput(this, 'ApiUrl', {
      value: certificateArn
        ? (domainName ? 'https://' + domainName : 'https://' + alb.loadBalancerDnsName)
        : 'http://' + alb.loadBalancerDnsName,
    });

    new cdk.CfnOutput(this, 'EcrRepositoryUri', {
      value: repository.repositoryUri,
    });
  }
}
