#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { MedDigtwinStack } from '../lib/meddigtwin-stack';

const app = new cdk.App();

new MedDigtwinStack(app, 'MedDigtwinStack', {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION || 'us-east-1'
  },
});
