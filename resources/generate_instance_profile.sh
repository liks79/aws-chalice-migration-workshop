wget https://raw.githubusercontent.com/liks79/aws-chalice-migration-workshop/master/resources/workshop-cloud9-instance-profile-role-trust.json
wget https://raw.githubusercontent.com/liks79/aws-chalice-migration-workshop/master/resources/workshop-cloud9-policy.json

PARN=$(aws iam create-policy --policy-name workshop-cloud9-policy --policy-document file://workshop-cloud9-policy.json --query "Policy.Arn" --output text)
aws iam create-role --role-name workshop-cloud9-instance-profile-role --assume-role-policy-document file://workshop-cloud9-instance-profile-role-trust.json
aws iam attach-role-policy --role-name workshop-cloud9-instance-profile-role --policy-arn $PARN
aws iam create-instance-profile --instance-profile-name workshop-cloud9-instance-profile
aws iam add-role-to-instance-profile --role-name workshop-cloud9-instance-profile-role --instance-profile-name workshop-cloud9-instance-profile
