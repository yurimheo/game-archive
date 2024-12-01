#!/bin/bash

# 공통 레이아웃 파일들을 복사하는 셸 스크립트입니다.
# 사용하기 위해서는 `.\sync_common_assets.sh` 를 입력하면 됩니다.
# 또한 `./sy` 정도만 입력해도 자동 완성 됩니다!

# common-service 디렉토리
COMMON_SERVICE_DIR="../common-service"

# 복사 받을 디렉토리
TARGET_TEMPLATE_DIR="./app/templates"
TARGET_STATIC_DIR="./app/static"

# 복사 여부 확인
echo "공통 파일들을 복사하려고 합니다. 기존 파일이 덮어써질 수 있습니다. 진행하시겠습니까? (y/n)"
read -p "Enter your choice: " CHOICE

if [[ "$CHOICE" == "y" || "$CHOICE" == "Y" ]]; then
    # 템플릿 복사
    echo "템플릿을(를) 복사하고 있습니다! 조금만 기다려주세요! 🤗"
    cp -v ${COMMON_SERVICE_DIR}/templates/base.html ${TARGET_TEMPLATE_DIR}/
    cp -v ${COMMON_SERVICE_DIR}/templates/footer.html ${TARGET_TEMPLATE_DIR}/
    cp -v ${COMMON_SERVICE_DIR}/templates/header.html ${TARGET_TEMPLATE_DIR}/

    # CSS 복사
    echo "CSS을(를) 복사하고 있습니다! 조금만 기다려주세요! 🤗"
    cp -v ${COMMON_SERVICE_DIR}/static/css/base.css ${TARGET_STATIC_DIR}/css/
    cp -v ${COMMON_SERVICE_DIR}/static/css/footer.css ${TARGET_STATIC_DIR}/css/
    cp -v ${COMMON_SERVICE_DIR}/static/css/header.css ${TARGET_STATIC_DIR}/css/

    # JS 복사
    echo "JS을(를) 복사하고 있습니다! 조금만 기다려주세요! 🤗"
    cp -v ${COMMON_SERVICE_DIR}/static/js/header.js ${TARGET_STATIC_DIR}/js/

    # 이미지 복사
    echo "이미지을(를) 복사하고 있습니다! 조금만 기다려주세요! 🤗"
    cp -v ${COMMON_SERVICE_DIR}/static/images/logo.png ${TARGET_STATIC_DIR}/images/
    cp -v ${COMMON_SERVICE_DIR}/static/images/search-filter.png ${TARGET_STATIC_DIR}/images/
    cp -v ${COMMON_SERVICE_DIR}/static/images/slide1.jpg ${TARGET_STATIC_DIR}/images/
    cp -v ${COMMON_SERVICE_DIR}/static/images/slide2.jpg ${TARGET_STATIC_DIR}/images/
    cp -v ${COMMON_SERVICE_DIR}/static/images/slide3.jpg ${TARGET_STATIC_DIR}/images/
    cp -v ${COMMON_SERVICE_DIR}/static/images/main-hyl.jpg ${TARGET_STATIC_DIR}/images/

    echo "복사 성공하였습니다. 감사합니다! 🎀"
else
    echo "복사가 취소되었습니다."
fi
