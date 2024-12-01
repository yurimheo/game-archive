#!/bin/bash

# 공통 리소스 디렉토리
COMMON_TEMPLATES="gateway/app/templates"
COMMON_STATIC="gateway/app/static"

# 서비스 리스트
SERVICES=("auth-service" "discount-service" "qa-service" "news-service" "timed-deal-service")

# 각 서비스에 복사
for SERVICE in "${SERVICES[@]}"; do
    echo "Copying templates to $SERVICE..."
    cp -r $COMMON_TEMPLATES $SERVICE/app/

    echo "Copying static files to $SERVICE..."
    cp -r $COMMON_STATIC $SERVICE/app/
done

echo "All files copied successfully!"

