#!/bin/bash

# common-service 디렉토리
COMMON_SERVICE_DIR="../common-service"

# discount-service 디렉토리
TARGET_TEMPLATE_DIR="./app/templates"
TARGET_STATIC_DIR="./app/static"

# 템플릿 복사
echo "Copying templates..."
cp -v ${COMMON_SERVICE_DIR}/templates/base.html ${TARGET_TEMPLATE_DIR}/
cp -v ${COMMON_SERVICE_DIR}/templates/footer.html ${TARGET_TEMPLATE_DIR}/
cp -v ${COMMON_SERVICE_DIR}/templates/header.html ${TARGET_TEMPLATE_DIR}/

# CSS 복사
echo "Copying CSS..."
cp -v ${COMMON_SERVICE_DIR}/static/css/base.css ${TARGET_STATIC_DIR}/css/
cp -v ${COMMON_SERVICE_DIR}/static/css/footer.css ${TARGET_STATIC_DIR}/css/
cp -v ${COMMON_SERVICE_DIR}/static/css/header.css ${TARGET_STATIC_DIR}/css/

# JS 복사
echo "Copying JS..."
cp -v ${COMMON_SERVICE_DIR}/static/js/header.js ${TARGET_STATIC_DIR}/js/

# 이미지 복사
echo "Copying images..."
cp -v ${COMMON_SERVICE_DIR}/static/images/logo.png ${TARGET_STATIC_DIR}/images/
cp -v ${COMMON_SERVICE_DIR}/static/images/search-filter.png ${TARGET_STATIC_DIR}/images/
cp -v ${COMMON_SERVICE_DIR}/static/images/slide1.jpg ${TARGET_STATIC_DIR}/images/
cp -v ${COMMON_SERVICE_DIR}/static/images/slide2.jpg ${TARGET_STATIC_DIR}/images/
cp -v ${COMMON_SERVICE_DIR}/static/images/slide3.jpg ${TARGET_STATIC_DIR}/images/

echo "Copy complete!"

