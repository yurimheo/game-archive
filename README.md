# 🎮 Game Archive: 하이브리드 클라우드 기반 게임 커뮤니티 플랫폼

> AWS와 온프레미스를 연동한 실전형 DevOps 프로젝트,  
> 인프라 자동화부터 MSA 마이그레이션까지 직접 구축한 **게임 커뮤니티 웹서비스**

![badge](https://img.shields.io/badge/Platform-Hybrid_Cloud-orange)
![badge](https://img.shields.io/badge/Infra-AWS_+_OnPrem-lightgrey)
![badge](https://img.shields.io/badge/Automation-Terraform_·_Ansible-blue)
![badge](https://img.shields.io/badge/Backend-Flask-%23000000)
![badge](https://img.shields.io/badge/Orchestration-Kubernetes-%23326CE5)
![badge](https://img.shields.io/badge/CI/CD-GitHub_Actions_·_ArgoCD-green)
![badge](https://img.shields.io/badge/Monitoring-Prometheus_·_Grafana-red)

---

## 🧾 프로젝트 개요

- **프로젝트명**: 하이브리드 클라우드 기반 게임 커뮤니티 웹서비스  
- **진행 기간**: 2024.11 ~ 2024.12  
- **팀 구성**: 6인 (팀장)  
- **주요 기술스택**: Flask, Docker, Kubernetes, Ansible, Terraform, MySQL, Nginx, AWS, Prometheus, Grafana  

---

## 🧩 프로젝트 소개

이 프로젝트는 **AWS와 온프레미스를 연동한 하이브리드 클라우드 인프라** 위에서 운영되는  
**MSA 기반 게임 커뮤니티 플랫폼**을 구축한 실전형 DevOps 경험입니다.

초기에는 모놀리식 구조에서 시작해 **MSA로 마이그레이션**하며 아키텍처 구조 설계의 유연성을 경험했고,  
**Terraform + Ansible로 인프라를 자동화**, CI/CD, 모니터링, 테스트까지 전체 시스템을 직접 설계하고 운영했습니다.

---

## 🧰 주요 기여 및 역할 (팀장 / 인프라 & 백엔드 총괄)

### 🎯 PM 및 협업 리딩
- 전체 일정 관리, 역할 분배, 문서화 및 기술 커뮤니케이션 총괄

### ☁️ Terraform: AWS 리소스 IaC 구성
- VPC, EC2, RDS, S3, ALB 등 인프라 구성 자동화
- 모듈화 및 재사용 가능한 Terraform 구조 설계

### 🔧 Ansible: 온프레미스 서버 자동화 및 K8s 클러스터 설치
- Kubespray 없이 직접 구성한 **커스텀 Playbook 기반 K8s 구축**
    - `site.yml`, `install-helm-ingress-nginx.yml`, `install_argocd.yml`, `set_google_dns.yml`
- Helm, Ingress, ArgoCD, MetalLB, DNS 설정 자동화
- SSH 키 배포, 사용자 설정, 인벤토리 구성 등 서버 초기 세팅 자동화

### 🌐 웹서비스 개발 (Flask)
- **Q&A, 뉴스, 공략 게시판 등 CRUD 기능 전체 구현**
- 공통 템플릿 구성 (Jinja2), API 분리 기반 MSA 설계
- 서비스별 Flask 앱 분리 및 API 마이그레이션 수행

### 🛢️ DB 설계 및 연동
- 각 API 서비스에 맞춘 **MySQL 스키마 설계**
- 데이터 정규화 및 관계 설계 → 서비스 분리 시에도 구조 유연성 확보
- SQLAlchemy ORM 기반 DB 연결 및 마이그레이션 적용

### 📄 문서화 및 설계 시각화
- 아키텍처 다이어그램, 플로우 차트, README 및 명세서 작성

---

## 📊 인프라 아키텍처

![Game Archive 인프라 아키텍처](https://i.postimg.cc/d368skK5/team-archive-infrastructure-architecture.png)

## 🔄 서비스 플로우차트

> 사용자 관점에서 서비스가 어떻게 흐르고 연결되는지를 한눈에 파악할 수 있도록 직접 설계한 플로우 차트입니다.

![서비스 플로우차트](https://i.postimg.cc/qvS2vH9H/Team3-Flow-Chart-drawio-1.png)

### 📦 CI/CD 파이프라인
- GitHub Actions: 코드 커밋 → Docker 이미지 빌드
- DockerHub 업로드 → ArgoCD로 자동 배포
- Slack으로 배포 상태 자동 알림 전송

### 🧩 Kubernetes 클러스터
- 온프레미스에 구성된 MSA 기반 서비스 구조
- Helm으로 API 서비스(Nginx + Flask) 반복 배포 및 관리
- 각 서비스는 MySQL 인스턴스와 독립 연결

### 🌐 네트워크 및 이중화
- Nginx Master/Slave 구성 + Keepalived로 고가용성 확보
- Ingress Controller 통해 외부 요청 및 서비스 트래픽 처리

### 📈 모니터링 및 테스트
- Prometheus + Grafana: 실시간 메트릭 수집 및 시각화
- AlertManager + Slack: 장애 발생 알림 설정
- JMeter, LitmusChaos: 부하 및 장애 주입 테스트 수행

---

## 🚧 기술적 이슈 & 해결 경험

| 이슈 | 해결 방법 |
|------|-----------|
| 서비스 간 DB 연결 오류, 지연 현상 | 연결 방식 변경 및 DB 설정 튜닝 후 해결 |
| 초기 모놀리식 구조 → MSA 전환 시 API 재설계 | Flask Blueprint 및 서비스별 독립 구조 도입 |
| K8s 배포 환경 설정 충돌 | Helm 값 분리 및 재빌드 전략 적용 |
| CI/CD 파이프라인 오작동 | GitHub Actions 로그 기반 디버깅 및 Docker 재빌드 |

---

## 🌱 회고 및 성장

이번 프로젝트를 통해 **DevOps의 핵심 흐름**을 실무처럼 체험할 수 있었습니다.

- **Terraform과 Ansible로 인프라 자동화**의 실질적인 구현력 향상
- 구조 설계 미숙으로 겪었던 어려움을 통해, **초기 설계의 중요성**을 체감
- AWS와 온프레미스를 연동한 하이브리드 인프라 운영 경험을 통해  
  **클라우드 네이티브 환경에 대한 확신과 방향성**을 얻게 되었습니다.

> 학습의 단계를 넘어, 실전에서 동작하는 구조를 만든 경험은  
> 앞으로의 **DevOps 및 시스템 엔지니어링 커리어의 중요한 전환점**이 되었습니다.

---

## 🧑‍💻 실행 방법

```bash
# 개발 환경 세팅 예시
git clone https://github.com/your-id/game-archive-flask-msa-k8s-Iac.git
cd backend
pip install -r requirements.txt

# kubectl, ansible, terraform 등은 환경에 맞게 설치 필요

## 🎥 웹서비스 미리보기

![웹 시연 GIF](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2tyNXJmbTF4b2EwNW51Nm0wd3czb3VlcXo5cXR6ZHExM2ZpdXVkdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/QtcCBK3xO8qMwJ8tVu/giphy.gif)


---
## 🔗 관련 링크

- [Ansible 기반 Kubernetes 클러스터 자동화 스크립트](https://github.com/yurimheo/ansible-k8s-cluster)
