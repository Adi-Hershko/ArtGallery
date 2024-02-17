import React, { useState, useEffect } from 'react';
import AWS from 'aws-sdk';

// Configure AWS SDK with your credentials
AWS.config.update({
  accessKeyId: 'YOUR_ACCESS_KEY_ID',
  secretAccessKey: 'YOUR_SECRET_ACCESS_KEY',
  region: 'YOUR_REGION' // e.g., 'us-east-1'
});

const s3 = new AWS.S3();