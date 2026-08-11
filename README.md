# 🎲 Jogar Dado - AWS Lambda

Função serverless em Python que simula o lançamento de um dado (1-6), exposta via HTTP com AWS Lambda Function URL.

## Stack
- Python 3.12
- AWS Lambda
- Function URL (auth: AWS_IAM)

## Como funciona

`dado.py` recebe um evento do Lambda, sorteia um número de 1 a 6 e retorna:

```json
{"statusCode": 200, "body": "{\"resultado\": 4}"}
```

## Deploy

```bash
# 1. Empacotar
zip -j function.zip dado.py

# 2. Criar a função (troque o ARN pela sua role)
aws lambda create-function \
  --function-name jogar-dado \
  --runtime python3.12 \
  --handler dado.handler \
  --zip-file fileb://function.zip \
  --role <ARN_DA_ROLE>

# 3. Criar a Function URL
aws lambda create-function-url-config \
  --function-name jogar-dado \
  --auth-type AWS_IAM

# 4. Dar permissão de invocação
aws lambda add-permission \
  --function-name jogar-dado \
  --statement-id AllowMyUserInvoke \
  --action lambda:InvokeFunctionUrl \
  --principal "<SEU_ARN>" \
  --function-url-auth-type AWS_IAM
```

## Como testar

![Console AWS:](assets/teste-console.png)

**Console AWS:** Lambda → Functions → `jogar-dado` → aba Test → Create new event → Test

![CLI AWS:](assets/test-cli.png)

**CLI (invoke direto):** ```bash aws lambda invoke --function-name jogar-dado --payload '{}' \
  --cli-binary-format raw-in-base64-out response.json
cat response.json
```

**CLI (via HTTP assinado):**
```bash
FUNCTION_URL=$(aws lambda get-function-url-config --function-name jogar-dado --query "FunctionUrl" --output text)
curl "$FUNCTION_URL" \
  --user "$(aws configure get aws_access_key_id):$(aws configure get aws_secret_access_key)" \
  --aws-sigv4 "aws:amz:us-east-1:lambda"
```

## Atualizar o código

```bash
zip -j function.zip dado.py
aws lambda update-function-code --function-name jogar-dado --zip-file fileb://function.zip
```

## Por que AWS_IAM em vez de acesso público?

O ambiente de laboratório (AWS Academy/Vocareum) bloqueia acesso anônimo via política de organização, mesmo com a permissão de recurso liberada. `AWS_IAM` exige requisição assinada e contorna essa restrição.
