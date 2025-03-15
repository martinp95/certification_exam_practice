-- Insert the AWS Cloud Practitioner certification
INSERT INTO certifications (id, name, description)
VALUES (
  uuid_generate_v4(),
  'AWS Cloud Practitioner',
  'AWS Cloud Practitioner certification exam for cloud fundamentals and AWS basics.'
);

-- Insert 20 questions associated with the certification.
-- Using a CTE to retrieve the certification id by its name.
WITH cert AS (
  SELECT id FROM certifications WHERE name = 'AWS Cloud Practitioner'
)
INSERT INTO questions (id, certification_id, question_text, question_type, answer_choices, correct_answer)
VALUES 
  -- 1. Single Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'What is the AWS Cloud Practitioner certification?',
    'single_choice',
    '{"A": "An entry-level exam validating basic understanding of the AWS Cloud", "B": "A professional-level exam", "C": "An architect-level exam", "D": "A developer-level exam"}',
    '{"answer": "A"}'
  ),
  -- 2. Multiple Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'Which AWS services are used for computing?',
    'multiple_choice',
    '{"A": "Amazon EC2", "B": "AWS Lambda", "C": "Amazon S3", "D": "Amazon Lightsail"}',
    '{"answers": ["A", "B", "D"]}'
  ),
  -- 3. Single Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'Which AWS service provides scalable object storage?',
    'single_choice',
    '{"A": "Amazon S3", "B": "Amazon EC2", "C": "Amazon RDS", "D": "Amazon VPC"}',
    '{"answer": "A"}'
  ),
  -- 4. Multiple Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'Which of the following AWS services offer database solutions?',
    'multiple_choice',
    '{"A": "Amazon RDS", "B": "Amazon DynamoDB", "C": "Amazon EC2", "D": "Amazon Redshift"}',
    '{"answers": ["A", "B", "D"]}'
  ),
  -- 5. Single Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'What does AWS stand for?',
    'single_choice',
    '{"A": "Amazon Web Services", "B": "Advanced Web Solutions", "C": "Automated Web Systems", "D": "Amazon Workflow Service"}',
    '{"answer": "A"}'
  ),
  -- 6. Multiple Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'Which AWS services are serverless?',
    'multiple_choice',
    '{"A": "AWS Lambda", "B": "Amazon EC2", "C": "AWS Fargate", "D": "AWS Batch"}',
    '{"answers": ["A", "C"]}'
  ),
  -- 7. Single Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'Which AWS service is primarily used for content delivery?',
    'single_choice',
    '{"A": "Amazon CloudFront", "B": "Amazon Route 53", "C": "Amazon S3", "D": "AWS Direct Connect"}',
    '{"answer": "A"}'
  ),
  -- 8. Multiple Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'Which of the following are AWS security services?',
    'multiple_choice',
    '{"A": "AWS IAM", "B": "AWS KMS", "C": "Amazon S3", "D": "AWS Shield"}',
    '{"answers": ["A", "B", "D"]}'
  ),
  -- 9. Single Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'Which AWS service is a fully managed NoSQL database?',
    'single_choice',
    '{"A": "Amazon DynamoDB", "B": "Amazon Aurora", "C": "Amazon Redshift", "D": "Amazon RDS"}',
    '{"answer": "A"}'
  ),
  -- 10. Multiple Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'Which AWS services provide monitoring and logging functionalities?',
    'multiple_choice',
    '{"A": "Amazon CloudWatch", "B": "AWS CloudTrail", "C": "Amazon S3", "D": "AWS Config"}',
    '{"answers": ["A", "B", "D"]}'
  ),
  -- 11. Single Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'What is the primary benefit of using AWS Lambda?',
    'single_choice',
    '{"A": "No server management", "B": "Manual scaling", "C": "High cost", "D": "Fixed infrastructure"}',
    '{"answer": "A"}'
  ),
  -- 12. Multiple Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'Which AWS services can help with infrastructure as code?',
    'multiple_choice',
    '{"A": "AWS CloudFormation", "B": "AWS OpsWorks", "C": "AWS Config", "D": "Amazon EC2"}',
    '{"answers": ["A", "B"]}'
  ),
  -- 13. Single Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'Which service is used for domain name registration in AWS?',
    'single_choice',
    '{"A": "Amazon CloudFront", "B": "AWS Route 53", "C": "Amazon S3", "D": "AWS IAM"}',
    '{"answer": "B"}'
  ),
  -- 14. Multiple Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'Which AWS services are commonly used for analytics?',
    'multiple_choice',
    '{"A": "Amazon Redshift", "B": "Amazon QuickSight", "C": "Amazon DynamoDB", "D": "AWS Glue"}',
    '{"answers": ["A", "B", "D"]}'
  ),
  -- 15. Single Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'What does VPC stand for in AWS?',
    'single_choice',
    '{"A": "Virtual Private Cloud", "B": "Virtual Public Cloud", "C": "Virtual Private Connection", "D": "Virtual Proxy Cloud"}',
    '{"answer": "A"}'
  ),
  -- 16. Multiple Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'Which AWS services can be used for container management?',
    'multiple_choice',
    '{"A": "Amazon ECS", "B": "Amazon EKS", "C": "AWS Fargate", "D": "AWS Lambda"}',
    '{"answers": ["A", "B", "C"]}'
  ),
  -- 17. Single Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'Which service is primarily used for object storage with archival capabilities?',
    'single_choice',
    '{"A": "Amazon S3 Glacier", "B": "Amazon S3 Standard", "C": "Amazon EBS", "D": "Amazon EC2"}',
    '{"answer": "A"}'
  ),
  -- 18. Multiple Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'Which services are part of AWS’s machine learning offerings?',
    'multiple_choice',
    '{"A": "Amazon SageMaker", "B": "AWS DeepLens", "C": "Amazon Rekognition", "D": "Amazon VPC"}',
    '{"answers": ["A", "B", "C"]}'
  ),
  -- 19. Single Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'Which AWS service helps manage user identities and permissions?',
    'single_choice',
    '{"A": "AWS IAM", "B": "Amazon EC2", "C": "Amazon RDS", "D": "AWS CloudFormation"}',
    '{"answer": "A"}'
  ),
  -- 20. Multiple Choice
  (
    uuid_generate_v4(),
    (SELECT id FROM cert),
    'Which of the following AWS services are used for data migration?',
    'multiple_choice',
    '{"A": "AWS Snowball", "B": "AWS Database Migration Service", "C": "Amazon S3", "D": "Amazon CloudWatch"}',
    '{"answers": ["A", "B"]}'
  );

commit;