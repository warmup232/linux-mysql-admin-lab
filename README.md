# linux-mysql-admin-lab

Linux 및 MySQL 서버 관리 실습 프로젝트

## 프로젝트 소개

Linux 서버 및 MySQL 데이터베이스 관리 역량을 학습하기 위해 진행한 개인 실습 프로젝트입니다.

Linux 환경에서 MySQL 데이터베이스를 구성하고, Flask를 활용하여 직원, 부서, 프로젝트 정보를 관리하는 REST API를 구현했습니다.

## 개발 환경

- Ubuntu Server
- MySQL
- VMware Workstation

## 주요 기능

### 회사 관리 API

직원, 부서, 프로젝트 정보를 관리할 수 있는 RESTful 백엔드 API입니다.

### 기술 스택

- Python
- Flask
- MySQL
- REST API
- Linux / Ubuntu
- Git / GitHub

## 데이터베이스

관계형 데이터베이스인 MySQL을 사용했습니다.

주요 테이블:

- Departments
- Employees
- Projects

주요 데이터베이스 구성:

- 테이블 간 외래 키(Foreign Key) 관계
- Unique 제약 조건
- Timestamp를 이용한 데이터 변경 시간 관리

## 데이터베이스 보안

애플리케이션에서는 MySQL `root` 계정을 사용하지 않습니다.

별도의 애플리케이션 전용 사용자를 생성하고 필요한 권한만 부여했습니다.

부여된 권한:

- SELECT
- INSERT
- UPDATE
- DELETE

최소 권한 원칙(Principle of Least Privilege)에 따라 데이터베이스 접근 권한을 제한했습니다.

## API 엔드포인트

### Employees

| Method | Endpoint | 설명 |
|---|---|---|
| GET | `/employees` | 전체 직원 조회 |
| GET | `/employees/<id>` | ID로 직원 조회 |
| POST | `/employees` | 직원 등록 |
| PUT | `/employees/<id>` | 직원 정보 수정 |
| DELETE | `/employees/<id>` | 직원 삭제 |

## API 응답 예시

```json
{
  "id": 1,
  "name": "Kim Minsoo",
  "email": "minsoo@example.com",
  "department": "IT"
}
## 데이터베이스 설정

다음 SQL 스크립트를 순서대로 실행하여 데이터베이스를 구성합니다.

database/01_schema.sql
database/02_seed.sql
database/03_permissions.sql
프로젝트 구조
company-management-api/
├── app/
│   └── app.py
├── database/
│   ├── 01_schema.sql
│   ├── 02_seed.sql
│   └── 03_permissions.sql
├── .gitignore
├── requirements.txt
└── README.md

## 보안 참고

데이터베이스 계정 정보는 보안을 위해 소스 코드에 포함하지 않았습니다.
